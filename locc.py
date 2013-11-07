#!/usr/local/bin/python

#
# Lines of Code Counter
#
# Author:   Christian Floisand
# Version:  1.0
# Created:  2013/10/31
# Modified: 2013/11/02
#
# Outputs the total number of code lines, comment lines, and whitespace in a project.
# The files parsed are given by their extensions so the client can decide which file types to use
# in collecting the data.
#

import os, sys, string
from loccounter import LocCounter


# Globals
g_SupportedFiletypes = ["c", "cpp", "cc", "m", "mm", "h", "hpp", "cs", "py", "lua", "js"]
g_ValidHelpFlags = ["-h", "-H", "--help", "-?"]


def printUsage():
    """Prints usage information to user.

    Current supported file types:
        c, cpp, cc, m, mm, h, hpp, cs, py, lua, js
    """
    
    print "usage: locc.py -files=<filetypes...> [path]"
    print "\t-filetypes\tA comma-separated list of one of the supported source code file extensions:"
    print "\t\t\t", ", ".join(["%s" % s for s in g_SupportedFiletypes])
    print "\t-path\t\tSpecifies the root directory to begin recursively searching for source files."
    print "\t\t\tIf not given, or '.', the current working directory is used."
    print 

def getFiletypes():
    """Fetches the source code file types the user has requested.

    The built-in map function is used to insert a '.' at the front of each extension, which is required
    when matching the file extension against files in the search.
    """
    
    try:
        if not sys.argv[1][0:7] == "-files=":
            print "Error parsing command-line arguments."
            printUsage()
            sys.exit(0)

        fTypes = string.split(sys.argv[1][7:], ",") # Start at index 7 since indices 0-6 is the option specifier '-files='
        for t in fTypes:
            if not t in g_SupportedFiletypes:
                print t + " is not a supported source code file type."
                sys.exit(0)
                
        fTypes = map(lambda f: "." + f, fTypes)
        
    except IndexError:
        print "Error parsing command-line arguments."
        printUsage()
        sys.exit(0)

    return fTypes

def getPath():
    """Fetches the path the user has requested to act as the root directory in the recursive search.

    If no path is given, or a '.' is specified, the path defauls to the current working directory.
    """
    
    try:
        path = sys.argv[2]
        if path == ".":
            path = os.getcwd()

    except IndexError:
        path = os.getcwd()

    return path

def getFiles(searchPath, fileExts):
    """Fetches the files that will be included in the count.

    Args:
        searchPath: The root directory to begin recursive search.
        fileExts: A list of file extensions to filter files by.

    Returns:
        A list of all the files matching the file types given at the command-line.
    """

    fileList = []
    for root, dirs, files in os.walk(searchPath):
        # Extend is faster than using '+=' since it does not create a new concatenated list each time.
        fileList.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] in fileExts])

    return fileList

def printSummary(counts):
    """Formats and prints the output of the counts totalled from all the files read.

    Also draws a horizontal bar graph for visualizing the relativity of the counts.
    """
    formatString = "{0:<20}{1:>7}"
    
    totalLines = counts["code"] + counts["comment"] + counts["whitespace"]
    try:
        # Round up by adding 0.5 before converting back to integer for use in range() function.
        codeGraph = int(float(counts["code"]) / totalLines * 100 + 0.5)
        commentGraph = int(float(counts["comment"]) / totalLines * 100 + 0.5)
        whitespaceGraph = int(float(counts["whitespace"]) / totalLines * 100 + 0.5)
    except ZeroDivisionError:
        codeGraph, commentGraph, whitespaceGraph = 0, 0, 0
    
    print
    print "SUMMARY"
    print "------------------------------"
    print formatString.format("Lines of code:", counts["code"]), "".join(["%s" % "+" for i in range(codeGraph)])
    print formatString.format("Comments:", counts["comment"]), "".join(["%s" % "+" for i in range(commentGraph)])
    print formatString.format("Whitespace:", counts["whitespace"]), "".join(["%s" % "+" for i in range(whitespaceGraph)])
    print "------------------------------"
    print formatString.format("Files read:", counts["files-read"])
    if counts["files-failed"] > 0:
        print formatString.format("Files failed:", counts["files-failed"])
        for item in counts["failed-files-list"]:
            print "\t" + item
    print


## main ##

if sys.argv[1] in g_ValidHelpFlags:
    printUsage()
else:
    totalCounts = {
        "code"          :   0,
        "comment"       :   0,
        "whitespace"    :   0,
        "files-read"    :   0,
        "files-failed"  :   0,
        "failed-files-list" : []
        }
    
    files = getFiles(getPath(), getFiletypes())
    for currentFile in files:
        try:
            fileHandle = open(currentFile, "r")
            counter = LocCounter(os.path.splitext(currentFile)[1])
            for currentLine in fileHandle:
                counter.parseLine(currentLine)
            totalCounts["code"] += counter.codeCount
            totalCounts["comment"] += counter.commentCount
            totalCounts["whitespace"] += counter.whitespaceCount
            totalCounts["files-read"] += 1
            fileHandle.close()

        except IOError:
            totalCounts["files-failed"] += 1
            totalCounts["failed-files-list"].append(currentFile)

    printSummary(totalCounts)
