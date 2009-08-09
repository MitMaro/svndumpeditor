"""
     File: /src/SubversionDumpData.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated August 09, 2009
  Purpose: Holds a Subversion dump data
 License:
Copyright (c) 2009, Tim Oram
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
  * Neither the name of Mit Maro Productions nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY TIM ORAM ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL TIM ORAM BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import __future__

from Exceptions import *

class SVNDumpData:
    """ Holds the dump file and contains methods to help parse the dump file.
    This is also used with portions of the dump file."""
    
    def __init__(self, data):
        self.index = 0
        self.data = data
        self.length = len(data)
        
    def getNextLine(self):
        """ Grab a line of text """
        # check to see if we are already at the end of the file
        if self.index >= self.length: raise EndOfDump
        
        start = self.index
        i = 0
        
        # keep checking characters till a newline (ascii 10) is found
        while ord(self.data[self.index + i]) != 10:
            # if we reach the end of the file
            i += 1
            if self.index + i >= self.length: raise EndOfDump
        
        self.index += i + 1
        
        # return the line
        return self.data[start:start + i]
    
    def getRemaining(self):
        """ Return the rest of the data in the dump """
        # check to see if we are already at the end of the file
        if self.index >= self.length: raise EndOfDump
        return self.data[self.index:]

    def getChunk(self, size):
        """ Returns a chunk of size from current index of the data in the dump
        """
        start = self.index
        self.index += size
        if self.index > self.length: raise EndOfDump
        return self.data[start:start + size]
