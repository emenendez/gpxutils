#!/usr/local/bin/python3

import argparse
import gpxpy
import gpxpy.gpx
from pathlib import Path

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
    if segment is not None:
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


new_segment = None

for infile in args.input:
    infile = Path(infile)
    with infile.open() as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                # Create new segment, and write out the current one
                new_segment = writeAndCreateNewFile(segment, infile.stem)




# 'gpsbabel', '-t', '-i', 'gpx', '-f', str(outfile), '-x', 'track,sdistance=0.3k', '-o', 'gpx', '-F', outfile

                # for point in segment.points:

                #     print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
