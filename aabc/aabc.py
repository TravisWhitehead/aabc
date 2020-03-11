#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
aabc
Copyleft (C) 2020 TravisWhitehead

aabc heavily uses code from gplaycli https://github.com/matlink/gplaycli
Copyleft (C) 2015 Matlink

gplaycli is hardly based on GooglePlayDownloader https://framagit.org/tuxicoman/googleplaydownloader
Copyright (C) 2013 Tuxicoman

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

import argparse
import configparser
import enum
import logging
import os
import pprint
import sys

from gpapi.googleplay import GooglePlayAPI, LoginError, RequestError
from pkg_resources import get_distribution, DistributionNotFound

from . import hooks
from .reporters.csv import CSVReporter

try:
    import keyring
    HAVE_KEYRING = True
except ImportError:
    HAVE_KEYRING = False

# Set up logger that prints logging level per message
logger = logging.getLogger(__name__)  # default level is WARNING
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.propagate = False


class ERRORS(enum.IntEnum):
    """
    Contains constant errors
    """
    SUCCESS = 0
    KEYRING_NOT_INSTALLED = 10
    CANNOT_LOGIN_GPLAY = 15


try:
    __version__ = '%s [Python%s] ' % (get_distribution('aabc').version, sys.version.split()[0])
except DistributionNotFound:
    __version__ = 'unknown: aabc not installed (version in setup.py)'


class aabchecker:
    def __init__(self, args=None, config_file=None):
        if config_file is None:
            config_file_paths = [
                'aabc.conf',
                os.path.expanduser('~') + '/.config/aabc/aabc.conf',
                '/etc/aabc/aabc.conf'
            ]
            for path in config_file_paths:
                if os.path.isfile(path):
                    config_file = path
                    break
            if config_file is None:
                logger.warn('No configuration files found at %s, using default values')

        self.gpapi = None

        config = configparser.ConfigParser()
        if config_file:
            config.read(config_file)

        self.gmail_address = config.get('Credentials', 'gmail_address', fallback=None)
        self.gmail_password = config.get('Credentials', 'gmail_password', fallback=None)
        self.keyring_service = config.get('Credentials', 'keyring_service', fallback=None)

        self.device_codename = config.get('Device', 'codename', fallback='bacon')

        self.locale = config.get('Locale', 'locale', fallback='en_US')
        self.timezone = config.get('Locale', 'timezone', fallback='UTC')

        if not args:
            return

        if args.report_file is not None:
            self.reporter = CSVReporter(args.report_file)

        if args.verbose is not None:
            self.verbose = args.verbose

        if self.verbose:
            logger.setLevel(logging.INFO)
        logger.info('aabc version %s', __version__)
        logger.info('Configuration file is %s', config_file)

        if args.device_codename is not None:
            self.device_codename = args.device_codename

    # TODO: Support multiple apps to check with BulkDetails
    @hooks.connected
    def check_aab(self, app):
        '''
        Return whether app uses Android App Bundles.

        Queries Google Play Store for details about app and checks the file
        list; reports that Android App Bundles are used when more than one
        file is listed.
        '''

        try:
            details = self.gpapi.details(app)
            files = details['details']['appDetails']['file']
            num_files = len(files)

            if self.verbose:
                files_list = pprint.pformat(files)
                logger.info(str(num_files) + ' files found for ' + details['docid'] + ':\n'
                            + files_list)

            return num_files > 1
        except RequestError as request_error:
            logger.error('Failed to get details for app.')
            logger.error(request_error)

    def connect(self):
        '''
        Connect aabc to the Google Play API. Credentials might be stored into
        the keyring if the keyring package is installed.
        '''
        self.gpapi = GooglePlayAPI(locale=self.locale, timezone=self.timezone,
                                   device_codename=self.device_codename)
        ok, err = self.connect_credentials()
        if ok:
            self.token = self.gpapi.authSubToken
            self.gsfid = self.gpapi.gsfId
        return ok, err

    def connect_credentials(self):
        logger.info('Using credentials to connect to API')
        if self.gmail_password:
            logger.info('Using plaintext password')
            password = self.gmail_password
        elif self.keyring_service and HAVE_KEYRING:
            password = keyring.get_password(self.keyring_service, self.gmail_address)
        elif self.keyring_service and not HAVE_KEYRING:
            logger.error('You asked for keyring service but keyring package is not installed')
            return False, ERRORS.KEYRING_NOT_INSTALLED
        else:
            logger.error('No password found. Check your configuration file.')
            return False, ERRORS.CANNOT_LOGIN_GPLAY
        try:
            self.gpapi.login(email=self.gmail_address, password=password)
        except LoginError as e:
            logger.error('Bad authentication, login or password incorrect (%s)', e)
            return False, ERRORS.CANNOT_LOGIN_GPLAY
        return True, None


def main():
    parser = argparse.ArgumentParser(description='A tool for checking if apps on the Google Play \
                                     Store use Android App Bundles')
    parser.add_argument('apps', nargs='*', help='Apps to check if using Android App Bundles')
    parser.add_argument('-C', '--config', help='Use a different config file than gplaycli.conf',
                        metavar='CONF_FILE', nargs=1)
    parser.add_argument('-dc', '--device-codename', help='The device codename to fake',
                        choices=GooglePlayAPI.getDevicesCodenames(), metavar='DEVICE_CODENAME')
    parser.add_argument('-r', '--report-file', help='The file to write the report to')
    parser.add_argument('-v', '--verbose', help='Be verbose', action='store_true')
    parser.add_argument('-V', '--version', help='Print version and exit', action='store_true')

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if len(args.apps) == 0:
        logger.error('Must specify at least one app to check.')
        return 1

    checker = aabchecker(args, args.config)

    checker.reporter.report_app(args.apps[0], checker.check_aab(args.apps[0]))
