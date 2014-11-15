gpxutils
========

Tools for working with GPX files.

gpxclean
--------

Clean GPX tracks and split into multiple files.

gpxpull
-------

Pull files from modern Garmin GPSes, clean, and split. On Windows, with the help of the [USB Drive Letter Manager](http://www.uwe-sieber.de/usbdlm_e.html), gpxpull can automatically download and clean GPX files from a USB-connected Garmin GPS.

Usage
-----

```
$ gpxclean --help

usage: gpxclean.py [-h] [-s SPLIT] [-o OUTPUT] [-t] [-n] [-l LENGTH]
                   [-f [PREFIX]] [-d] [-i]
                   input [input ...]

Clean GPX tracks and split into multiple files.

positional arguments:
  input                 a .gpx file to clean and split

optional arguments:
  -h, --help            show this help message and exit
  -s SPLIT, --split SPLIT
                        Split tracks if points are greater than this distance
                        apart (meters).
  -o OUTPUT, --output OUTPUT
                        Directory to place output .gpx files.
  -t, --no-time         Do not use time in output filenames.
  -n, --name            Use track/waypoint name in output filenames.
  -l LENGTH, --max-filename-length LENGTH
                        Truncate output filename to this number of characters.
  -f [PREFIX], --prefix [PREFIX]
                        Add a prefix to all files, or prompt if none is
                        specified.
  -d, --date-directories
                        Put files in subdirectories by date.
  -i, --interactive     Prompt to save/discard each track.
```

```
$ gpxpull --help

usage: gpxpull.py [-h] [-s SPLIT] [-o OUTPUT] [-t] [-n] [-l LENGTH]
                  [-f [PREFIX]] [-d] [-i] [-p]
                  drive [drive ...]

Pull GPX files from modern Garmin GPSes, clean, and split.

positional arguments:
  drive                 drive name of a USB-connected Garmin GPS

optional arguments:
  -h, --help            show this help message and exit
  -s SPLIT, --split SPLIT
                        Split tracks if points are greater than this distance
                        apart (meters).
  -o OUTPUT, --output OUTPUT
                        Directory to place output .gpx files.
  -t, --no-time         Do not use time in output filenames.
  -n, --name            Use track/waypoint name in output filenames.
  -l LENGTH, --max-filename-length LENGTH
                        Truncate output filename to this number of characters.
  -f [PREFIX], --prefix [PREFIX]
                        Add a prefix to all files, or prompt if none is
                        specified.
  -d, --date-directories
                        Put files in subdirectories by date.
  -i, --interactive     Prompt to save/discard each track.
  -p, --pause           Prompt the user to press a key before exiting.
```

### Requirements

- [Python 3.4](https://www.python.org/) or newer
- [gpxpy](https://github.com/tkrajina/gpxpy)

### Installation

#### Windows

1. Install [Python 3.4](https://www.python.org/downloads/) or newer. Be sure to enable the "Add python.exe to Path" option.

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

gpxutils itself is cross-platform by default. It should be possible to automate GPS downloads with an AppleScrit Folder Action; contact me if you have success or would like to try.

#### Linux

gpxutils itself is cross-platform by default. It should be possible to automate GPS downloads with a udev script; contact me if you have success or would like to try.

### Changelog

#### 2.0.1

- Fixed packaging bug for uploading to PyPI

#### 2.0.0

- Added -f and -d options for more flexible file naming
- Removed nonsensical track name and track time options

#### 1.1.1

- Add -p option to pause for keypress after running gpxpull
