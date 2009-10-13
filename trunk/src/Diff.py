"""
     File: /src/Diff.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: September 02, 2009; Updated October 13, 2009
  Purpose: Contains some functions for creating and patching diffs
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

import difflib
import tempfile
import os
import subprocess

# Creates a diff that can later be used in patch
def createDiff(data_one, data_two):
    d = difflib.unified_diff(data_one.splitlines(), data_two.splitlines(), "data1", "data2")
    patch = ''
    for line in d:
        patch += line.strip("\n") + "\n"
    return patch

# returns a full file that contains visual cues to the difference between two
# files
def createVisualDiff(data_one, data_two):
    d = difflib.Differ()
    rtn = ""
    for line in list(d.compare(data_one, data_two)):
        # trim the two spaces from unchanged lines
        if line[0] is " ":
            rtn += line[2:] + "\n"
        # exclude the lines that are showing changes in a line
        elif line[0] is not "?":
            rtn += line + "\n"
    return rtn

# This will be ugly, Python doesn't currently support patch, even though it does
# support diff. Uses the system patch program to apply a diff to a file.
def applyPatch(file, patch):
    # create the data temp file
    data_tmpfile = tempfile.NamedTemporaryFile(delete=False)
    data_tmpfile_name = data_tmpfile.name
    data_tmpfile.write(file)
    data_tmpfile.close()
    
    # create the patch temp file
    patch_tmpfile = tempfile.NamedTemporaryFile(delete=False)
    patch_tmpfile_name = patch_tmpfile.name
    patch_tmpfile.write(patch)
    patch_tmpfile.close()
    
    # path to patch should be settable
    t = subprocess.call(["/usr/bin/patch", "-s",  data_tmpfile_name  , patch_tmpfile_name], stdout = subprocess.PIPE)
    # if patch returns anything other then 0 something bad happened
    if  t != 0:
        # deletes the reject file
        # would be nice if I could tell patch to not make any files on error
        # --dry-run option may help
        os.remove(data_tmpfile_name + ".rej")
        return False
    
    # read the temp file
    rtn = open(data_tmpfile_name).read()
    
    # delete the two temp files we created
    os.remove(data_tmpfile_name)
    os.remove(patch_tmpfile_name)
    
    return rtn

