"""
     File: /src/parser.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/svneditor
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated July 31, 2009
  Purpose: Used for parsing svn dump files and re-writing them
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

# import the hashlib module for md5
import hashlib

class Revision:
    """ Describes a subversion revision """

    def __init__(self, rev):
        """ Creates a revision setting """
        
        self.content_length = None
        self.prop_content_length = None
        self.revision_number = rev
        self.property_data = None
        self.nodes = []
        
class Node:
    """ Describes a subversion node """
    def __init__(self):
        # the following properties are supported
        self.properties = {
            # the ones I need/use
            "Node-path": None,
            "Node-kind": None,
            "Node-action": None,
            "Content-length": None,
            "Text-content-md5": None,
            "Text-content-length": None,
            "Prop-content-length": None,
            # these will be recreated in new dump file but are not supported
            "Text-delta": None,
            "Prop-delta": None,
            "Text-delta-base-md5": None,
            "Text-delta-base-sha1": None,
            "Text-copy-source-sha1": None,
            "Text-content-sha1": None,
            "Node-copyfrom-rev": None,
            "Node-copyfrom-path": None,
            "Text-copy-source-md5": None
        }
        
        self.properties_order = [
            'Node-path',
            'Node-kind',
            'Node-action',
            'Node-copyfrom-rev',
            'Node-copyfrom-path',
            'Text-copy-source-md5',
            'Text-copy-source-sha1',
            'Prop-content-length',
            'Text-content-length',
            'Text-delta',
            'Prop-delta',
            'Text-delta-base-md5',
            'Text-delta-base-sha1',
            'Text-content-md5',
            'Text-content-sha1',
            'Content-length',
        ]
        
        # property and text data
        self.property_data = None
        self.text_data = None
        
    def setProperty(self, name, value):
        """ Set a node property """
        name = name.strip()
        value = value.strip()
        if(name not in self.properties):
            print("NOTICE: Unrecognised Property (" + name + ")")
        self.properties[name] = value
    
    def updateText(self, value):
        """ Update the nodes text content but only if there is content """
        if self.text_data is not None:
            self.text_data = value
        
    def updateContentLength(self):
        """ Update the length data for the node """
        
        # get the lengths
        if self.text_data is not None:
            text_length = len(self.text_data)
        else: 
            text_length = 0
        if self.property_data is not None:
            prop_length = len(self.property_data)
        else:
            prop_length = 0
            
        # only update the content and text length if they were given
        if self.properties['Text-content-length'] is not None:
            self.properties['Text-content-length'] = str(text_length)
        if self.properties['Content-length'] is not None:
            self.properties['Content-length'] = str(text_length + prop_length)
            
    def updateTextMD5(self):
        """ Update the md5 hash of the text content """
        if(self.text_data is not None and 
           self.properties['Text-content-md5'] is not None):
            md5 = hashlib.md5()
            md5.update(self.text_data)
            self.properties['Text-content-md5'] = md5.hexdigest()
            
            
class _SVNDumpData:
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

class SVNDumpFileParser:
    """ Parsers a subversion dump file into a python data structure """

    def __init__(self, data):
        self.dumpfile = _SVNDumpData(data)
        
        self.log_version = 0
        self.uuid = ''
        self.revisions = []
        
    def parseHeaderLine(self, line):
        """ Parses a line thats a header, raises an error when invalid line is
        passed """
        tmp = line.split()
        if len(tmp) is not 2:
            raise ParseError("ERROR: Invalid Header Line (" + line + ")")
        return tmp[1]
    
    def skipEmptyLine(self):
        """ Skips a line that is checked to be empty. If it is not a error is 
        raised """
        # skip empty line
        if len(self.dumpfile.getNextLine().strip()) is not 0:
            raise ParseError('ERROR: Invalid dump file (Expecting Empty Line)')
        
    def skipEmptyLines(self, line = ""):
        """ Skips lines till a non empty line is found. Returns the non empty 
        line """
        while line == "" : line = self.dumpfile.getNextLine()
        return line
    
    def parse(self):
        """ Parses a dump file creating the python data structure """
        try:
            try:
                # get the version
                line = self.dumpfile.getNextLine()
                if line[0:27] != 'SVN-fs-dump-format-version:':
                    raise ParseError('ERROR: No Version Found In File')
                self.log_version = self.parseHeaderLine(line)
                
                self.skipEmptyLine()
                
                # get the UUID
                line = self.dumpfile.getNextLine()
                if line[0:4] == 'UUID':
                    self.uuid = self.parseHeaderLine(line)
                    self.skipEmptyLine()
                    line = self.dumpfile.getNextLine()
                    
            except EndOfDump:
                raise ParseError("Unexpected end of dump file")
                
            # get the rest of the data
            while True:
                try:
                    # find the next revision
                    if line[0:16] != 'Revision-number:':
                        raise ParseError('ERROR: No Revision Found')
                    rev = Revision(int(self.parseHeaderLine(line)))
                    
                    # get revision information
                    line = self.dumpfile.getNextLine()
                    if line[0:20] != 'Prop-content-length:':
                        raise ParseError("ERROR: No Property Content Length")
                    rev.prop_content_length = self.parseHeaderLine(line)

                    line = self.dumpfile.getNextLine()
                    if line[0:15] != 'Content-length:':
                        raise ParseError("ERROR: No Content Length")
                    rev.content_length = self.parseHeaderLine(line)
                    
                    # get revision property data
                    rev.property_data = \
                        self.dumpfile.getChunk(int(rev.content_length))
                    
                    line = self.dumpfile.getNextLine()
                    
                except EndOfDump:
                    raise ParseError("Unexpected end of dump file")
                
                # get the node information for revision
                while True:
                    node = Node()
                    
                    try:

                        # get node properties
                        line = self.skipEmptyLines(line)
                        
                        # sometimes there is an empty revision
                        if line[0:16] == 'Revision-number:': break
                        
                        # get the nodes properties
                        while len(line) is not 0:
                            s = line.split(':')
                            if len(s) is not 2:
                                raise ParseError("Invalid property ("+line+")")
                            node.setProperty(s[0], s[1])
                            line = self.dumpfile.getNextLine()
                        
                        # sometimes there is no content (add dir, deletes, etc)
                        # so we check there is content before trying to look for
                        # the content
                        c_len = node.properties['Content-length']
                        if c_len is not None:
                            try:
                                # get node content
                                d = _SVNDumpData(self.dumpfile \
                                                 .getChunk(int(c_len)))
                                # only if there is property data
                                p_len = node.properties['Prop-content-length']
                                if(p_len is not None):
                                    node.property_data = d.getChunk(int(p_len))
                                # get the node text data (if there is any)
                                node.text_data = d.getRemaining()
                            except EndOfDump: pass # EOD is allowed here
                            
                        # add the node to the revision
                        rev.nodes.append(node)
                    except EndOfDump:
                        raise ParseError("Unexpected end of dump file")
                    try:
                        line = self.skipEmptyLines()
                        if line[0:16] == 'Revision-number:': break
                    except EndOfDump:
                        # end of file allowed here
                        self.revisions.append(rev)
                        return True
    
                self.revisions.append(rev)
        except ParseError, e:
            print("Parser Error - " + e.message)
            return False
        return True
    
class SVNDumpFileWriter:
    """ Writes a dump file from the data created by SVNDumpFileParser """
    
    def __init__(self, dump):
        self.dump = dump
    
    def writeFile(self, file_path):
        
        # open the file
        self.f = open(file_path, 'wb')
        # write the dump header
        self.f.write('SVN-fs-dump-format-version: ' \
                     + self.dump.log_version + "\n\n")
        if self.dump.uuid is not '':
            self.f.write(str('UUID: ' + self.dump.uuid + "\n\n"))
        
        # write the revisions
        for rev in self.dump.revisions:
            self.writeRevision(rev)
            
        # close the file
        self.f.close()
        
    def writeRevision(self, rev):
        
        # write revision header
        self.f.write('Revision-number: ' + str(rev.revision_number) + '\n')
        self.f.write('Prop-content-length: ' + rev.prop_content_length + '\n')
        self.f.write('Content-length: ' + rev.content_length + '\n')
        self.f.write(rev.property_data + '\n\n')
        
        # write the node
        for node in rev.nodes:
            self.writeNode(node)
            
    def writeNode(self, node):
        # write properties
        for prop in node.properties_order:
            if node.properties[prop] is not None:
                props = True
                self.f.write(prop + ": " + node.properties[prop] + "\n")
        self.f.write('\n')
        if node.property_data is not None:
            self.f.write(node.property_data)
        if node.text_data is not None:
            self.f.write(node.text_data)
        if node.property_data is not None or node.text_data is not None:
            self.f.write('\n')
        self.f.write('\n')
            
        

class EndOfDump(Exception):
    """ Raised when the end of the SVN Dump File is reached """
    pass

class ParseError(Exception):
    """ Raised when the dump contains invalid data """
    
    def __init__(self, message = ""):
        self.message = message
    def _get_message(self): return self._message
    def _set_message(self, message): self._message = message
    message = property(_get_message, _set_message)


    
