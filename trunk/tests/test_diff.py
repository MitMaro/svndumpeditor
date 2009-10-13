"""
     File: /tests/test_diff.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: September 09, 2009; Updated October 13, 2009
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

from nose.tools import raises, assert_equal, assert_false
import Diff

class TestDiff:

    def setUp(self):
        self.patch = """--- data1 
+++ data2 
@@ -1,5 +1,5 @@
  a
  b
- c
+ f
  d
  e
"""

    def testCreateDiff(self):
        assert_equal(self.patch, ''.join(Diff.createDiff(" a\n b\n c\n d\n e\n", " a\n b\n f\n d\n e\n")))

    def testApplyPatchWithPatchConflict(self):
        assert_false(Diff.applyPatch(" a\n b\n e\n d\n e\n", self.patch))
        
    def testApplyPatch(self):
        assert_equal(" a\n b\n f\n d\n e\n", Diff.applyPatch(" a\n b\n c\n d\n e\n", self.patch))

    def testCreateVisualDiff(self):
        diff = Diff.createVisualDiff(" a\n b\n c\n d\n e\n".splitlines(), " a\n b\n f\n d\n e\n".splitlines())
        assert_equal(" a\n b\n-  c\n+  f\n d\n e\n", diff)
