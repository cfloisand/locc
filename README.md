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

	c, cpp, cc, h, hpp, m, mm, cs, py, lua, js

### Sample usage ###

	$ ./locc.py -files=c,cpp ~/path/to/project
	
	SUMMARY
	------------------------------
	Lines of code:          175 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	Comments:                69 ++++++++++++++++++++++
	Whitespace:              63 +++++++++++++++++++++
	------------------------------
	Files read:               2
	
