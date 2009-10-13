"""
     File: /src/Events.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: September 11, 2009; Updated October 13, 2009
  Purpose: Custom events used by the custom widgets
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

import wx

REVISION_CHANGE = wx.NewEventType()
EVT_REVISION_CHANGE = wx.PyEventBinder(REVISION_CHANGE, 1)

class RevisionChange(wx.PyEvent):
    def __init__(self, id, event_type, revision):
        wx.PyEvent.__init__(self, id, event_type)
        self.revision = revision


NODE_SELECT = wx.NewEventType()
EVT_NODE_SELECT = wx.PyEventBinder(NODE_SELECT, 1)

class NodeSelect(wx.PyEvent):
    def __init__(self, id, event_type, node):
        wx.PyEvent.__init__(self, id, event_type)
        self.node = node


CONTENT_SAVE = wx.NewEventType()
EVT_CONTENT_SAVE = wx.PyEventBinder(CONTENT_SAVE, 1)

class ContentSave(wx.PyEvent):
    def __init__(self, id, event_type):
        wx.PyEvent.__init__(self, id, event_type)


OPEN_DUMP = wx.NewEventType()
EVT_OPEN_DUMP = wx.PyEventBinder(OPEN_DUMP, 1)

class OpenDump(wx.PyEvent):
    def __init__(self, id, event_type):
        wx.PyEvent.__init__(self, id, event_type)


SAVE_DUMP = wx.NewEventType()
EVT_SAVE_DUMP = wx.PyEventBinder(SAVE_DUMP, 1)

class SaveDump(wx.PyEvent):
    def __init__(self, id, event_type):
        wx.PyEvent.__init__(self, id, event_type)
