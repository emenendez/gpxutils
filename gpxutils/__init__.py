#!/usr/local/bin/python3

from pathlib import Path
import gpxutils.gpxclean as GC
import gpxutils.gpxpull as GP

gpxclean = GC.gpxclean
gpxpull = GP.gpxpull

_DEFAULTS = {
    'split': 300,
    'output': Path('.'),
    'output_time': True,
    'output_name': False,
    'max_filename_length': 50,
    'file_prefix': None,
    'date': False,
    'interactive': False,
}


def applyDefaults(options):
    defaults = dict(_DEFAULTS)
    defaults.update(options)
    options = defaults


def addArguments(parser):
    parser.add_argument('-s', '--split', type=int, default=_DEFAULTS.get('split'), help='Split tracks if points are greater than this distance apart (meters).')
    parser.add_argument('-o', '--output', type=Path, default=_DEFAULTS.get('output'), help='Directory to place output .gpx files.')
    parser.add_argument('-t', '--no-time', action='store_false', dest='time', help='Do not use time in output filenames.')
    parser.add_argument('-n', '--name', action='store_true', dest='name', help='Use track/waypoint name in output filenames.')
    parser.add_argument('-l', '--max-filename-length', type=int, dest='length', default=_DEFAULTS.get('max_filename_length'), help='Truncate output filename to this number of characters.')
    parser.add_argument('-f', '--prefix', nargs='?', default=_DEFAULTS.get('file_prefix'), const=str(), help='Add a prefix to all files, or prompt if none is specified.')
    parser.add_argument('-d', '--date-directories', action='store_true', dest='date', help='Put files in subdirectories by date.')
    parser.add_argument('-i', '--interactive', action='store_true', dest='interactive', help='Prompt to save/discard each track.')
    parser.set_defaults(time=_DEFAULTS.get('output_time'), name=_DEFAULTS.get('output_name'), date=_DEFAULTS.get('date'), interactive=_DEFAULTS.get('interactive'))
