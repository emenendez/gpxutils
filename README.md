gpxutils
========

gpxutils is a Python module and set of command-line tools to simplify working with GPSes and GPX files. It will help you automatically download GPS tracks and waypoints from a GPS device and clean up the files, making your GPS workflow much faster.

gpxclean
--------

Remove "tails" from GPX tracks and save each track as an individual file with flexible naming options.

gpxpull
-------

Pull files from GPSes, clean, and split. On Windows, with the help of the [USB Drive Letter Manager](http://www.uwe-sieber.de/usbdlm_e.html), gpxpull can automatically download and clean GPX files from a USB-connected Garmin GPS.

Usage
-----

```
$ gpxclean --help

usage: gpxclean [-h] [--version] [-s SPLIT] [-o OUTPUT] [-F] [-t] [-n]
                [-l LENGTH] [-f [PREFIX]] [-d] [-i]
                input [input ...]

Clean GPX tracks and split into multiple files.

positional arguments:
  input                 a .gpx file to clean and split

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s SPLIT, --split SPLIT
                        split tracks if points are greater than this many
                        meters apart; use 0 for no splitting (default: 300)
  -o OUTPUT, --output OUTPUT
                        directory to place output .gpx files (default: .)
  -F, --filename        use input filename in output filenames (default:
                        False)
  -t, --no-time         do not use time in output filenames (default: False)
  -n, --no-name         do not use track/waypoint name in output filenames
                        (default: False)
  -l LENGTH, --max-filename-length LENGTH
                        truncate output filename to this number of characters
                        (default: 50)
  -f [PREFIX], --prefix [PREFIX]
                        add a prefix to all files, or prompt if none is
                        specified (default: no prefix)
  -d, --date-directories
                        put files in subdirectories by date (default: False)
  -i, --interactive     prompt to save/discard each track (default: False)
```

```
$ gpxpull --help

usage: gpxpull [-h] [--version] [-s SPLIT] [-o OUTPUT] [-F] [-t] [-n]
               [-l LENGTH] [-f [PREFIX]] [-d] [-i] [-p] [-g GPS]
               drive [drive ...]

Pull GPX files from GPSes, clean, and split.

positional arguments:
  drive                 drive name of a mass-storage GPS, or GPSBabel input
                        filename

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s SPLIT, --split SPLIT
                        split tracks if points are greater than this many
                        meters apart; use 0 for no splitting (default: 300)
  -o OUTPUT, --output OUTPUT
                        directory to place output .gpx files (default: .)
  -F, --filename        use input filename in output filenames (default:
                        False)
  -t, --no-time         do not use time in output filenames (default: False)
  -n, --no-name         do not use track/waypoint name in output filenames
                        (default: False)
  -l LENGTH, --max-filename-length LENGTH
                        truncate output filename to this number of characters
                        (default: 50)
  -f [PREFIX], --prefix [PREFIX]
                        add a prefix to all files, or prompt if none is
                        specified (default: no prefix)
  -d, --date-directories
                        put files in subdirectories by date (default: False)
  -i, --interactive     prompt to save/discard each track (default: False)
  -p, --pause           prompt the user to press a key before exiting
                        (default: False)
  -g GPS, --gps GPS     GPSBabel input format; use 'usb' for Garmin USB mass-
                        storage GPSes (default: usb)
```

### Requirements

- [Python 3.4](https://www.python.org/) or newer
- [gpxpy](https://github.com/tkrajina/gpxpy)

### Installation

#### Windows

1. Install [Python 3.4](https://www.python.org/downloads/) or newer. Be sure to enable the "Add python.exe to Path" option. A reboot may be necessary after this step.

2. Install gpxutils from a Windows command prompt:  
   `pip3 install gpxutils`

3. Install the [USB Drive Letter Manager](http://www.uwe-sieber.de/usbdlm_e.html).

4. Create a new text file with the following contents and save it as `c:\Program Files\USBDLM\USBDLM.ini`:
   ```
[OnArrival1]
FileExists=%drive%\Garmin\GPX
open="gpxpull" -o "C:\GPX-out" %drive%
```

#### Mac

gpxutils itself is cross-platform by default. It should be possible to automate GPS downloads with an AppleScript Folder Action; contact me if you have success or would like to try.

#### Linux

gpxutils itself is cross-platform by default. It should be possible to automate GPS downloads with a udev script; contact me if you have success or would like to try.

### Changelog

#### 3.0.0

- Use GPSBabel to download tracks and waypoints from a variety of GPSes
- Change default file naming
- Fix interactive-mode errors from tracks and waypoints without times

#### 2.0.4

- Fixed relative path bug on Windows
- Allow drive letters without trailing ':' on Windows

#### 2.0.3

- Display default options in help message
- Add version message

#### 2.0.2

- Workaround for trailing quote in output path
- Better output path error handling

#### 2.0.1

- Fixed packaging bug for uploading to PyPI

#### 2.0.0

- Added -f and -d options for more flexible file naming
- Removed nonsensical track name and track time options

#### 1.1.1

- Add -p option to pause for keypress after running gpxpull
