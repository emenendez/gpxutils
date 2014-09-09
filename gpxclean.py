#!/usr/local/bin/python3

import argparse
import gpxpy

parser = argparse.ArgumentParser(description='Clean GPX tracks and split into multiple files.')
parser.add_argument('input', nargs='+', help='a .gpx file to clean and split')
args = parser.parse_args()

for infile in args.input:
	pass