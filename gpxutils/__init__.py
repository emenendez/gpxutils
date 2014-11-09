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


def getDefault(option):
    if option in _DEFAULTS:
        return _DEFAULTS[option]
    else:
        return None


def applyDefaults(options):
    defaults = dict(_DEFAULTS)
    defaults.update(options)
    options = defaults
