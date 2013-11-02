#
# Lines of Code Counter
#
# Author:   Christian Floisand
# Version:  1.0
# Created:  2013/10/31
# Modified: 2013/11/01
# Copyright (c) 2013 Christian Floisand
#
# Outputs the total number of code lines, comment lines, and whitespace in a project.
# The files parsed are given by their extensions so the client can decide which file types to use
# in collecting the data.
#

import os
import sys
import string
from loccounter import LocCounter


# Globals
g_CommandLineErrorString = "Error parsing command-line arguments."
g_SupportedFiletypes = ["c", "cpp", "m", "mm", "h", "hpp", "cs", "py", "lua"]
g_ValidHelpFlags = ["-h", "-H", "--help", "-?"]


def printUsage():
    """Prints usage information to user.

    Current supported file types:
        c, cpp, m, mm, h, hpp, cs, py, lua
    """
    
    print "usage: python loc.py -files=<filetypes...> [path]"
    print "\t-filetypes\tA comma-separated list of one of the supported source code file extensions:"
    print "\t\t\tc, cpp, m, mm, h, hpp, cs, py, lua"
    print "\t-path\t\tSpecifies the root directory to begin recursively searching for source files."
    print "\t\t\tIf not given, or '.', the current working directory is used."
    print 

def getFiletypes():
    """Fetches the source code file types the user has requested.

    The built-in map function is used to insert a '.' at the front of each extension, which is required
    when matching the file extension against files in the search.

    Raises:
        IndexError: if command-line argument specifying file types is not given.
    """
    
    try:
        if not sys.argv[1][0:7] == "-files=":
            print g_CommandLineErrorString
            printUsage()
            sys.exit(0)

        fTypes = string.split(sys.argv[1][7:], ",") # Start at index 7 since indices 0-6 is the option specifier '-files='
        for t in fTypes:
            if not t in g_SupportedFiletypes:
                print t + " is not a supported source code file type."
                sys.exit(0)
                
        fTypes = map(lambda f: "." + f, fTypes)
        
    except IndexError:
        print g_CommandLineErrorString
        printUsage()
        sys.exit(0)

    return fTypes

def getPath():
    """Fetches the path the user has requested to act as the root directory in the recursive search.

    If no path is given, or a '.' is specified, the path defauls to the current working directory.

    Raises:
        IndexError: if command-line argument specifying the search path is not given.
        But this is optional, and will default to the current working directory without halting execution.
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


## main ##

if sys.argv[1] in g_ValidHelpFlags:
    printUsage()
else:
    totalCodeCount = 0
    totalCommentCount = 0
    totalWhitespaceCount = 0
    totalFilesRead = 0
    totalFilesFailed = 0
    failedFiles = []
    
    files = getFiles(getPath(), getFiletypes())
    for currentFile in files:
        try:
            fileHandle = open(currentFile, "r")
            counter = LocCounter(os.path.splitext(currentFile)[1])
            for currentLine in fileHandle:
                counter.countLine(currentLine)
            totalCodeCount += counter.codeCount
            totalCommentCount += counter.commentCount
            totalWhitespaceCount += counter.whitespaceCount
            totalFilesRead += 1
            fileHandle.close()

        except IOError:
            totalFilesFailed += 1
            failedFiles.extend(currentFile)

    print "Total number of files read: %d" % totalFilesRead
    print "Total lines of code: %d" % totalCodeCount
    print "Total lines of comments: %d" % totalCommentCount
    print "Total lines of whitespace: %d" % totalWhitespaceCount
