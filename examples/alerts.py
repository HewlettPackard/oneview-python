# -*- coding: utf-8 -*-
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
from config_loader import try_load_from_file
from hpeOneView.resources.resource import extract_id_from_uri
from pprint import pprint

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

_client = OneViewClient(config)

# Getting the first 5 alerts
print("\nGetting the first 5 alerts")
alerts = _client.alerts.get_all(0, 5)
for alert in alerts:
    print("uri: '{uri}' | type: '{type}' | alertState: '{alertState}'".format(**alert))

# Get a specific alert (first of the list that was obtained in previous item)
print("\nGet a specific alert")
id_alert_by_id = extract_id_from_uri(alerts[0]['uri'])
print("Find id == %s" % id_alert_by_id)
alert_by_id = _client.alerts.get(id_alert_by_id)
print("uri: '%s' | alertState: '%s'" % (alert_by_id['uri'], alert_by_id['alertState']))

# Get by Uri
print("Find uri == %s" % (alert['uri']))
alert_by_uri = _client.alerts.get(alert['uri'])
print("uri: '%s' | alertState: '%s'" % (alert_by_uri['uri'], alert_by_uri['alertState']))

# Find first alert by state
print("\nGet first alert by state: Cleared")
alert_by_state = _client.alerts.get_by('alertState', 'Cleared')[0]
print("Found alert by state: '%s' | uri: '%s'" % (alert_by_state['alertState'], alert_by_state['uri']))

# Updates state alert and add note
print("\nUpdate state alert and add a note")
alert_to_update = {
    'uri': alert_by_state['uri'],
    'alertState': 'Active',
    'notes': 'A note to delete!'
}
alert_updated = _client.alerts.update(alert_to_update)
print("uri = '%s' | alertState = '%s'" % (alert_by_state['uri'], alert_by_state['alertState']))
print("Update alert successfully.")
pprint(alert_updated)

# Filter by state
print("\nGet all alerts filtering by alertState")
alerts = _client.alerts.get_all(filter="\"alertState='Locked'\"", view="day", count=10)
for alert in alerts:
    print("'%s' | type: '%s' | alertState: '%s'" % (alert['uri'], alert['type'], alert['alertState']))


# Deletes the AlertChangeLog item identified by URI
print("\nDelete alert change log by URI")
# filter by user entered logs
list_change_logs = [x for x in alert_updated['changeLog'] if x['userEntered'] is True]
uri_note = list_change_logs[-1]['uri']
_client.alerts.delete_alert_change_log(uri_note)
print("Note with URI '%s' deleted" % uri_note)
# Deletes the alert
print("\nDelete an alert")
_client.alerts.delete(alert_by_id)
print("Successfully deleted alert")
