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

    def write(self, data):
        '''Write AAB usage data to report file in CSV format.

        Iterate over data and write a row to report file for each entry where
        the first colun is the Android app ID and the second column is 1 or 0
        depending on whether the app uses Android App Bundles.

        Args:
            data (list): list of 2-tuples containing Android app IDs and
                boolean indicating whether AAB is used by the app.
        '''
        # Convert booleans to 1s and  0s
        data = map(lambda pair: (pair[0], 1 if pair[1] else 0), data)

        self.writer.writerows(data)
