#!/usr/local/bin/python3

from pathlib import Path
import gpxutils.gpxclean as GC
import gpxutils.gpxpull as GP

gpxclean = GC.gpxclean
gpxpull = GP.gpxpull

__version__ = '2.1.0'

_DEFAULTS = {
    'split': 300,
    'output': Path('.'),
    'output_time': True,
    'output_name': False,
    'max_filename_length': 50,
    'file_prefix': None,
    'date': False,
    'interactive': False,
    'gps': 'usb',
}


class OutputDirectoryError(OSError):
    def __init__(self, filename):
        self.filename = filename


def _getPrefixDefault():
    if _DEFAULTS.get('file_prefix') is None:
        return 'no prefix'
    elif _DEFAULTS.get('file_prefix') == str():
        return 'prompt'
    else:
        return _DEFAULTS.get('file_prefix')


def getDefault(option):
    return _DEFAULTS.get(option)


def applyDefaults(options):
    defaults = dict(_DEFAULTS)
    defaults.update(options)
    options = defaults


def ArgumentParser(description):
    import argparse

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--version', action='version', version='gpxutils {}'.format(__version__))
    parser.add_argument('-s', '--split', type=int, default=getDefault('split'),
        help='split tracks if points are greater than this many meters apart; use 0 for no splitting (default: %(default)d)')
    parser.add_argument('-o', '--output', type=Path, default=getDefault('output'),
        help='directory to place output .gpx files (default: %(default)s)')
    parser.add_argument('-t', '--no-time', action='store_false', dest='time',
        help='do not use time in output filenames (default: {})'.format(not getDefault('output_time')))
    parser.add_argument('-n', '--name', action='store_true', dest='name',
        help='use track/waypoint name in output filenames (default: %(default)s)')
    parser.add_argument('-l', '--max-filename-length', type=int, dest='length', default=getDefault('max_filename_length'),
        help='truncate output filename to this number of characters (default: %(default)d)')
    parser.add_argument('-f', '--prefix', nargs='?', default=getDefault('file_prefix'), const=str(),
        help='add a prefix to all files, or prompt if none is specified (default: {})'.format(_getPrefixDefault()))
    parser.add_argument('-d', '--date-directories', action='store_true', dest='date',
        help='put files in subdirectories by date (default: %(default)s)')
    parser.add_argument('-i', '--interactive', action='store_true', dest='interactive',
        help='prompt to save/discard each track (default: %(default)s)')
    parser.set_defaults(time=getDefault('output_time'), name=getDefault('output_name'),
        date=getDefault('date'), interactive=getDefault('interactive'))

    return parser
