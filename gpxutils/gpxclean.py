#!/usr/local/bin/python3

import gpxpy
import gpxpy.gpx
from datetime import datetime
from pathlib import Path
import string
import sys
import gpxutils


def prompt(copy, time):
    default = time.date() == datetime.now().date()
    answer = input('Save {}? [{}] '.format(copy, 'Y/n' if default else 'y/N'))
    answer = answer.strip().lower()
    if answer == str():
        return default
    elif answer[0] == 'y':
        return True
    elif answer[0] == 'n':
        return False
    else:
        return default

def makePath(base_dir, base_name, i, **options):
    gpxutils.applyDefaults(options)

    # Hack: remove trailing double-quote if present
    if base_dir.name.endswith('"'):
        base_dir = base_dir.with_name(base_dir.name[:-1])

    # Create output directory if possible
    try:
        if not base_dir.exists():
            base_dir.mkdir(parents=True)
        if not base_dir.is_dir():
            raise Exception
    except Exception:
        print('Error: could not create output directory {}'.format(base_dir), file=sys.stderr)
        exit()

    if i == 0:
        if options['max_filename_length'] != 0:
            base_name = base_name[0:options['max_filename_length'] - 4]
        return base_dir / '{}.gpx'.format(base_name)
    else:
        if options['max_filename_length'] != 0:
            base_name = base_name[0:options['max_filename_length'] - 8]
        return base_dir / '{}_{:03d}.gpx'.format(base_name, i)

def createUniqueFile(base_name, name_postfix, time=None, name=None, **options):
    gpxutils.applyDefaults(options)

    i = 0
    if options['file_prefix'] is not None:
        file_name = options['file_prefix']
    else:
        file_name = base_name
    file_name += '_' + name_postfix
    if options['output_time'] and time:
        file_name += '_' + time.strftime('%Y-%m-%d %H.%M.%S')
    if options['output_name'] and name:
        file_name += '_' + name
    
    # Create valid filename
    file_name = file_name.replace('(', '').replace(')', '')  # Remove parens
    valid_chars = '-_. {}{}'.format(string.ascii_letters, string.digits)
    file_name = ''.join(c if c in valid_chars else '-' for c in file_name)

    output = options['output']
    if options['date']:
        if time:
            output /= time.strftime('%Y-%m-%d')
        else:
            output /= 'unknown date'

    while makePath(output, file_name, i, **options).exists():
        i += 1

    return makePath(output, file_name, i, **options)
    
def writeAndCreateNewFile(segment, base_name, track_name=None, **options):
    gpxutils.applyDefaults(options)

    if segment is not None and segment.get_points_no() > 1:
        # Create new GPX file
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        track = gpxpy.gpx.GPXTrack(name=track_name)
        gpx.tracks.append(track)

        # Add segment to our GPX track:
        track.segments.append(segment)
        
        time = segment.get_time_bounds().start_time

        keep = (not options['interactive']) or prompt('track {} from {}.gpx @ {}'.format(track_name, base_name, time.strftime('%Y-%m-%d %H:%M')), time)
        if keep:
            outfile = createUniqueFile(base_name, 'trk', time, track_name, **options)
            with outfile.open('w') as output:
                output.write(gpx.to_xml())
        
    # Return a new segment
    return gpxpy.gpx.GPXTrackSegment()

def writeWaypoint(waypoint, base_name, **options):
    gpxutils.applyDefaults(options)

    if waypoint:
        # Create new GPX file
        gpx = gpxpy.gpx.GPX()

        # Append waypoint
        gpx.waypoints.append(waypoint)

        keep = (not options['interactive']) or prompt('waypoint {} from {}.gpx @ {}'.format(waypoint.name, base_name, waypoint.time.strftime('%Y-%m-%d %H:%M')), waypoint.time)
        if keep:
            outfile = createUniqueFile(base_name, 'wpt', waypoint.time, waypoint.name, **options)
            with outfile.open('w') as output:
                output.write(gpx.to_xml())


def gpxclean(input, **options):
    gpxutils.applyDefaults(options)

    new_segment = None
    current_track_name = None

    with input.open(encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        # Extract tracks
        for track in gpx.tracks:
            for segment in track.segments:
                # Create new segment, and write out the current one
                new_segment = writeAndCreateNewFile(new_segment, input.stem, current_track_name, **options)
                current_track_name = track.name

                previous_point = None
                for point in segment.points:
                    if previous_point:
                        if point.distance_2d(previous_point) > options['split']:
                            # Start new segment
                            new_segment = writeAndCreateNewFile(new_segment, input.stem, current_track_name, **options)
                            
                    previous_point = point
                    new_segment.points.append(point)
        # Write final segment
        new_segment = writeAndCreateNewFile(new_segment, input.stem, current_track_name, **options)

        # Extract waypoints
        for waypoint in gpx.waypoints:
            writeWaypoint(waypoint, input.stem, **options)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Clean GPX tracks and split into multiple files.')
    gpxutils.addArguments(parser)
    parser.add_argument('input', nargs='+', type=Path, help='a .gpx file to clean and split')
    args = parser.parse_args()

    if args.prefix == str():
        args.prefix = input('File prefix: ')

    for infile in args.input:
        gpxclean(input=infile, split=args.split, output=args.output, output_time=args.time, output_name=args.name, max_filename_length=args.length,
                 file_prefix=args.prefix, date=args.date, interactive=args.interactive)


if __name__ == "__main__":
    main()
