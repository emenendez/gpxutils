#!python3

from pathlib import Path, WindowsPath
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

    # Hack to create proper absolute drive paths on Windows
    if not drive.is_absolute() and isinstance(drive, WindowsPath):
        if len(str(drive)) == 1:
            drive = Path(str(drive) + ':/')
        elif len(str(drive)) == 2 and str(drive)[1] == ':':
            drive /= '/'

    gpxDir = drive / 'Garmin' / 'GPX'
    if gpxDir.exists():
        processFiles(gpxDir, **options)


def main():
    parser = gpxutils.ArgumentParser(description='Pull GPX files from GPSes, clean, and split.')
    parser.add_argument('-p', '--pause', action='store_true',
        help='prompt the user to press a key before exiting (default: %(default)s)')
    parser.add_argument('-g', '--gps', default=gpxutils.getDefault('gps'),
        help='GPSBabel input format; use \'usb\' for Garmin USB mass-storage GPSes (default: %(default)s)')
    parser.add_argument('drive', nargs='+', help='drive name of a mass-storage GPS, or GPSBabel input filename')
    args = parser.parse_args()

    if args.pause:
        import atexit
        atexit.register(lambda: input('\n[Press ENTER to exit]'))

    if args.prefix == str():
        args.prefix = input('File prefix: ')

    for drive in args.drive:
        gpxpull(drive=drive, split=args.split, output=args.output, output_time=args.time, output_name=args.name, max_filename_length=args.length,
                file_prefix=args.prefix, date=args.date, interactive=args.interactive, gps=args.gps)


if __name__ == "__main__":
    main()
