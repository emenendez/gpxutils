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

usage: gpxcleant.py [-h] [-s SPLIT] [-o OUTPUT] [-T] [-t] [-N] [-n]
                    [-l LENGTH]
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
  -T, --time            Use time in output filenames (default).
  -t, --no-time         Do not use time in output filenames.
  -N, --name            Use track/waypoint name in output filenames.
  -n, --no-name         Do not use track/waypoint name in output filenames
                        (default).
  -l LENGTH, --max-filename-length LENGTH
                        Truncate output filename to this number of characters.
```

```
$ gpxpull --help

usage: gpxpull.py [-h] [-s SPLIT] [-o OUTPUT] [-T] [-t] [-N] [-n]
                  [-l LENGTH] [-p]
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
  -T, --time            Use time in output filenames (default).
  -t, --no-time         Do not use time in output filenames.
  -N, --name            Use track/waypoint name in output filenames.
  -n, --no-name         Do not use track/waypoint name in output filenames
                        (default).
  -l LENGTH, --max-filename-length LENGTH
                        Truncate output filename to this number of characters.
  -p, --pause           Prompt the user to press a key before exiting.
```

### Requirements

- [Python 3.4](https://www.python.org/) or newer
- [gpxpy](https://github.com/tkrajina/gpxpy)

### Installation

1. Install [Python 3.4](https://www.python.org/downloads/) or newer.

2. Install gpxutils from a command prompt:  
   `pip3 install git+https://github.com/emenendez/gpxutils.git`

3. Install the [USB Drive Letter Manager](http://www.uwe-sieber.de/usbdlm_e.html).

4. Add the following to the end of `c:\Program Files\USBDLM\USBDLM.ini`:
   ```
[OnArrival1]
FileExists=%drive%\Garmin\GPX
open="gpxpull" -o "C:\GPX-out\" %drive%
```
