"""
     File: /src/PropertyData.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: August 09, 2009; Updated August 10, 2009
  Purpose: Holds a Subversion revision's property data
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

from Exceptions import *

class PropertyKeyValue:
    """ Describes a property key value pair. """
    def __init__(self, key, value):
        self.key = key
        self.keylength = len(key)
        self.value = value
        self.valuelength = len(value)

class PropertyData:
    """ Describes the property data as keyvalue pairs. """
    
    def __init__(self, data):
        self.index = 0
        
        # strip the leading newline
        self.data = data.lstrip()
        self.length = len(self.data)
        self.keyvaluepairs = []
        
    def parse(self):
        """ Extracts key value pairs from the raw property data. """
        try:
            # keep looping till the end of data (EOD)
            while True:
                # get a line
                line = self.getNextLine()
                tmp = line.split()
                if len(tmp) is not 2 or tmp[0] is not "K":
                    raise ParseError("Invalid Property Key")
                
                # extract the key value
                key = self.getChunk(int(tmp[1]))
                
                # skip the trailing newline
                self.getNextLine()
                
                line = self.getNextLine()

                tmp = line.split()
                if len(tmp) is not 2 or tmp[0] is not "V":
                    raise ParseError("Invalid Property Value")
                
                # extract the value value
                value = self.getChunk(int(tmp[1]))
                
                # add the key-value pair to the list
                self.keyvaluepairs.append(PropertyKeyValue(key, value))

                # skip the trailing newline
                self.getNextLine()
        
        # fired when the end of the data is reached
        except EndOfDump:
            pass # do nothing
    
    def getChunk(self, size):
        """ Returns a chunk of size from current index of the data """
        start = self.index
        self.index += size
        if self.index > self.length: raise EndOfDump
        return self.data[start:start + size]
    
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
    
    def calculateLength(self):
        """ Returns the length of the text representation of the property data.
        """
        length = 1 # +1 for leading newline
        for kp in self.keyvaluepairs:
            # the key length + value length + 'k ' length + length of characters
            # in key length + 'v ' length + length of characters in value length
            length += kp.keylength + kp.valuelength + len(str(kp.keylength)) + \
                  len(str(kp.valuelength)) + 8 # len('K V ') = 4 and 4 "\n"
        length +=  9 # the length of 'PROPS-END'
        
        return length
    
