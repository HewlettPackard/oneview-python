import requests
requests.packages.urllib3.disable_warnings()
import sys
import json
import logging
import time
from threading import Thread
import time

from config_loader import try_load_from_file

rest_call_timeout_sec = 60
max_retries_in_session = 50
polling_call_timeout_sec = 10 * 60
sec_between_polling = 10


class ServerHardware(Thread):

    def __init__(self, config):
        # override_version=None, retries=max_retries_in_session, appliance_ip_address=None):

        if config.get("appliance_ip"):
            self.base_url = "https://" + config.get("appliance_ip")

        # create a persistant session so that we can retry if the appliance goes offline (e.g. first time setup)
        self.sess = requests.Session()
        self.retries = config.get("max_retries")
        adap = requests.adapters.HTTPAdapter(max_retries=self.retries)
        self.sess.mount('http://', adap)
        self.sess.mount('https://', adap)

        # if version is passed in, use that.  Else use the default for the program
        # Default to the minimal version number that implements all the requirements that we need. Defined per program.
        # Eventually we may need version overrides at each REST call.
        if config.get("api_version"):
            self.api_version = config.get("api_version")
        else:
            self.api_version = 120

        logging.info("The API Version utilized is {0}.".format(self.api_version))
        self._header = {'X-API-Version': '{}'.format(self.api_version), 'Content-Type': 'application/json'}
        self._secure_header = {}
        self.appliance_ip = config.get("appliance_ip")
        self.appliance_username = config['credentials'].get("userName")
        self.appliance_password = config['credentials'].get("password")
        self.migrate_source_ip = config.get("source_appliance_ip")
        self.migrate_source_username = config['credentials'].get("source_username")
        self.migrate_source_password = config['credentials'].get("source_password")
        self.migrate_source_hardware_uri = None

    def get_secure_headers(self):
        """Helper method to appliance_request().
        Gives header information required by the appliance with authentication information.
        Return
        ------
        _secure_header: dict. Dictionary containing X-API-Verions, Content-Type, and Auth.  The Auth parameter value is a sessionID.
        """
        # Once _secure_header is defined, we can use it over and over again for the duration of its life.
        # Note, the header is only good for that user (administrator), 24 hours, and until the next reboot.
        if self._secure_header:
            return self._secure_header
        payload = {"userName": self.appliance_username, "password": self.appliance_password}
        url = '/rest/login-sessions'
        try:
            r = self.sess.post(self.base_url + url, verify=False, headers=self._header, data=json.dumps(payload), timeout=rest_call_timeout_sec)
        except requests.exceptions.RequestException as e:
            raise Exception("There was an issue connecting to the appliance to get headers. Exception message: {0}".format(e))
        except Exception as e:
            raise Exception("There was an issue with the HTTP Call to get headers. Exception message: {0}".format(e))
        if r.status_code >= 300:
            raise Exception('Failure to get secure connection. Status {0}.'.format(r.status_code))
        try:
            safe_json = r.json()
            self._secure_header = self._header.copy()
            self._secure_header['Auth'] = safe_json.get('sessionID')
            if self._secure_header['Auth'] is None:
                raise Exception('Auth token for the header is undefined.  No Session ID available. Status: {0}.'.format(r.status_code))
            return self._secure_header
        except ValueError as e:
            raise Exception('Failure to get a JSON value from the response. Status: {0}.'.format(r.status_code))
        except:
            raise Exception('Failure to access the sessionID from the response. Status: {0}. JSON: {1}'.format(r.status_code, r.json()))

    def appliance_request(self, request_type, url, secure=True, payload=None, other_properties={}, extra_headers={}, poll=True,
                          timeout=None):

        if timeout is None:
            timeout = rest_call_timeout_sec

        if not secure:
            head = self._header
        else:
            head = self.get_secure_headers()

        full_url = self.base_url + url
        logging.debug("Preparing HTTP {0} request.".format(request_type))
        logging.debug("Preparing URL: {0}.".format(full_url))
        logging.debug("Preparing Headers: {0}.".format(head))
        logging.debug("Preparing Payload: {0}.".format(json.dumps(payload)))
        polling_results = {}
        try:
            if request_type == "POST":
                r = self.sess.post(full_url, verify=False, headers=head, data=json.dumps(payload), timeout=timeout, **other_properties)
            # elif request_type == "PUT":
            #     r = self.sess.put(full_url, verify=False, headers=head, data=json.dumps(payload), timeout=timeout, **other_properties)
            # elif request_type == "GET":
            #     r = self.sess.get(full_url, verify=False, headers=head, timeout=timeout, **other_properties)
            # elif request_type == "DELETE":
            #     r = self.sess.delete(full_url, verify=False, headers=head, timeout=timeout, **other_properties)
            else:
                raise Exception(
                    "RestAppliance attempted to call an http request other than POST, PUT, or GET. request_type: {0}. url: {1}".format(request_type, url))
            try:
                safe_json_result = r.json()
            except:
                safe_json_result = {}
            logging.debug("Returned. Status code: {0}.".format(r.status_code))
            logging.debug("Returned. JSON: {0}.".format(safe_json_result))
            # 202 status codes indicate a task that is pollable. The calling function may not know that this will return a 202.
            success = False

            if r.status_code == 202:
                if not poll:
                    return (True, r, safe_json_result, {'task_state': 'N/A', 'task_status': 'N/A'})
                (task_state, task_status) = self.poll_for_task(url, r)
                polling_results = {'task_state': task_state,
                                   'task_status': task_status}
                if task_state == "Completed":
                    success = True

            elif r.status_code < 300:
                success = True
            else:
                polling_results = {'task_state': safe_json_result.get('errorCode', 'Error'),
                                   'task_status': safe_json_result.get('details', str(safe_json_result))}
            return (success, r, safe_json_result, polling_results)
        except requests.exceptions.RequestException as e:
            raise Exception("There was an issue connecting to the appliance. Exception message: {0}".format(e))
        except Exception as e:
            raise Exception("There was an issue with the HTTP Call. Exception message: {0}".format(e))

    def poll_for_task(self, calling_url, response):
        '''Helper method to appliance_request().
        Status Response 202 indicates an asynchronous REST call.  Poll until the task is complete or error.
        Adds to the set of parameters that appliance_request() returns.
        Parameters
        ----------
        calling_url : string
            The URL that was called in appliance_request.
        response : a response object from a Requests call.
        Return
        ------
        tuple containing:
            task_state: str.  A short summary of the execution/completion status
            task_status: str. State of the task.  For Example: Unknown, Running, Terminated, Error, Warning, Completed.
        '''
        url = response.headers.get('location')
        if url is None:
            url = response.json().get('uri')
        if url is None:
            raise Exception('Could not read the task to poll. Originating request on URL: {0}.'.format(calling_url))
        full_rest_url = self.base_url + url
        task_state = 'Running'
        start_time = time.time()
        try:
            logging.debug("Starting polling the rest task {0}.".format(url))
            already_reset_session = False
            while task_state in ['Running', 'New', 'Pending', 'Starting']:
                if time.time() >= start_time + polling_call_timeout_sec:
                    raise Exception('Task Polling did not respond within {0} seconds. Time out and exit. Originating request on URL: {1}'.format(
                        polling_call_timeout_sec, calling_url))
                time.sleep(sec_between_polling)
                r_tree = None
                try:
                    logging.debug("Current Time {0}".format(time.asctime(time.localtime(time.time()))))
                    r_tree = self.sess.get(full_rest_url + "?view=tree", verify=False, headers=self.get_secure_headers(), timeout=rest_call_timeout_sec)
                except Exception as e:
                    logging.exception("Migration failed: " + str(e))
                    if already_reset_session:
                        raise Exception("There was an issue with the HTTP Call for task polling. Exception message: {0}".format(e))
                    # delete and recreate of the session if it loses connection.  Changes in IP address, FQDN, etc can make use lose the session.
                    else:
                        already_reset_session = True
                        self.sess.close()
                        self.sess = requests.Session()
                        adap = requests.adapters.HTTPAdapter(max_retries=self.retries)
                        self.sess.mount('http://', adap)
                        self.sess.mount('https://', adap)
                if r_tree:
                    r_treejson = r_tree.json()
                    task_resource = r_treejson.get('resource')
                    task_state = task_resource.get('taskState')
                    task_status = task_resource.get('taskStatus', '')
                    task_errors = task_resource.get('taskErrors', None)
                    if task_errors:
                        print("Task failed.")
                        # in case of errors place them in log output and append to status message
                        for e in task_errors:
                            logging.error(e)
                        task_status += ";" + ";".join([str(e) for e in task_errors])
                    logging.debug("Percent Complete : {0}. State: {1}. Status: {2}.".format(task_resource.get('percentComplete'), task_state, task_status))
                    logging.debug("The task tree for {0} is:".format(full_rest_url))
                    logging.debug("Returned JSON: {0}".format(r_treejson))
                else:
                    logging.debug("Exception during get call, response was not set")
                    logging.debug("Unable to get the task tree for {0}".format(full_rest_url))
            return(task_state, task_status)
        except ValueError as e:
            raise Exception('Error getting the JSON results from the task. Originating request on URL: {0}. Exception: {1}'.format(calling_url, e))
        except Exception as e:
            raise Exception('Error in polling for the task. Originating request on URL: {0}. Exception: {1}'.format(calling_url, e))

    def get_migratable_device(self):
        '''Method to get list of migratable device .

        Return
        ------
        list containing server hardware that are eligible for migration:

        '''

        url = '/rest/migrate/migratable-server-hardware/'
        payload = {"ipAddress": self.migrate_source_ip,
                   "username": self.migrate_source_username, "password": self.migrate_source_password}

        (migrateable_success, migrateable_resp, migrateable_json_response, _) = self.appliance_request(
            request_type='POST', url=url, secure=True, payload=payload)
        if migrateable_success:
            logging.info('migrateable accepted.')
        else:
            raise Exception('migratable device listing failed. Status: {0}. JSON Response: {1}'.format(migrateable_resp.status_code,
                                                                                                       json.dumps(migrateable_json_response, sort_keys=True, indent=4, separators=(',', ': '))))

        sh_list = migrateable_json_response['serverHardware']

        return sh_list

    def do_migrate(self):
        '''Method to perform the migration of selected harware .

        '''
        url = '/rest/migrate'
        payload = {"ipAddress": self.migrate_source_ip, "username": self.migrate_source_username,
                   "password": self.migrate_source_password, "uri": self.migrate_source_hardware_uri}

        migrate_json_response = {}
        (migrate_success, migrate_resp, migrate_json_response, _) = self.appliance_request(
            request_type='POST', url=url, secure=True, payload=payload)
        if migrate_success:
            logging.info('migration successful.')
        else:
            raise Exception('migration failed. Status: {0}. JSON Response: {1}'.format(migrate_resp.status_code,
                                                                                       json.dumps(migrate_json_response, sort_keys=True, indent=4, separators=(',', ': '))))


