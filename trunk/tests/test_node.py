"""
     File: /tests/test_node.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: August 18, 2009; Updated August 18, 2009
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

from Node import Node, Reference
from PropertyData import PropertyData, PropertyKeyValue
from Exceptions import ParseError
from nose.tools import raises, assert_equal

class TestNode:

    def testSetProperty(self):
        self.node.setProperty("Node-kind", 'dir')
        assert_equal(self.node.properties['Node-kind'], "dir")

    @raises(ParseError)
    def testSetPropertyInvalid(self):
        self.node.setProperty("Invalid-Property", 'invalid')
        
    def testUpdateText(self):
        self.node.updateText("Some Different Text")
        assert_equal(self.node.text_data, "Some Different Text")
        
    def testUpdateContentLength(self):
        self.node.updateText("Some Different Text")
        self.node.updateContentLength()
        assert_equal(self.node.properties['Content-length'], '47')
        assert_equal(self.node.properties['Text-content-length'], '19')
    
    def testUpdateContentLengthWithNones1(self):
        
        # set these to none
        self.node.properties['Content-length'] = None
        self.node.properties['Text-content-length'] = None
        self.node.updateContentLength()
        
        # they should not change
        assert_equal(self.node.properties['Content-length'], None)
        assert_equal(self.node.properties['Text-content-length'], None)

    def testUpdateContentLengthWithNones2(self):
        self.node.text_data = None
        self.node.property_data = None
        
        self.node.updateContentLength()
        
        # they should not change
        assert_equal(self.node.properties['Content-length'], '0')
        assert_equal(self.node.properties['Text-content-length'], '0')


    def testUpdateHash(self):
        self.node.updateHash()
        # they should not change
        assert_equal(self.node.properties['Text-content-md5'], 'd96d5a3dbe20c5f629587d3405a1eac2')
        assert_equal(self.node.properties['Text-content-sha1'], 'c92990287c37102e847f507f1ad2a6a477a451cc')

    def setUp(self):
        print "Here"

        self.node = Node()
        self.node.text_data = "Some Text Data"
        self.node.property_data = PropertyData("K 3\nkey\nV 5\nvalue\n")
        self.node.property_data.parse()
        self.node.properties = {
            "Node-path": '/path/to/node',
            "Node-kind": 'file',
            "Node-action": 'add',
            "Content-length": '42',
            "Text-content-md5": '',
            "Text-content-sha1": '',
            "Text-content-length": '14',
            "Prop-content-length": '28'
        }

    def tearDown(self):
        pass

class TestReference:
    
    def testReference(self):
        ref = Reference(1, 2)
        assert_equal(ref.revision, 1)
        assert_equal(ref.node, 2)
