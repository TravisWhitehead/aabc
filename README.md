# aabc: Android App Bundle Checker

aabc is a utility that checks whether Android apps are published using Android App Bundles (AAB) or as monolithic APKs.
aabc takes app IDs and queries Google Play APIs to determine AAB usage based on file counts.

## Usage
If you find that the usage instructions below are unclear or inaccurate, please [open an issue](https://github.com/TravisWhitehead/aabc/issues/new).
This may not be kept very up to date while under rapid development.

Run `aabc -h` to see an overview of available options and usage information:
```sh
$ aabc -h

usage: aabc [-h] [-c CONF_FILE] [-dc DEVICE_CODENAME] [-i INPUT_FILE]
            [-r REPORT_FILE] [-v] [-V]
            [apps [apps ...]]

A tool for checking if apps on the Google Play Store use Android App Bundles

positional arguments:
  apps                  Apps to check if using Android App Bundles

optional arguments:
  -h, --help            show this help message and exit
  -c CONF_FILE, --config CONF_FILE
                        Use a different config file than gplaycli.conf
  -dc DEVICE_CODENAME, --device-codename DEVICE_CODENAME
                        The device codename to fake
  -i INPUT_FILE, --input-file INPUT_FILE
                        File containing a list of app IDs to check if using
                        Android App Bundles
  -r REPORT_FILE, --report-file REPORT_FILE
                        The file to write the report to
  -v, --verbose         Be verbose
  -V, --version         Print version and exit
```

### Check Apps on Your Device via ADB
The original version of this project used ADB to check for AAB usage with the apps installed on a device connected to your computer.
See release [v0.1.2](https://github.com/TravisWhitehead/aabc/tree/v0.1.2) for this use case.

## Thanks
* to https://github.com/NoMore201/googleplay-api for querying Google Play
* to https://github.com/matlink/gplaycli for some borrowed code & examples of gpapi usage