if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    config = try_load_from_file()
    max_retries_in_session = 10

    ra = ServerHardware(config)
    # override_version=4000,
    #                    retries=max_retries_in_session,
    #                    appliance_ip_address="172.27.2.235"
    #                    )

    sh_list = ra.get_migratable_device()

    if len(sh_list) <= 0:
        sys.exit()
    else:
        print("List of server hardware for migrate: ")
    for i, sh in enumerate(sh_list):
        print(50 * "#")
        print("Hardware number: ", i + 1)

        for x, y in sh.items():
            if x == 'status':
                continue
            print(x, ":", y)

    select_sh_list = [int(item) for item in input("Enter the list of server hardware to migrate: ").split()]
    for select_sh in select_sh_list:

        if select_sh in range(1, len(sh_list) + 1):
            select_sh = int(select_sh)
            print("You have chosen: " + str(select_sh))

        else:
            print('You chosen wrong!')
            sys.exit()
        try:
            ra.migrate_source_hardware_uri = sh_list[select_sh - 1]["uri"]
            t1 = Thread(target=ra.do_migrate)
            t1.start()

            t1.join()

        except ValueError as e:
            raise Exception('Error performing the migration.Server hardware is : {0}. Exception: {1}'.format(sh_list[select_sh - 1]["name"], e))
