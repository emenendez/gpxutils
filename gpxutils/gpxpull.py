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
    gpxutils.addArguments(parser)
    parser.add_argument('-p', '--pause', action='store_true', help='Prompt the user to press a key before exiting.')
    parser.add_argument('drive', nargs='+', type=Path, help='drive name of a USB-connected Garmin GPS')
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
