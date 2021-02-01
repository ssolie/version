#!/usr/bin/python
#
# Parses out the first embedded Amiga-style version string in a file.
#
# Special thanks to https://regex101.com/ for the assistance.
#
# Compatible with Python 2.5 and higher.
#
#
# version.py - Parses Amiga-style embedded version string
# Copyright (C) 2021 Steven Solie
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

import sys
import re
import getopt

# Embedded version string.
version = '$VER: version.py 54.1 (25.1.2021)'

# All output goes to outfile.
#
# In future, this can be set to other files.
outfile = sys.stdout

# Default command line arguments.
args = {
	'd': False,
	'n': False,
	'infile': None
}

def print_usage():
	print("Usage: version.py [option] file")
	print("  -d : Append date string to output")
	print("  -n : Output only version and revision string")
	print("file : Input file")

def parse_args():
	""" Parse command line arguments
	"""
	try:
		opts, files = getopt.getopt(sys.argv[1:], "dn")
	except getopt.GetoptError:
		return False

	for opt, val in opts:
		if opt == '-d':
			args['d'] = True

		if opt == '-n':
			args['n'] = True

	if (len(files)) != 1:
		return False
	else:
		args['infile'] = files[0]

	return True

if __name__ == "__main__":
	if not parse_args():
		print_usage()
		exit(1)

	file = open(args['infile'])
	content = file.read()
	file.close()

	version_regex  = re.compile(r""".*\$VER:\s(\S*)\s(\d+)\.(\d+)\s\((\d+)\.(\d+)\.(\d+)\)""")

	version_match = version_regex.search(content)
	if version_match:
		name     = version_match.group(1)
		version  = version_match.group(2)
		revision = version_match.group(3)
		mday     = version_match.group(4)
		month    = version_match.group(5)
		year     = version_match.group(6)
	else:
		outfile.write('No version string found\n')
		exit(1)

	if args['n']:
		outfile.write(str(version) + '.' + str(revision))
	else:
		outfile.write(name + ' ' + version + '.' + revision)

		if args['d']:
			outfile.write(' (' + mday + '/' + month + '/' + year + ')')

	outfile.write('\n')
	exit(0)
