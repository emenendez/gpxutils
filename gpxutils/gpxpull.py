#!python3

from pathlib import Path, WindowsPath
import subprocess
import sys
import tempfile
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

    if options['gps'].lower() == 'usb':
        drive = Path(drive)

        # Hack to create proper absolute drive paths on Windows
        if not drive.is_absolute() and isinstance(drive, WindowsPath):
            if len(str(drive)) == 1:
                drive = Path(str(drive) + ':/')
            elif len(str(drive)) == 2 and str(drive)[1] == ':':
                drive /= '/'

        gpxDir = drive / 'Garmin' / 'GPX'
        if gpxDir.exists():
            processFiles(gpxDir, **options)

    else:
        # Create temporary file
        tempFile = tempfile.NamedTemporaryFile(delete=False)
        tempFile.close()
        tempFile = Path(tempFile.name)

        # Call gpsbabel to pull tracks and waypoints
        try:
            subprocess.check_call(['gpsbabel', '-t', '-w', '-i', options['gps'], '-f', drive, '-o', 'gpx', '-F', str(tempFile)])
        except Exception as e:
            raise e
        else:
            # Call gpxclean on temporary file
            gpxutils.gpxclean(tempFile, **options)
        finally:
            # Clean up tempfile
            tempFile.unlink()


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
        try:
            gpxpull(drive=drive, split=args.split, output=args.output, output_filename=args.filename, output_time=args.time, output_name=args.name, 
                    max_filename_length=args.length, file_prefix=args.prefix, date=args.date, interactive=args.interactive, gps=args.gps)
        except gpxutils.OutputDirectoryError as e:
            print('Error: could not create output directory {}'.format(e.filename), file=sys.stderr)
        except subprocess.CalledProcessError:
            print('Error: GPSBabel encountered an error', file=sys.stderr)
        except OSError:
            print('Error: could not find GPSBabel', file=sys.stderr)


if __name__ == "__main__":
    main()
