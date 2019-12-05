#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys


def app_uses_aab(device_serial, app):
    """Return whether app uses Android App Bundles."""

    if not app:
        error('Cannot call app_uses_aab() with empty app argument.', 5)

    command = ['pm', 'path', app]
    output = run_command_on_device(device_serial, command).stdout.decode('utf-8')
    paths = output.splitlines()

    # Check that these are APK paths just in case
    for path in paths:
        if not path.endswith('.apk'):
            print(output)
            error('pm returned something other than path(s) to APK(s). See output above.', 4)

    return len(paths) > 1

def check_adb_installed():
    """Exit with error if adb is not in PATH."""

    if shutil.which('adb') is None:
        error('adb not found. adb must be installed and in your PATH. adb is available in '
              'Android SDK Platform-Tools. See '
              'https://developer.android.com/studio/releases/platform-tools', 3)


def error(message, exit_status):
    """Print message to stderr and exit with exit_status."""

    print(message, file=sys.stderr)
    sys.exit(exit_status)


def get_app_list(device_serial, third_party_apps_only=False):
    """Return list of app names that are installed on a device."""

    command = ['pm', 'list', 'packages']
    if third_party_apps_only:
        command.append('-3')

    output = run_command_on_device(device_serial, command)
    apps = output.stdout.decode('utf-8').splitlines()
    apps = map(lambda line: line.replace('package:', ''), apps)

    return apps


def get_app_types(device_serial, apps):
    """Return list of pairs of app names and whether they use Android App Bundles."""

    app_types = []
    for app in apps:
        app_types.append((app, app_uses_aab(device_serial, app)))

    return app_types


def parse_arguments():
    """Returns parsed CLI arguments"""

    parser = argparse.ArgumentParser(
        description='Output list of Android apps installed on devices that use Android App '
        'Bundles (default) or are monolithic.')

    parser.add_argument(
        'device_serial', nargs='+', help='Serial(s) of device(s) to check (from "adb devices" '
        'output)')

    parser.add_argument(
        '-3', '--third-party-apps-only', action='store_true', help='Only check if third-party '
        'apps use Android App Bundles')

    exclusive = parser.add_mutually_exclusive_group()
    exclusive.add_argument(
        '-a', '--output-aab', action='store_const', dest='output_type', const='aab',
        default='aab', help='Output list of packages that use Android App Bundles')

    exclusive.add_argument(
        '-m', '--output-monolithic', action='store_const', dest='output_type', const='monolithic',
        help='Output list of packages that are monolithic (not using Android App Bundles)')

    return parser.parse_args()


def run_command_on_device(device_serial, command):
    """Run shell command on device."""

    try:
        output = subprocess.run(['adb', '-s', device_serial, 'shell'] + command,
                                capture_output=True, check=True)

    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr.decode('utf-8'))
        sys.exit(e.returncode)

    return output


def main():
    args = parse_arguments()

    check_adb_installed()

    for device in args.device_serial:
        apps = get_app_list(device, args.third_party_apps_only)
        app_types = get_app_types(device, apps)

        for app, app_type in app_types:
            if args.output_type == 'aab' and app_type:
                print(app)
            if args.output_type == 'monolithic' and not app_type:
                print(app)

    sys.exit(0)


if __name__ == '__main__':
    main()
