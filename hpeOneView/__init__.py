#!/usr/bin/env python
"""
HPE OneView Library
~~~~~~~~~~~~~~~~~~~~~

hpeOneView is a library for interfacing with HPE OneView Management Appliance.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

__title__ = 'hpeOneView'
__version__ = '6.2.0'
__copyright__ = '(C) Copyright (2012-2021) Hewlett Packard Enterprise Development LP'
__license__ = 'Apache'

###
# (C) Copyright [2021] Hewlett Packard Enterprise Development LP
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


import sys
import warnings

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)
if PY2:
    if PYTHON_VERSION < (2, 7, 9):
        warning_message = 'Running unsupported Python version: %s, unexpected errors might occur.'
        warning_message += ' Use of Python v2.7.9+ is advised.'
        warnings.warn(warning_message % '.'.join(map(str, PYTHON_VERSION)), Warning)
elif PYTHON_VERSION < (3, 4):
        warning_message = 'Running unsupported Python version> %s, unexpected errors might occur.'
        warning_message += ' Use of Python v3.4+ is advised.'
        warnings.warn(warning_message % '.'.join(map(str, PYTHON_VERSION)), Warning)

from hpeOneView.connection import *
from hpeOneView.exceptions import *

logging.getLogger(__name__).addHandler(logging.NullHandler())

sys.excepthook = handle_exceptions


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-a', '--appliance', dest='host', required=True,
                        help='HPE OneView Appliance hostname or IP')
    parser.add_argument('-u', '--user', dest='user', required=True,
                        help='HPE OneView Username')
    parser.add_argument('-p', '--pass', dest='passwd', required=True,
                        help='HPE OneView Password')
    parser.add_argument('-c', '--certificate', dest='cert', required=False,
                        help='Trusted SSL Certificate Bundle in PEM '
                             '(Base64 Encoded DER) Format')
    parser.add_argument('-r', '--proxy', dest='proxy', required=False,
                        help='Proxy (host:port format')
    args = parser.parse_args()
    con = connection(args.host)
    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)
    credential = {'userName': args.user, 'password': args.passwd}
    con.login(args.host, credential)
    con.logout()


if __name__ == '__main__':
    import sys
    import argparse

    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
