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

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "description": "This is a very simple test event",
    "serviceEventSource": "true",
    "serviceEventDetails": {
        "caseId": "1234",
        "primaryContact": "contactDetails",
        "remoteSupportState": "Submitted"
    },
    "severity": "OK",
    "healthCategory": "PROCESSOR",
    "eventTypeID": "hp.justATest",
    "rxTime": "2012-05-14T20:23:56.688Z",
    "urgency": "None",
    "eventDetails":
    [{"eventItemName": "ipv4Address",
        "eventItemValue": "198.51.100.5",
        "isThisVarbindData": "false",
        "varBindOrderIndex": -1}]
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

_client = OneViewClient(config)

# Getting the first 5 events
print("\nGetting the first 5 events:")
events = _client.events.get_all(0, 5)
for event in events:
    print("eventTypeID: '%s' | description: %s " % (event['description'], event['eventTypeID']))

# Create an Event
event = _client.events.create(options)
print("\nCreated event successfully.\n  uri = '%s'" % (event['uri']))

# Get by Uri
print("\nFind uri == %s" % (event['uri']))
event_by_uri = _client.events.get(event['uri'])
print("uri: '%s' | eventTypeID: '%s' \n" % (event_by_uri['uri'], event_by_uri['eventTypeID']))

# Filter by state
print("\nGet all events filtering by eventTypeID")
events = _client.events.get_all(filter="\"eventTypeID='StatusPoll.EnclosureStatus'\"", count=10)
for event in events:
    print("uri: '%s' | eventTypeID: '%s'" % (event['uri'], event['eventTypeID']))
