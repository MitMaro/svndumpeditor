"""
     File: /src/SubversionDumpParser.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated October 13, 2009
  Purpose: The Subversion dump file parser
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
from SubversionDumpData import SVNDumpData
from Revision import Revision
from PropertyData import PropertyData, PropertyKeyValue
from Node import Node


class SVNDumpFileParser:
    """ Parsers a subversion dump file into a python data structure """

    def __init__(self, data):
        self.dumpfile = SVNDumpData(data)
        
        self.log_version = 0
        self.uuid = ''
        self.revisions = []
        # connects revision number to index in self.revisions
        self.revisions_lookup = {}
        
    def parseHeaderLine(self, line):
        """ Parses a line thats a header, raises an error when invalid line is
        passed """
        tmp = line.split(':')
        if len(tmp) is not 2:
            raise ParseError("ERROR: Invalid Header Line (" + line + ")")
        return tmp[1].lstrip()
    
    def skipEmptyLine(self):
        """ Skips a line that is checked to be empty. If it is not a error is 
        raised """
        # skip empty line
        if len(self.dumpfile.getNextLine().strip()) is not 0:
            raise ParseError('ERROR: Invalid dump file (Expecting Empty Line)')
        
    def skipEmptyLines(self, line = ""):
        """ Skips lines till a non empty line is found. Returns the non empty 
        line """
        line = line.strip()
        while line == "" : line = self.dumpfile.getNextLine().strip()
        return line
    
    def parseDumpHead(self):
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
                
            return line
                
        except EndOfDump:
            raise ParseError("Unexpected end of dump file")
    
    def parseRevision(self, line):
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
            
            
            # parse the revision property data without PROPS-END 
            rev.property_data = PropertyData(
                self.dumpfile.getChunk(int(rev.prop_content_length))[:-10]
            )
            rev.property_data.parse()
            
            return [self.dumpfile.getNextLine(), rev]
            
        except EndOfDump:
            raise ParseError("Unexpected end of dump file")
        
    def parseNode(self, line):
        node = Node()
        
        try:
            # get node properties
            line = self.skipEmptyLines(line)
            
            # sometimes there is an empty revision, perhaps hot the greatest
            # way to handle this
            if line[0:16] == 'Revision-number:': raise EndOfRevision(line)
            
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
                    d = SVNDumpData(self.dumpfile \
                                     .getChunk(int(c_len)))
                    # only if there is property data
                    p_len = node.properties['Prop-content-length']
                    if(p_len is not None):
                        # parse the node property data
                        node.property_data = PropertyData(
                          d.getChunk(int(p_len))[:-10]
                        )
                        node.property_data.parse()
                        
                    # get the node text data (if there is any)
                    node.text_data = d.getRemaining()
                except EndOfDump: pass # EOD is allowed here
            return [line, node]
        except EndOfDump:
            raise ParseError("Unexpected end of dump file")
        

    
    def parse(self):
        """ Parses a dump file creating the python data structure """
        try:
            # parse out the dump head data
            line = self.parseDumpHead()
            
            # get the rest of the data
            while True:
                # parse the revision data
                line, rev = self.parseRevision(line)
                # get the node information for revision
                while True:
                    try:
                        line, node = self.parseNode(line)
                        # add the node to the revision
                        rev.nodes.append(node)
                                                
                        # add node to the lookup dictionary
                        if node.properties['Node-path'] is not None:
                            rev.nodes_lookup[node.properties['Node-path']] = len(rev.nodes) - 1
                        else:
                            raise ParseError("Empty Node Path") # pragma: no cover
                    
                    # we made it to the new revision during the node parse
                    except EndOfRevision, e:
                        line = e.line
                        break
                    
                    try:
                        line = self.skipEmptyLines()
                        if line[0:16] == 'Revision-number:': break
                    except EndOfDump:
                        # end of file allowed here
                        self.revisions.append(rev)
                        return True
                # add the revision to the data
                self.revisions.append(rev)
                
                # add to the revisions lookup dictionary
                self.revisions_lookup[rev.revision_number] = len(self.revisions) - 1
                
        except ParseError, e:
            print("Parser Error - " + e.message)
            return False
