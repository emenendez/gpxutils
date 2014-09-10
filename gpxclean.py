#!/usr/local/bin/python3

import argparse
import gpxpy
import gpxpy.gpx
from pathlib import Path


SPLIT_DISTANCE = 300  # Split tracks if points are greater than 300m apart


parser = argparse.ArgumentParser(description='Clean GPX tracks and split into multiple files.')
parser.add_argument('input', nargs='+', help='a .gpx file to clean and split')
args = parser.parse_args()


def makePath(base_name, i):
    return Path('{} {:03d}.gpx'.format(base_name, i))

def createUniqueFile(base_name, time):
    i = 0
    file_name = base_name
    if time:
        file_name += ' ' + time.strftime('%Y-%m-%d %H.%M.%S')
    while makePath(file_name, i).exists():
        i += 1
    return makePath(file_name, i)

def writeAndCreateNewFile(segment, base_name):
    if segment is not None and segment.get_points_no() > 1:
        # Create new GPX file
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)

        # Add segment to our GPX track:
        track.segments.append(segment)
        
        time = segment.get_time_bounds().start_time
        outfile = createUniqueFile(base_name, time)
        with outfile.open('w') as output:
            output.write(gpx.to_xml())
    
    # Return a new segment
    return gpxpy.gpx.GPXTrackSegment()

def writeWaypoint(waypoint, base_name):
    if waypoint:
        # Create new GPX file
        gpx = gpxpy.gpx.GPX()

        # Append waypoint
        gpx.waypoints.append(waypoint)

        outfile = createUniqueFile(base_name + ' waypoint', waypoint.time)
        with outfile.open('w') as output:
            output.write(gpx.to_xml())


new_segment = None

for infile in args.input:
    infile = Path(infile)
    with infile.open() as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        # Extract tracks
        for track in gpx.tracks:
            for segment in track.segments:
                # Create new segment, and write out the current one
                new_segment = writeAndCreateNewFile(new_segment, infile.stem)

                previous_point = None
                for point in segment.points:
                    if previous_point:
                        if point.distance_2d(previous_point) > SPLIT_DISTANCE:
                            # Start new segment
                            new_segment = writeAndCreateNewFile(new_segment, infile.stem)
                            
                    previous_point = point
                    new_segment.points.append(point)
        # Write final segment
        writeAndCreateNewFile(new_segment, infile.stem)

        # Extract waypoints
        for waypoint in gpx.waypoints:
            writeWaypoint(waypoint, infile.stem)
