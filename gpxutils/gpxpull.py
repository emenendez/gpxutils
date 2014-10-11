#!python3

from pathlib import Path
import gpxutils.gpxclean


class _DEFAULTS:
    split = 300
    output = Path('.')
    output_time = True
    output_name = False
    max_filename_length = 50


def processFiles(gpxDir, split=_DEFAULTS.split, output=_DEFAULTS.output, output_time=_DEFAULTS.output_time,
                 output_name=_DEFAULTS.output_name, max_filename_length=_DEFAULTS.max_filename_length):
    for file in gpxDir.iterdir():
        if file.is_dir():
            processFiles(file, split, output, output_time, output_name, max_filename_length)
        elif file.suffix.lower() == '.gpx':
            print(file)
            gpxutils.gpxclean.gpxclean(file, split, output, output_time, output_name, max_filename_length)


def gpxpull(drive, split=_DEFAULTS.split, output=_DEFAULTS.output, output_time=_DEFAULTS.output_time,
            output_name=_DEFAULTS.output_name, max_filename_length=_DEFAULTS.max_filename_length):
    gpxDir = drive / 'Garmin' / 'GPX'
    if gpxDir.exists():
        processFiles(gpxDir, split, output, output_time, output_name, max_filename_length)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Pull GPX files from modern Garmin GPSes, clean, and split.')
    parser.add_argument('-s', '--split', type=int, default=_DEFAULTS.split, help='Split tracks if points are greater than this distance apart (meters).')
    parser.add_argument('-o', '--output', type=Path, default=_DEFAULTS.output, help='Directory to place output .gpx files.')
    parser.add_argument('-T', '--time', action='store_true', dest='time', help='Use time in output filenames (default).')
    parser.add_argument('-t', '--no-time', action='store_false', dest='time', help='Do not use time in output filenames.')
    parser.add_argument('-N', '--name', action='store_true', dest='name', help='Use track/waypoint name in output filenames.')
    parser.add_argument('-n', '--no-name', action='store_false', dest='name', help='Do not use track/waypoint name in output filenames (default).')
    parser.add_argument('-l', '--max-filename-length', type=int, dest='length', default=_DEFAULTS.max_filename_length, help='Warn if output filename is longer than this number of characters.')
    parser.add_argument('drive', nargs='+', type=Path, help='drive name of a USB-connected Garmin GPS')
    parser.set_defaults(time=_DEFAULTS.output_time, name=_DEFAULTS.output_name)
    args = parser.parse_args()

    for drive in args.drive:
        gpxpull(drive=drive, split=args.split, output=args.output, output_time=args.time, output_name=args.name, max_filename_length=args.length)
        