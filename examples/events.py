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

CONFIG = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

OPTIONS = {
    "description": "This is a very simple test EVENT",
    "serviceEventSource": "true",
    "serviceEventDetails": {
        "caseId": "1234",
        "primaryContact": "contactDetails",
        "remoteSupportState": "Submitted"
    },
    "severity": "OK",
    "healthCategory": "PROCESSOR",
    "EVENTTypeID": "hp.justATest",
    "rxTime": "2012-05-14T20:23:56.688Z",
    "urgency": "None",
    "EVENTDetails":
    [{"EVENTItemName": "ipv4Address",
      "EVENTItemValue": "198.51.100.5",
      "isThisVarbindData": "false",
      "varBindOrderIndex": -1}]
}

# Try load CONFIG from a file (if there is a CONFIG file)
CONFIG = try_load_from_file(CONFIG)

_CLIENT = OneViewClient(CONFIG)

# Getting the first 5 EVENTS
print("\nGetting the first 5 EVENTS:")
EVENTS = _CLIENT.events.get_all(0, 5)
for EVENT in EVENTS:
    print("EVENTTypeID: '%s' | description: %s " % (EVENT['description'], EVENT['EVENTTypeID']))

# Create an Event
EVENT = _CLIENT.events.create(OPTIONS)
print("\nCreated EVENT successfully.\n  uri = '%s'" % (EVENT['uri']))

# Get by Uri
print("\nFind uri == %s" % ('/rest/EVENTS/24'))
EVENT_BY_URI = _CLIENT.events.get('/rest/EVENTS/24')
print("uri: '%s' | EVENTTypeID: '%s' \n" % (EVENT_BY_URI['uri'], EVENT_BY_URI['EVENTTypeID']))

# Filter by state
print("\nGet all EVENTS filtering by EVENTTypeID")
EVENTS = _CLIENT.events.get_all(filter="\"EVENTTypeID='StatusPoll.EnclosureStatus'\"", count=10)
for EVENT in EVENTS:
    print("uri: '%s' | EVENTTypeID: '%s'" % (EVENT['uri'], EVENT['EVENTTypeID']))
