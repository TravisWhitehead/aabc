#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyleft (C) 2020 TravisWhitehead

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

def get_files_from_details(details):
    '''Get file dictionary from GooglePlayAPI.details() response.

    Accepts a details dictionary produced by GooglePlayAPI.details() or
    GooglePlayAPI.bulkDetails() and returns the list of files or None if
    details is None.

    Args:
        details (dict): details dictionary produced by GooglePlayAPI.details()
            or GooglePlayAPI.bulkDetails()

    Returns:
        list of files from the details dictionary
    '''
    if details is None:
        return None
    else:
        return details['details']['appDetails']['file']

def get_apps_from_input_file(input_file):
    '''Get list of app IDs from input file listing one app ID per line.

    Args:
        input_file (str): path to file containing one app ID per line

    Returns:
        list of app IDs read from input_file or an empty list if input_file is None
    '''
    if input_file is not None:
        with open(input_file) as f:
            apps = f.read().splitlines()
            return apps
    return []
