"""
     File: /tests/test_subversion_dump_writer.py
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

from SubversionDumpWriter import SVNDumpFileWriter
from SubversionDumpParser import SVNDumpFileParser
from Exceptions import ParseError

from nose.tools import raises, assert_equal
from difflib import  Differ
from pprint import pprint

import os


class TestParseHeaderLine:
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

    def testWriteFile(self):
        self.writer.writeFile('tmp.test')
        file = open('tmp.test').read()
        if file != self.data:
            d = Differ()
            pprint(list(d.compare(self.data.splitlines(True), file.splitlines(True))))
            os.remove('tmp.test')
            assert False
        os.remove('tmp.test')
    
    def setUp(self):
        self.parser = SVNDumpFileParser(self.data)
        self.parser.parse()
        
        self.writer = SVNDumpFileWriter(self.parser)
        
    def tearDown(self):
        pass


