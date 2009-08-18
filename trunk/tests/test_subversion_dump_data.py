"""
     File: /tests/test_subversion_dump_data.py
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

from SubversionDumpData import SVNDumpData
from nose.tools import raises, assert_equal

class TestPropertyData:
    
    def testGetNextLine(self):
        assert_equal(self.datadump.getNextLine(), "Line 1")
        assert_equal(self.datadump.getNextLine(), "Line 2")
        assert_equal(self.datadump.getNextLine(), "Line 3")
        
    def testGetChunk(self):
        assert_equal(self.datadump.getChunk(3), "Lin")
        assert_equal(self.datadump.getChunk(6), "e 1\nLi")
        assert_equal(self.datadump.getChunk(10), "ne 2\nLine ")
        
    def testGetRemaining(self):
        self.datadump.getChunk(10)
        assert_equal(self.datadump.getRemaining(), "e 2\nLine 3\n")

    def setUp(self):
        self.datadump = SVNDumpData("Line 1\nLine 2\nLine 3\n")
        
    def tearDown(self):
        pass
    
    
    