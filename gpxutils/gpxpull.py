#!python3

from pathlib import Path
import gpxutils


def processFiles(gpxDir, **options):
    gpxutils.applyDefaults(options)

    for file in gpxDir.iterdir():
        if file.is_dir():
            processFiles(file, **options)
        elif file.suffix.lower() == '.gpx':
            print(file)
            gpxutils.gpxclean(file, **options)


def gpxpull(drive, **options):
    gpxutils.applyDefaults(options)

    gpxDir = drive / 'Garmin' / 'GPX'
    if gpxDir.exists():
        processFiles(gpxDir, **options)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pull GPX files from modern Garmin GPSes, clean, and split.')
    parser.add_argument('-s', '--split', type=int, default=gpxutils.getDefault('split'), help='Split tracks if points are greater than this distance apart (meters).')
    parser.add_argument('-o', '--output', type=Path, default=gpxutils.getDefault('output'), help='Directory to place output .gpx files.')
    parser.add_argument('-t', '--no-time', action='store_false', dest='time', help='Do not use time in output filenames.')
    parser.add_argument('-n', '--name', action='store_true', dest='name', help='Use track/waypoint name in output filenames.')
    parser.add_argument('-l', '--max-filename-length', type=int, dest='length', default=gpxutils.getDefault('max_filename_length'), help='Truncate output filename to this number of characters.')
    parser.add_argument('-f', '--prefix', nargs='?', default=gpxutils.getDefault('file_prefix'), const=str(), help='Add a prefix to all files, or prompt if none is specified.')
    parser.add_argument('-d', '--date-directories', action='store_true', dest='date', help='Put files in subdirectories by date.')
    parser.add_argument('-i', '--interactive', action='store_true', dest='interactive', help='Prompt to save/discard each track.')
    parser.add_argument('-p', '--pause', action='store_true', help='Prompt the user to press a key before exiting.')
    parser.add_argument('drive', nargs='+', type=Path, help='drive name of a USB-connected Garmin GPS')
    parser.set_defaults(time=gpxutils.getDefault('output_time'), name=gpxutils.getDefault('output_name'), date=gpxutils.getDefault('date'), interactive=gpxutils.getDefault('interactive'))
    args = parser.parse_args()

    if args.pause:
        import atexit
        atexit.register(lambda: input('\nPress ENTER to exit...'))

    if args.prefix == str():
        args.prefix = input('File prefix: ')

    for drive in args.drive:
        gpxpull(drive=drive, split=args.split, output=args.output, output_time=args.time, output_name=args.name, max_filename_length=args.length,
                file_prefix=args.prefix, date=args.date, interactive=args.interactive)


if __name__ == "__main__":
    main()
