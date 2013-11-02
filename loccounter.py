#
# Lines of Code Counter Class Module
#
# Author:   Christian Floisand
# Version:  1.0
# Created:  2013/11/01
# Modified: 2013/11/02
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

    With each line read from the source file, call the parseLine method on it, and the count values will be
    updated and stored for each unique instance of the class. When EOF is reached, the final count values
    (codeCount, commentCount, whitespaceCount) for the file should be accessed and added to the running total.

    Note: it is assumed that each comment type in each file type is of the same length.
        i.e. all opening block comment tags in Python are 3 characters, all closing comment tags in C++ are 2 characters,
        all line comment tags in Python are 1 character, etc.
    """
    
    codeCount = 0
    commentCount = 0
    whitespaceCount = 0
    
    def __init__(self, fileType):
        """Object initialization.
        Fetch the correct comment tag dictionary given the source code file type.
        The inBlock variable is used to track whether parsing is currently inside a block comment or not.
        """
        self._inBlock = False
        self._tags = CommentTags[fileType]
        self._lineTagLength = len(self._tags["line"][0])
        self._openTagLength = len(self._tags["block_open"][0])
        self._closeTagLength = len(self._tags["block_close"][0])

    def __findBlockTag(self, line, blockTag):
        for tag in self._tags[blockTag]:
            index = line.find(tag)
            if index >= 0:
                self._inBlock = not self._inBlock
                break
        return index

    def __findWhitespace(self, line):
        if line in string.whitespace:
            self.whitespaceCount += 1
            return True
        return False

    def __countLine(self, line):
        """Parses the given line and updates counters for code and comments. By the time this method is called,
        it has already been determined that line is not whitespace.

        Once a condition is met, this method returns immediately to avoid unnecessary parsing.

        When parsing for comments, this method accounts for both inline one-line comments and inline block
        comments, following a line of source code.
        """
        if self._inBlock:
            self.commentCount += 1
            # If when in the block, only a closing block comment tag is found, take back the count that was
            # added since this shouldn't count as a comment line.
            if self.__findBlockTag(line, "block_close") == 0:
                self.commentCount -= 1
            return

        # This check for one-line comments includes inline comments (following a line of source code).
        for tag in self._tags["line"]:
            index = line.find(tag)
            if index >= 0:
                if not len(line) == self._lineTagLength:
                    self.commentCount += 1
                if index > 0:
                    self.codeCount += 1
                return

        index = self.__findBlockTag(line, "block_open")
        if index >= 0:
            if index > 0:
                self.codeCount += 1
            # Strip away the opening block comment tag so that parsing for the closing tag doesn't count
            # the opening tag again (for languages where the tags are the same; i.e. Python).
            newLine = line[index + self._openTagLength:]
            
            # Make sure than one-line block comments are accounted for.
            if self.__findBlockTag(newLine, "block_close") > 0 :
                self.commentCount += 1
                return
            
            if len(newLine) > self._openTagLength:
                self.commentCount += 1

            return

        self.codeCount += 1
        return

    def parseLine(self, line):
        """This is the only public method exposed by the class, and should be the only one called by the client."""
        line = line.strip()
        if not self.__findWhitespace(line):
            self.__countLine(line)
    

if __name__ == "__main__":
    pass
