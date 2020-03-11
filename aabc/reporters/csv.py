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

import csv


class CSVReporter:
    '''
    Handles reporting of Android App Bundle usage in CSV format.

    Stores tuples of Android app IDs and booleans indicating whether or not
    Android App Bundles are used.
    '''
    def __init__(self, report_path):
        report_file = open(report_path, 'w')
        self.writer = csv.writer(report_file)

    def report_app(self, appid, uses_aab):
        '''
        Stores app ID and whether it uses_aab in the report file.
        '''
        self.writer.writerow([appid, 1 if uses_aab else 0])
