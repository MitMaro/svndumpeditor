"""
     File: /tests/test_property_data.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor
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

from Exceptions import ParseError
from PropertyData import PropertyData, PropertyKeyValue
from nose.tools import raises, assert_equal

class TestPropertyData:

    def testGetChunk(self):
        assert_equal(self.propdata.getChunk(5), "K 3\nk")
        #assert_equal(self.propdata.getChunk(3), "ey\n")
        
    def testGetNextLine(self):
        assert_equal(self.propdata.getNextLine(), "K 3")
        #assert_equal(self.propdata.getNextLine(), "key")
        #assert_equal(self.propdata.getNextLine(), "V 5")
        
    def testCalculateLength(self):
        self.propdata.parse()
        assert_equal(self.propdata.calculateLength(), 46)
        
    def testParse(self):
        self.propdata.parse()
        assert_equal(len(self.propdata.keyvaluepairs), 2)
        assert_equal(self.propdata.keyvaluepairs[0].key, "key")
        assert_equal(self.propdata.keyvaluepairs[0].value, "value")
        assert_equal(self.propdata.keyvaluepairs[1].key, "key01")
        assert_equal(self.propdata.keyvaluepairs[1].value, "val")

    def setUp(self):
        self.propdata = PropertyData("K 3\nkey\nV 5\nvalue\nK 5\nkey01\nV 3\nval\n")
        
    def tearDown(self):
        pass

class TestPropertyDataInvalid:

    @raises(ParseError)
    def testParseInvalidKey1(self):
        self.propdata = PropertyData("K3\nkey\nV 5\nvalue\n")
        self.propdata.parse()
        
    @raises(ParseError)
    def testParseInvalidValue1(self):
        self.propdata = PropertyData("K 3\nkey\nV5\nvalue\n")
        self.propdata.parse()
        
    @raises(ParseError)
    def testParseInvalidKey2(self):
        self.propdata = PropertyData("A 3\nkey\nV 5\nvalue\n")
        self.propdata.parse()
        
    @raises(ParseError)
    def testParseInvalidValue2(self):
        self.propdata = PropertyData("K 3\nkey\nA 5\nvalue\n")
        self.propdata.parse()
        
        
        