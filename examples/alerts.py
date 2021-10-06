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

from pprint import pprint
from config_loader import try_load_from_file
from hpeOneView.resources.resource import extract_id_from_uri
from hpeOneView.oneview_client import OneViewClient

CONFIG = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

_CLIENT = OneViewClient(CONFIG)

# Getting the first 5 ALERTS
print("\nGetting the first 5 ALERTS")
ALERTS = _CLIENT.alerts.get_all(0, 5)
for alert in ALERTS:
    print("uri: '{uri}' | type: '{type}' | alertState: '{alertState}'".format(**alert))

# Get a specific alert (first of the list that was obtained in previous item)
print("\nGet a specific alert")
ID_ALERT_BY_ID = extract_id_from_uri(ALERTS[0]['uri'])
print("Find id == %s" % ID_ALERT_BY_ID)
ALERT_BY_ID = _CLIENT.alerts.get(ID_ALERT_BY_ID)
print("uri: '%s' | alertState: '%s'" % (ALERT_BY_ID['uri'], ALERT_BY_ID['alertState']))

# Get by Uri
print("Find uri == %s" % (alert['uri']))
ALERT_BY_URI = _CLIENT.alerts.get(alert['uri'])
print("uri: '%s' | alertState: '%s'" % (ALERT_BY_URI['uri'], ALERT_BY_URI['alertState']))

# Find first alert by state
print("\nGet first alert by state: Cleared")
ALERT_BY_STATE = _CLIENT.alerts.get_by('alertState', 'Cleared')[0]
print("Found alert by state: '%s' | uri: '%s'" % (ALERT_BY_STATE['alertState'],\
         ALERT_BY_STATE['uri']))

# Updates state alert and add note
print("\nUpdate state alert and add a note")
ALERT_TO_UPDATE = {
    'uri': ALERT_BY_STATE['uri'],
    'alertState': 'Active',
    'notes': 'A note to delete!'
}
ALERT_UPDATED = _CLIENT.alerts.update(ALERT_TO_UPDATE)
print("uri = '%s' | alertState = '%s'" % (ALERT_BY_STATE['uri'], ALERT_BY_STATE['alertState']))
print("Update alert successfully.")
pprint(ALERT_UPDATED)

# Filter by state
print("\nGet all ALERTS filtering by alertState")
ALERTS = _CLIENT.alerts.get_all(filter="\"alertState='Locked'\"", view="day", count=10)
for alert in ALERTS:
    print("'%s' | type: '%s' | alertState: '%s'" % (alert['uri'], alert['type'],\
         alert['alertState']))

# Deletes the alert
print("\nDelete an alert")
_CLIENT.alerts.delete(ALERT_BY_ID)
print("Successfully deleted alert")

# Deletes the AlertChangeLog item identified by URI
print("\nDelete alert change log by URI")
# filter by user entered logs
LIST_CHANGE_LOGS = [x for x in ALERT_UPDATED['changeLog'] if x['userEntered'] is True]
URI_NOTE = LIST_CHANGE_LOGS[-1]['uri']
_CLIENT.alerts.delete_alert_change_log(URI_NOTE)
print("Note with URI '%s' deleted" % URI_NOTE)
