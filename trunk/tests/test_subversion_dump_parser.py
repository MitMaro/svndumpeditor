"""
     File: /tests/test_subversion_dump_parser.py
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

from SubversionDumpParser import SVNDumpFileParser
from Exceptions import ParseError, EndOfDump
from nose.tools import raises, assert_equal

class TestParseHeaderLine:

    def testValidHeader1(self):
        assert_equal(self.parser.parseHeaderLine("name: value"), "value")
        
    def testValidHeader2(self):
        assert_equal(self.parser.parseHeaderLine("name:value"), "value")
    
    @raises(ParseError)
    def testInvalidHeader1(self):
        self.parser.parseHeaderLine("invalidheader")
    
    def setUp(self):
        self.parser = SVNDumpFileParser("")
        
    def tearDown(self):
        pass

class TestSkipEmptyLine:
    
    def testSkipEmptyLine(self):
        self.parser.skipEmptyLine()
    
    @raises(ParseError)
    def testSkipEmptyLineError(self):
        self.parser.skipEmptyLine()
        self.parser.skipEmptyLine()
    
    def setUp(self):
        self.parser = SVNDumpFileParser("   \nNon-Empty Line\n")
        
    def tearDown(self):
        pass
    
class TestSkipEmptyLines:
    
    def testSkipEmptyLines1(self):
        assert_equal(self.parser.skipEmptyLines(""), "Non-Empty Line")
        
    def testSkipEmptyLines2(self):
        assert_equal(self.parser.skipEmptyLines("  "), "Non-Empty Line")

    def testSkipEmptyLines3(self):
        assert_equal(self.parser.skipEmptyLines("Non-Empty Given Line"), "Non-Empty Given Line")
        
    def setUp(self):
        self.parser = SVNDumpFileParser("\n\nNon-Empty Line\n")
        
    def tearDown(self):
        pass
    
class TestParseDumpHead:
    
    def testParseValidHeader(self):
        data = \
"""SVN-fs-dump-format-version: 2

UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Rev...
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseDumpHead()
    
    @raises(ParseError)
    def testParseInvalidHeader1(self):
        data = ""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseDumpHead()
        
    @raises(ParseError)
    def testParseInvalidHeader2(self):
        data = \
"""SVN-fs-dump-format-versisn: 2

UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Rev...
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseDumpHead()
    
class TestParseRevision:
    
    def testValidRevision(self):
        data = \
"""Prop-content-length: 26
Content-length: 26

K 3
xxx
V 3
xxx
PROPS-END

Node-path: /path/to/file
Node-kind: file
Node-action: add
Prop-content-length: 28
Text-content-length: 24
Text-content-md5: 474eae617ba4accc62cea9e709fb72f3
Text-content-sha1: 03531ed9e988918b844870f3a1d4dcff9c8565a3
Content-length: 52

K 4
xxxx
V 4
xxxx
PROPS-END
This is the text content

"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseRevision("Revision-number: 1")
    
    @raises(ParseError)
    def testInvalidRevision1(self):
        self.parser = SVNDumpFileParser("")
        self.parser.parseRevision("Revision-n: 1")
        
    @raises(ParseError)
    def testInvalidRevision2(self):
        self.parser = SVNDumpFileParser("Prop-contet-length: 26\n")
        self.parser.parseRevision("Revision-number: 1")
            
    @raises(ParseError)
    def testInvalidRevision3(self):
        self.parser = SVNDumpFileParser("Prop-content-length: 26\nConent-length: 26\n")
        self.parser.parseRevision("Revision-number: 1")
                           
    @raises(ParseError)
    def testInvalidRevision4(self):
        self.parser = SVNDumpFileParser("")
        self.parser.parseRevision("Revision-number: 1")

class TestParseNode:
    
    def testValid1(self):
        data = \
"""
Node-path: /path/to/file
Node-kind: file
Node-action: add
Prop-content-length: 28
Text-content-length: 24
Text-content-md5: 474eae617ba4accc62cea9e709fb72f3
Text-content-sha1: 03531ed9e988918b844870f3a1d4dcff9c8565a3
Content-length: 52

K 4
xxxx
V 4
xxxx
PROPS-END
This is the text content
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseNode("")
        
    def testValid2(self):
        data = \
"""
Node-path: /path/to/file
Node-kind: file
Node-action: add
Prop-content-length: 10
Content-length: 10

PROPS-END
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseNode("")
    
    @raises(ParseError)
    def testInvalid1(self):
        data = \
"""
Node-path: /path/to/file
Node-kind: file
Node-action invalid add
Prop-content-length: 28
Text-content-length: 24
Text-content-md5: 474eae617ba4accc62cea9e709fb72f3
Text-content-sha1: 03531ed9e988918b844870f3a1d4dcff9c8565a3
Content-length: 52

K 4
xxxx
V 4
xxxx
PROPS-END
This is the text content
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseNode("")
    
    @raises(ParseError)
    def testInvalid2(self):
        data = ""
        self.parser = SVNDumpFileParser(data)
        self.parser.parseNode("")

class TestParse:
    def testValidParse1(self):
        data = \
"""SVN-fs-dump-format-version: 2

UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Revision-number: 0
Prop-content-length: 46
Content-length: 46

K 3
key
V 5
value
K 5
key01
V 3
val
PROPS-END

Revision-number: 1
Prop-content-length: 26
Content-length: 26

K 3
xxx
V 3
xxx
PROPS-END

Node-path: /path/to/file
Node-kind: file
Node-action: add
Prop-content-length: 28
Text-content-length: 24
Text-content-md5: 474eae617ba4accc62cea9e709fb72f3
Text-content-sha1: 03531ed9e988918b844870f3a1d4dcff9c8565a3
Content-length: 52

K 4
xxxx
V 4
xxxx
PROPS-END
This is the text content

"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parse()

    def testValidParse2(self):
        data = \
"""SVN-fs-dump-format-version: 2

UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Revision-number: 0
Prop-content-length: 46
Content-length: 46

K 3
key
V 5
value
K 5
key01
V 3
val
PROPS-END

Revision-number: 1
Prop-content-length: 26
Content-length: 26

K 3
xxx
V 3
xxx
PROPS-END

Node-path: /path/to/file
Node-kind: file
Node-action: add
Prop-content-length: 28
Text-content-length: 24
Text-content-md5: 474eae617ba4accc62cea9e709fb72f3
Text-content-sha1: 03531ed9e988918b844870f3a1d4dcff9c8565a3
Content-length: 52

K 4
xxxx
V 4
xxxx
PROPS-END
This is the text content

Revision-number: 2
Prop-content-length: 26
Content-length: 26

K 3
xxx
V 3
xxx
PROPS-END

Node-path: /path/to/file
Node-kind: file
Node-action: add
Prop-content-length: 28
Text-content-length: 24
Text-content-md5: 474eae617ba4accc62cea9e709fb72f3
Text-content-sha1: 03531ed9e988918b844870f3a1d4dcff9c8565a3
Content-length: 52

K 4
xxxx
V 4
xxxx
PROPS-END
This is the text content
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parse()

    def testInValidParse(self):
        data = \
"""SVN-fs-dump-format-version: 2

UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Revision-number: 0
Prop-content-length: 10
Content-length: 10

PROPS-END

Revision-number: 1
"""
        self.parser = SVNDumpFileParser(data)
        self.parser.parse()

