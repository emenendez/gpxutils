gpxutils
========

Tools for working with GPX files.

gpxclean
--------

Clean GPX tracks and split into multiple files.

gpxpull
-------

Pull files from modern Garmin GPSes, clean, and split.

Usage
-----

### Requirements

- Python 3.4 or greater

### Installation

	pip install git+https://github.com/emenendez/gpxutils.git

### Windows

gpxpull can be used to automatically download and clean GPX files from a USB-connected Garmin GPS with the help of the [USB Drive Letter Manager](http://www.uwe-sieber.de/usbdlm_e.html).

Add the following to your USBDLM.ini:

	[OnArrival1]
	FileExists=%drive%\Garmin\GPX
	open=gpxpull -o "C:\GPX-out\" %drive%
