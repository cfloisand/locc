# locc #

## Lines of Code Counter ##

A Python script that recursively scans a given directory for source files, and counts 
the number of lines of code, comments, and whitespace totalled from all the files. File 
types need to be provided at the command prompt so the script can filter which source 
files to parse.  

The script counts inline block and line comments in addition to comments occupying 
its own line. For example, the line:

	a += 1; // increment a by 1
results in 1 line of code and 1 comment added to the total.

### Supported file types ###

	c, cpp, cc, h, hpp, m, mm, cs, py, lua, js, swift

### Sample usage ###

	$ ./locc.py -files=c,cpp ~/path/to/project
	
	SUMMARY
	------------------------------
	Lines of code:          175 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	Comments:                69 ++++++++++++++++++++++
	Whitespace:              63 +++++++++++++++++++++
	------------------------------
	Files read:               2
	
---

Copyright (C) 2014 Christian Floisand

This program is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the  GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  
If not, see <http://www.gnu.org/licenses/>.
