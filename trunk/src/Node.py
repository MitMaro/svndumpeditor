"""
     File: /src/Node.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated August 09, 2009
  Purpose: Holds a Subversion revisions node data
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
import hashlib

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
            "Text-content-sha1": None,
            "Text-content-length": None,
            "Prop-content-length": None,
            # these will be recreated in new dump file but are not supported.
            # Properties that contain "delta" should only exist in delta dumps
            # which are currently not supported by this program
            "Text-delta": None,
            "Prop-delta": None,
            "Text-delta-base-md5": None,
            "Text-delta-base-sha1": None,
            "Text-copy-source-sha1": None,
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
            prop_length = self.property_data.calculateLength()
        else:
            prop_length = 0
            
        # only update the content and text length if they were given
        if self.properties['Text-content-length'] is not None:
            self.properties['Text-content-length'] = str(text_length)
        if self.properties['Content-length'] is not None:
            self.properties['Content-length'] = str(text_length + prop_length)
            
    def updateHash(self):
        """ Update the md5 and sha1 hashes of the text content """
        if(self.text_data is not None): 
            if(self.properties['Text-content-md5'] is not None):
                md5 = hashlib.md5()
                md5.update(self.text_data)
                self.properties['Text-content-md5'] = md5.hexdigest()
            if(self.properties['Text-content-sha1'] is not None):
                sha1 = hashlib.sha1()
                sha1.update(self.text_data)
                self.properties['Text-content-sha1'] = sha1.hexdigest()

