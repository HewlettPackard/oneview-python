#!/usr/bin/env python3

###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from hpeOneView.oneview_client import OneViewClient
from functools import partial

import amqp
import amqp.spec
import datetime
import json
import ssl


def callback(channel, msg):
    # ACK receipt of message
    channel.basic_ack(msg.delivery_tag)

    # Convert from json into a Python dictionary
    body = json.loads(msg.body)

    # Create a new variable name 'resource' to point to the
    # nested resource dictionary inside of the body
    resource = body['resource']

    # Test to make sure that there is an alertState key
    # in the resource dictionary, if there is continue
    if 'alertState' in list(resource.keys()):
        # Filter only "Active" alerts
        if (('Active' == resource['alertState']) and
                ('Critical' == resource['severity']) and
                ('Created' == body['changeType'])):
            # Print out the requested information
            print('')
            print('original OneView alert:')
            print('------------------------------------------')
            print('changeType: %s' % (body['changeType']))
            print('data: %s' % (body['data']))
            print('eTag: %s' % (body['eTag']))
            print('newState: %s' % (body['newState']))
            print('resourceUri: %s' % (body['resourceUri']))
            print('resource:')
            print('------------------------------------------')
            print('    alertState: %s' % (resource['alertState']))
            print('    alertTypeID: %s' % (resource['alertTypeID']))
            print('    description: %s' % (resource['description']))
            print('    changeLog: %s' % (resource['changeLog']))
            print('    severity: %s' % (resource['severity']))
            print('    resourceName: %s'
                  % (resource['associatedResource']['resourceName']))
            print('    resourceCategory: %s'
                  % (resource['associatedResource']['resourceCategory']))
            print('    uri: %s' % (resource['uri']))
            # The timestamp from the appliance is in ISO 8601 format, convert
            # it to a Python datetime format instead
            atime = (datetime.datetime.strptime(body['timestamp'],
                                                '%Y-%m-%dT%H:%M:%S.%fZ'))
            # Print the timestamp is a simple format (still in UTC)
            print('timestamp: %s' % (atime.strftime('%Y-%m-%d %H:%M:%S')))
            print('resourceUri: %s' % (body['resourceUri']))
            print('')

    # Cancel this callback
    if msg.body == 'quit':
        channel.basic_cancel(msg.consumer_tag)


def recv(host, route):
    # Create and bind to queue
    EXCHANGE_NAME = 'scmb'
    dest = host + ':5671'

    # Setup our ssl options
    ssl_options = ({'ca_certs': 'caroot.pem',
                    'certfile': 'client.pem',
                    'keyfile': 'key.pem',
                    'cert_reqs': ssl.CERT_REQUIRED,
                    'ssl_version': ssl.PROTOCOL_TLSv1_1,
                    'server_side': False})

    # Connect to RabbitMQ
    conn = amqp.Connection(dest, login_method='EXTERNAL', ssl=ssl_options)
    conn.connect()

    ch = conn.channel()
    qname, _, _ = ch.queue_declare()
    ch.queue_bind(qname, EXCHANGE_NAME, route)
    ch.basic_consume(qname, callback=partial(callback, ch))

    # Start listening for messages
    while ch.callbacks:
        ch.wait(amqp.spec.Queue.BindOk)

    ch.close()
    conn.close()


def acceptEULA(oneview_client):
    # See if we need to accept the EULA before we try to log in
    eula_status = oneview_client.connection.get_eula_status()
    try:
        if eula_status is True:
            oneview_client.connection.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def getCertCa(oneview_client):
    ca_cert = oneview_client.certificate_authority
    ca_all = ca_cert.get_all()
    ca = open('caroot.pem', 'w+')
    for certs in ca_all:
        if certs['certificateDetails']['aliasName'] == 'localhostSelfSignedCertificate':
            cert = certs['certificateDetails']['base64Data']
            ca.write(cert)
            ca.close()


def genRabbitCa(oneview_client):
    certificate_ca_signed_client = {
        "commonName": "default",
        "type": "RabbitMqClientCertV2"
    }
    oneview_client.certificate_rabbitmq.generate(certificate_ca_signed_client)


def getRabbitKp(oneview_client):
    cert = oneview_client.certificate_rabbitmq.get_key_pair('default')
    ca = open('client.pem', 'w+')
    ca.write(cert['base64SSLCertData'])
    ca.close()
    ca = open('key.pem', 'w+')
    ca.write(cert['base64SSLKeyData'])
    ca.close()


def main():
    if amqp.VERSION < (2, 1, 4):
        print("WARNING: This script has been tested only with amqp 2.1.4, "
              "we cannot guarantee that it will work with a lower version.\n")

    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-a', '--appliance', dest='host', required=True,
                        help='HPE OneView Appliance hostname or IP')
    parser.add_argument('-u', '--user', dest='user', required=False,
                        default='Administrator', help='HPE OneView Username')
    parser.add_argument('-p', '--pass', dest='passwd', required=True,
                        help='HPE OneView Password')
    parser.add_argument('-r', '--route', dest='route', required=False,
                        default='scmb.alerts.#', help='AMQP Routing Key')
    parser.add_argument('-g', '--gen', dest='gen', required=False,
                        action='store_true',
                        help='Generate the Rabbit MQ keypair and exit')
    parser.add_argument('-d', '--download', dest='down', required=False,
                        action='store_true',
                        help='Download the required keys and certs then exit')
    args = parser.parse_args()
    config = {
        "ip": args.host,
        "credentials": {
            "userName": args.user,
            "password": args.passwd
        }
    }

    oneview_client = OneViewClient(config)
    acceptEULA(oneview_client)

    # Generate the RabbitMQ keypair (only needs to be done one time)
    if args.gen:
        genRabbitCa(oneview_client)
        sys.exit()

    if args.down:
        getCertCa(oneview_client)
        getRabbitKp(oneview_client)
        sys.exit()

    recv(args.host, args.route)


if __name__ == '__main__':
    import sys
    import argparse

    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
