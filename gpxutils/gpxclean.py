import gpxpy
import gpxpy.gpx
from pathlib import Path
import string
import sys


class _DEFAULTS:
    split = 300
    output = Path('.')
    output_time = True
    output_name = False
    max_filename_length = 50


def makePath(base_dir, base_name, i):
    if not base_dir.exists():
        base_dir.mkdir(parents=True)

    if i == 0:
        return base_dir / '{}.gpx'.format(base_name)
    else:
        return base_dir / '{}_{:03d}.gpx'.format(base_name, i)

def createUniqueFile(base_name, time=None, name=None, output=_DEFAULTS.output, output_time=_DEFAULTS.output_time,
                     output_name=_DEFAULTS.output_name, max_filename_length=_DEFAULTS.max_filename_length):
    i = 0
    file_name = base_name
    if output_time and time:
        file_name += '_' + time.strftime('%Y-%m-%d %H.%M.%S')
    if output_name and name:
        file_name += '_' + name
    
    # Create valid filename
    file_name = file_name.replace('(', '').replace(')', '')  # Remove parens
    valid_chars = '-_. {}{}'.format(string.ascii_letters, string.digits)
    file_name = ''.join(c if c in valid_chars else '-' for c in file_name)

    while makePath(output, file_name, i).exists():
        i += 1

    file_name = makePath(output, file_name, i)
    if max_filename_length != 0 and len(str(file_name)) > max_filename_length:
        print('Warning: {} greater than {} characters.'.format(file_name, max_filename_length), file=sys.stderr)

    return file_name

def writeAndCreateNewFile(segment, base_name, track_name=None, output=_DEFAULTS.output, output_time=_DEFAULTS.output_time,
                          output_name=_DEFAULTS.output_name, max_filename_length=_DEFAULTS.max_filename_length):
    if segment is not None and segment.get_points_no() > 1:
        # Create new GPX file
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        track = gpxpy.gpx.GPXTrack(name=track_name)
        gpx.tracks.append(track)

        # Add segment to our GPX track:
        track.segments.append(segment)
        
        time = segment.get_time_bounds().start_time
        outfile = createUniqueFile(base_name + '_track', time, track_name, output, output_time, output_name, max_filename_length)
        with outfile.open('w') as output:
            output.write(gpx.to_xml())
    
    # Return a new segment
    return gpxpy.gpx.GPXTrackSegment()

def writeWaypoint(waypoint, base_name, output=_DEFAULTS.output, output_time=_DEFAULTS.output_time,
                  output_name=_DEFAULTS.output_name, max_filename_length=_DEFAULTS.max_filename_length):
    if waypoint:
        # Create new GPX file
        gpx = gpxpy.gpx.GPX()

        # Append waypoint
        gpx.waypoints.append(waypoint)

        outfile = createUniqueFile(base_name + '_waypoint', waypoint.time, waypoint.name, output_time, output_name, max_filename_length)
        with outfile.open('w') as output:
            output.write(gpx.to_xml())


def gpxclean(input, split=_DEFAULTS.split, output=_DEFAULTS.output, output_time=_DEFAULTS.output_time,
             output_name=_DEFAULTS.output_name, max_filename_length=_DEFAULTS.max_filename_length):
    new_segment = None
    current_track_name = None

    with input.open(encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        # Extract tracks
        for track in gpx.tracks:
            for segment in track.segments:
                # Create new segment, and write out the current one
                new_segment = writeAndCreateNewFile(new_segment, infile.stem, current_track_name, output, output_time, output_name, max_filename_length)
                current_track_name = track.name

                previous_point = None
                for point in segment.points:
                    if previous_point:
                        if point.distance_2d(previous_point) > split:
                            # Start new segment
                            new_segment = writeAndCreateNewFile(new_segment, infile.stem, current_track_name, output, output_time, output_name, max_filename_length)
                            
                    previous_point = point
                    new_segment.points.append(point)
        # Write final segment
        new_segment = writeAndCreateNewFile(new_segment, infile.stem, current_track_name, output, output_time, output_name, max_filename_length)

        # Extract waypoints
        for waypoint in gpx.waypoints:
            writeWaypoint(waypoint, infile.stem, output, output_time, output_name, max_filename_length)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Clean GPX tracks and split into multiple files.')
    parser.add_argument('-s', '--split', type=int, default=_DEFAULTS.split, help='Split tracks if points are greater than this distance apart (meters).')
    parser.add_argument('-o', '--output', type=Path, default=_DEFAULTS.output, help='Directory to place output .gpx files.')
    parser.add_argument('-T', '--time', action='store_true', dest='time', help='Use time in output filenames (default).')
    parser.add_argument('-t', '--no-time', action='store_false', dest='time', help='Do not use time in output filenames.')
    parser.add_argument('-N', '--name', action='store_true', dest='name', help='Use track/waypoint name in output filenames.')
    parser.add_argument('-n', '--no-name', action='store_false', dest='name', help='Do not use track/waypoint name in output filenames (default).')
    parser.add_argument('-l', '--max-filename-length', type=int, dest='length', default=_DEFAULTS.max_filename_length, help='Warn if output filename is longer than this number of characters.')
    parser.add_argument('input', nargs='+', type=Path, help='a .gpx file to clean and split')
    parser.set_defaults(time=_DEFAULTS.output_time, name=_DEFAULTS.output_name)
    args = parser.parse_args()

    for infile in args.input:
        gpxclean(input=infile, split=args.split, output=args.output, output_time=args.time, output_name=args.name, max_filename_length=args.length)
        