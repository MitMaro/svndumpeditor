"""
     File: /src/SubversionDumpWriter.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated August 09, 2009
  Purpose: The Subversion dump file writer
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
from SubversionDumpData import SVNDumpData

    
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
        self.f.write('Content-length: ' + rev.content_length + '\n\n')
        # write the key-value pairs to the file
        for kp in rev.property_data.keyvaluepairs:
            self.f.write('K ' + str(kp.keylength) + "\n")
            self.f.write(kp.key + "\n")
            self.f.write('V ' + str(kp.valuelength) + "\n")
            self.f.write(kp.value + "\n")
        self.f.write("PROPS-END\n\n")
        
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
            # write each key-value pair to the file
            for kp in node.property_data.keyvaluepairs:
                self.f.write('K ' + str(kp.keylength) + "\n")
                self.f.write(kp.key + "\n")
                self.f.write('V ' + str(kp.valuelength) + "\n")
                self.f.write(kp.value + "\n")
            self.f.write("PROPS-END\n")
        if node.text_data is not None:
            self.f.write(node.text_data)
        if node.property_data is not None or node.text_data is not None:
            self.f.write('\n')
        self.f.write('\n')
            
        
