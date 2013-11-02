#
# Lines of Code Counter Class Module
#
# Author:   Christian Floisand
# Version:  1.0
# Created:  2013/11/01
# Modified: 2013/11/01
#

import string


# Individual comment tag definitions
# Each supported source code file type needs a dictionary defining the tags it uses for line comments
# and block comments. Some languages (e.g. Python) allow for more than one tag to start a comment, so the
# value entries in the dictionaries are lists.

C_CommentTags = {
    "line"          : ["//"],
    "block_open"    : ["/*"],
    "block_close"   : ["*/"]
    }

Py_CommentTags = {
    "line"          : ["#"],
    "block_open"    : ["'''", '"""'],
    "block_close"   : ["'''", '"""']
    }

Lua_CommentTags = {
    "line"          : ["--"],
    "block_open"    : ["--[["],
    "block_close"   : ["]]"]
    }

# Aggregate comment tags definition
# The keys in this dictionary correspond to the file type.
CommentTags = {
    ".c"    : C_CommentTags,
    ".cpp"  : C_CommentTags,
    ".h"    : C_CommentTags,
    ".hpp"  : C_CommentTags,
    ".m"    : C_CommentTags,
    ".mm"   : C_CommentTags,
    ".cs"   : C_CommentTags,
    ".py"   : Py_CommentTags,
    ".lua"  : Lua_CommentTags
    }


class LocCounter:
    """Lines of Code Counter class.

    This class needs to be instantiated with a source code file extension, which it uses to look up the
    corresponding comment tags to use when parsing the lines of the file.

    With each line read from the source file, call the countLine method on it, and the count values will be
    updated and stored for each unique instance of the class. When EOF is reached, the final count values
    (codeCount, commentCount, whitespaceCount) for the file should be accessed and added to the running total.

    Warning:
        At this time, the class assumes tags of the same file type and comment type are the same length.
        i.e. All line comment tags in Python are 1 character, all open block comment tags in Lua are 4 characters,
        all close block comments in C++ are 2 characters, etc.
    """
    
    codeCount = 0
    commentCount = 0
    whitespaceCount = 0
    
    def __init__(self, fileType):
        """Object initialization.
        Fetch the correct comment tag dictionary given the source code file type.
        The inblock variable is used to track whether parsing is currently inside a block comment or not.
        """
        self._inblock = False
        self._tags = CommentTags[fileType]
        self._lineTagLength = len(self._tags["line"][0])
        self._openTagLength = len(self._tags["block_open"][0])
        self._closeTagLength = len(self._tags["block_close"][0])

    def __readLineComment(self, line):
        for tag in self._tags["line"]:
            if line.startswith(tag, 0, self._lineTagLength):
                return True
        return False

    def __readOpenBlockComment(self, line):
        for tag in self._tags["block_open"]:
            if line.startswith(tag, 0, self._openTagLength):
                self._inblock = True
                return True
        return False

    def __readCloseBlockComment(self, line):
        linelength = len(line)
        for tag in self._tags["block_close"]:
            if line.endswith(tag, linelength - self._closeTagLength, linelength):
                self._inblock = False
                return True
        return False

    def __countWhitespace(self, line):
        if line in string.whitespace:
            self.whitespaceCount += 1
            return True
        return False

    def __countComments(self, line):
        line = line.strip()
        if self._inblock:
            self.commentCount += 1
            # If when in the block, only a closing block comment tag is found, take back the count that was
            # added since this shouldn't count as a comment line.
            if self.__readCloseBlockComment(line) and len(line) == self._closeTagLength:
                self.commentCount -= 1
            return True

        if self.__readLineComment(line):
            self.commentCount += 1
            return True
        
        if self.__readOpenBlockComment(line):
            # Only count this as a comment line if there is more than just the opening tag.
            if len(line) > self._openTagLength:
                self.commentCount += 1
            return True

        return False

    def countLine(self, line):
        """This is the only public method exposed by the class, and should be the only one called by the client."""
        if not self.__countWhitespace(line) and not self.__countComments(line):
            self.codeCount += 1
    

if __name__ == "__main__":
    pass

