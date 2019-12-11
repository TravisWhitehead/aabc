# aabc: Android App Bundle Checker

aabc is a utility that checks whether Android apps on a device were built using Android
App Bundles (AAB) or whether they're monolithic APKs. This script calls ADB to gather
this information and can output lists of apps built with AAB.

## Requirements

[Android Debug Bridge (`adb`)](https://developer.android.com/studio/command-line/adb) is required
to run aabc. ADB is a part of [Android SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools.html).

## Usage
If you find that the usage instructions below are unclear or inaccurate, please [open an issue](https://github.com/TravisWhitehead/aabc/issues/new).

### Connecting Android Device(s) with adb
1) [Enable developer options and USB debugging on your Android device(s).](https://developer.android.com/studio/debug/dev-options#enable)
2) Connect Android device(s) to your computer via USB.
3) Run `adb devices` and note the serial of the target device (the output in the left column).
    - A pop-up may appear on your device asking you to allow the connection. Allow it.

### Running aabc


Specify the devices you want to check by passing their serials (from step 3 above) to aabc:
```sh
# Check device with serial "FOBAR1234"
aabc FOOBAR1234

# Check multiple devices by passing multiple serials
aabc FOOBAR1234 HELLOWORLD12
```

By default, aabc will list apps that are built using Android App Bundles. This preference can be
specified explicitly by passing `-a` (this does the same as the above example):
```sh
aabc -a FOOBAR1234
```

You can do the opposite and output apps that don't use Android App Bundles (monolithic apps) with `-m`:
```sh
aabc -m FOOBAR1234
```

To filter out system apps that you might not care about checking, pass `-3` to look at third-party
apps only:
```sh
aabc -3 FOOBAR1234
```

See an overview of available options and usage information:
```sh
$ aabc -h

usage: aabc [-h] [-3] [-a | -m] device_serial [device_serial ...]

Output list of Android apps installed on devices that use Android App Bundles
(default) or are monolithic.

positional arguments:
  device_serial         Serial(s) of device(s) to check (from "adb devices"
                        output)

optional arguments:
  -h, --help            show this help message and exit
  -3, --third-party-apps-only
                        Only check if third-party apps use Android App Bundles
  -a, --output-aab      Output list of packages that use Android App Bundles
  -m, --output-monolithic
                        Output list of packages that are monolithic (not using
                        Android App Bundles)
```
