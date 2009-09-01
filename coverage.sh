#!/bin/bash
#      File: /coverage.py
#   Project: Subversion Dump Editor
#        By: Tim Oram [t.oram@mitmaro.ca]
#  Website: http://www.mitmaro.ca/projects/svneditor/
#           http://code.google.com/p/svndumpeditor/
#     Email: svndump@mitmaro.ca
#   Created: August 18, 2009; Updated August 18, 2009
#   Purpose: Generates a coverage report
#  License:
# Copyright (c) 2009, Tim Oram
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of Mit Maro Productions nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY TIM ORAM ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL TIM ORAM BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

echo "Name                   Stmts   Exec  Cover   Missing
----------------------------------------------------"

echo -n "          "
nosetests -q --with-coverage --cover-erase --cover-package=Exceptions tests/test_exceptions.py 2>&1 | grep Exceptions
echo -n "               "
nosetests -q --with-coverage --cover-erase --cover-package=Node tests/test_node.py 2>&1 | grep Node
echo -n "        "
nosetests -q --with-coverage --cover-erase --cover-package=PropertyData tests/test_property_data.py 2>&1 | grep PropertyData
echo -n "            "
nosetests -q --with-coverage --cover-erase --cover-package=Revision tests/test_revision.py 2>&1 | grep Revision
echo -n "  "
nosetests -q --with-coverage --cover-erase --cover-package=SubversionDumpData tests/test_subversion_dump_data.py 2>&1 | grep SubversionDumpData
echo -n ""
nosetests -q --with-coverage --cover-erase --cover-package=SubversionDumpParser tests/test_subversion_dump_parser.py 2>&1  | grep SubversionDumpParser
echo -n ""
nosetests -q --with-coverage --cover-erase --cover-package=SubversionDumpWriter tests/test_subversion_dump_writer.py 2>&1 | grep SubversionDumpWriter

echo