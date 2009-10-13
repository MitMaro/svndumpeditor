"""
     File: /src/Widgets.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: September 10, 2009; Updated October 13, 2009
  Purpose: Custom widgets
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
import Events

class RevisionsCombo(wx.Panel):
    """ A drop down combobox for the revisions """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.comboBox = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.triggerChange)
        label = wx.StaticText(self, label = "Revisions:")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.EXPAND)
        sizer.AddSpacer(3)
        sizer.Add(self.comboBox, 0, wx.EXPAND)
        self.SetSizer(sizer)

        self.parent = parent
        self.values = {}
    
    def triggerChange(self, event):
        """ Call this when there is a change in the revision """
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.RevisionChange(self.comboBox.GetId(),
                                                Events.REVISION_CHANGE,
                                                self.getRevision()))

    def getRevision(self):
        """ Return the revision index of the selected revision """
        return self.values[self.comboBox.GetValue()]

    def reset(self):
        """ Reset the widget to its default state """
        self.values.clear()
        self.comboBox.Clear()
    
    def populate(self, revisions):
        """ Populate the revisions drop down with revision data"""
        
        # reset first
        self.reset()
        
        # for each revision
        for i, r in enumerate(revisions):
            data_found = False
            # check nodes for data
            for n in r.nodes:
                if n.text_data is not None:
                    data_found = True
                    break
            # add the revision if there was a node with data, we don't show
            # revisions without data to view
            if data_found:
                # revision lookup, ComboBox text to index
                self.values["Revision: " + str(r.revision_number)] = i
                self.comboBox.Append("Revision: " + str(r.revision_number))

class NodeList(wx.Panel):
    """ The list of nodes for a revision """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.list =  wx.ListView(self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES)
        self.list.InsertColumn(0, "Nodes", width = 300)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.triggerChange)
        label = wx.StaticText(self, label = "File Nodes:")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.EXPAND)
        sizer.AddSpacer(3)
        sizer.Add(self.list, 1, wx.EXPAND)
        sizer.AddSpacer(5)
        self.SetSizer(sizer)

        self.parent = parent
        
    def triggerChange(self, event):
        """ Called when a selection change has been made"""
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.NodeSelect(self.list.GetId(),
                                                Events.NODE_SELECT,
                                                self.getNode()))

    def getNode(self):
        """ Returns the node index for the currently selected node """
        return self.list.GetItemData(self.list.GetFirstSelected())
    
    
    def reset(self):
        """ Reset to the factory defaults """
        self.list.DeleteAllItems()

    def populate(self, nodes):
        """ Populate the node list with the nodes """
        self.reset()
        for i, n in enumerate(nodes):
            # only show nodes with editable data
            if n.text_data is not None:
                listitem = wx.ListItem()
                listitem.SetText(n.properties['Node-path'])
                listitem.SetData(i)
                self.list.InsertItem(listitem)

class NodeContent(wx.Panel):
    """ A text area for displaying and editing node content """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.text = wx.TextCtrl(self, style = wx.TE_MULTILINE  | wx.HSCROLL)
        label = wx.StaticText(self, label="Node Content:")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.EXPAND)
        sizer.AddSpacer(3)
        sizer.Add(self.text, 1, wx.EXPAND)
        sizer.AddSpacer(5)
        self.SetSizer(sizer)
        self.parent = parent
    
    def setContent(self, content):
        """ Set the text content of the content viewer/editor """
        # later will add content modified check here
        self.text.ChangeValue(content)
    
    def getContent(self):
        """ Return the content of the viewer/editor """
        return self.text.GetValue()
    
    def reset(self):
        """ Reset to the factory defaults """
        # later add check for change here
        self.text.Clear()
    

class MainMenu(wx.MenuBar):
    """ The menu bar for the application """
    
    # some ids for the menubar items
    ID_OPEN = wx.NewId()
    ID_SAVE = wx.NewId()
    ID_ABOUT = wx.NewId()
    ID_EXIT = wx.NewId()
    
    def __init__(self, parent, *args, **kwargs):
        wx.MenuBar.__init__(self, *args, **kwargs)
        
        self.file = wx.Menu()
        self.file.Append(MainMenu.ID_OPEN, "&Open Dump", "Open a SVN Repository Dump")
        self.file.Append(MainMenu.ID_SAVE, "&Save Dump", "Save a  copy of the SVN Repository Dump")
        self.Append(self.file, "&File")
        self.parent = parent
        
        # bind the events to our custom events
        self.file.Bind(wx.EVT_MENU, self.triggerSaveDump, id=self.ID_SAVE)
        self.file.Bind(wx.EVT_MENU, self.triggerOpenDump, id=self.ID_OPEN)
                    
    def triggerOpenDump(self, event):
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.OpenDump(self.GetId(), Events.OPEN_DUMP))

    def triggerSaveDump(self, event):
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.SaveDump(self.GetId(), Events.SAVE_DUMP))


class StatusBar(wx.StatusBar):
    """ The status bar for the application """
    def __init__(self, parent, *args, **kwargs):
        wx.StatusBar.__init__(self, parent, *args, **kwargs)

    def set(self, text):
        self.SetStatusText(text)

class ToolBar(wx.ToolBar):
    """ The toolbar for the application """
    ID_OPEN = wx.NewId()
    ID_SAVE_CONTENT = wx.NewId()
    ID_SAVE_DUMP = wx.NewId()
    ID_ABOUT = wx.NewId()
    ID_EXIT = wx.NewId()
    
    def __init__(self, parent, *args, **kwargs):
        wx.ToolBar.__init__(self, parent, style= wx.TB_NOICONS, *args, **kwargs)
        
        self.AddLabelTool(ToolBar.ID_OPEN, 'Open Dump', wx.NullBitmap)
        self.AddLabelTool(ToolBar.ID_SAVE_DUMP, 'Export Dump', wx.NullBitmap)
        self.AddSeparator()
        self.AddLabelTool(ToolBar.ID_SAVE_CONTENT, 'Save Content', wx.NullBitmap)
        self.Realize()
        
        self.parent = parent 
        
        self.Bind(wx.EVT_MENU, self.triggerSaveDump, id=self.ID_SAVE_DUMP)
        self.Bind(wx.EVT_MENU, self.triggerSaveContent, id=self.ID_SAVE_CONTENT)
        self.Bind(wx.EVT_MENU, self.triggerOpenDump, id=self.ID_OPEN)
        
    def triggerOpenDump(self, event):
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.OpenDump(self.GetId(), Events.OPEN_DUMP))

    def triggerSaveDump(self, event):
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.SaveDump(self.GetId(), Events.SAVE_DUMP))
            
    def triggerSaveContent(self, event):
        self.parent.GetEventHandler() \
            .ProcessEvent(Events.ContentSave(self.GetId(), Events.CONTENT_SAVE))


class OpenDialog(wx.FileDialog):
    def __init__(self, parent, *args, **kwargs):
        wx.FileDialog.__init__(self,
                               parent,
                               message = "Please Select a Subversion Dump File",
                               style = wx.FD_FILE_MUST_EXIST | wx.FD_OPEN,
                               *args,
                               **kwargs)

class SaveDialog(wx.FileDialog):
    def __init__(self, parent, *args, **kwargs):
        wx.FileDialog.__init__(self,
                               parent,
                               message = "Please Select a Subversion Dump File",
                               style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                               *args,
                               **kwargs)

            
        
        
