"""
     File: /src/main.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/projects/svneditor/
           http://code.google.com/p/svndumpeditor/
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated October 13, 2009
  Purpose: The GUI that wraps the dump file parser and writer
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

import wx # for the gui
import Events
import Widgets

from SubversionDumpParser import SVNDumpFileParser # the dump parser
from SubversionDumpWriter import SVNDumpFileWriter # the dump writer


class ApplicationWindow(wx.Frame):
    """ The main application window, this class handles all the GUI creation """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL) 
        
        # the revision drop down
        self.revisions = Widgets.RevisionsCombo(self)
        right_sizer.AddSpacer(5)
        right_sizer.Add(self.revisions, 0, wx.EXPAND)
        
        # the node list
        self.node_list = Widgets.NodeList(self)
        right_sizer.AddSpacer(5)
        right_sizer.Add(self.node_list, 1, wx.EXPAND)
        right_sizer.AddSpacer(5)
        
        # the content viewer/editor
        self.content = Widgets.NodeContent(self)
        left_sizer.AddSpacer(5)
        left_sizer.Add(self.content, 1, wx.EXPAND)
        left_sizer.AddSpacer(5)
        
        # layout the main application
        main_sizer = wx.BoxSizer()
        main_sizer.AddSpacer(10)
        main_sizer.Add(right_sizer, 2, wx.EXPAND)
        main_sizer.AddSpacer(10)
        main_sizer.Add(left_sizer, 5, wx.EXPAND)
        main_sizer.AddSpacer(10)
        self.SetSizer(main_sizer)
        
        # add the menu
        self.menu = Widgets.MainMenu(self)        
        self.SetMenuBar(self.menu)
        
        # add the status bar
        self.status = Widgets.StatusBar(self)
        self.SetStatusBar(self.status)
        
        # add the toolbar
        self.toolbar = Widgets.ToolBar(self)
        self.SetToolBar(self.toolbar)
        
        self.CenterOnScreen()

class App(ApplicationWindow):
    """ The application logic class, this class gives the GUI functionality. """
    def __init__(self, *args, **kwargs):
        ApplicationWindow.__init__(self, *args, **kwargs)

        self.data = None
        self.revision_id = None
        self.node_id = None
        
        # bind out custom events to do some work
        self.Bind(Events.EVT_OPEN_DUMP, self.openSubversionDump)
        self.Bind(Events.EVT_SAVE_DUMP, self.saveSubversionDump)
        self.Bind(Events.EVT_CONTENT_SAVE, self.saveNodeContent)
        self.Bind(Events.EVT_REVISION_CHANGE, self.showRevisionNodes)
        self.Bind(Events.EVT_NODE_SELECT, self.showNodeContent)

    def openSubversionDump(self, event):
        """ Open and parse a subversion dump file """
        # create the dialog
        dialog = Widgets.OpenDialog(self)
        
        # if file was selected
        if dialog.ShowModal() == wx.ID_OK:
            # load the file
            try:
                f = open(dialog.GetPath(), 'rb')
                self.data = SVNDumpFileParser(f.read())
                f.close()
            except IOError:
                self.status.set("Error Reading Subversion Dump File")
                return
            
            # parse the dump
            if not self.data.parse():
                self.status.set("Error Parsing Subversion Dump File")
                return
            
            self.status.set("Subversion Dump File Parsed Successfully")
            
            self.node_list.reset()
            self.content.reset()
            self.revisions.populate(self.data.revisions)
    
    def saveSubversionDump(self, event):
        """ Save the dump to a new file """
        
        # create the dialog
        dialog = Widgets.SaveDialog(self)
        
        # if ok was clicked
        if dialog.ShowModal() == wx.ID_OK:
            # load the data into the parser and write the file
            try:
                w = SVNDumpFileWriter(self.data)
                w.writeFile(dialog.GetPath())
            except IOError:
                self.status.set("Error Exporting Subversion Dump File")
                return
            self.status.set("Subversion Dump File Exported")
            
    def saveNodeContent(self, event):
        """ Saves the edited file """
        
        if self.node_id is not None:
            # Update the text
            self.data.revisions[self.revision_id].nodes[self.node_id] \
                                   .updateText(self.content.getContent())
            # recalculate the contents length
            self.data.revisions[self.revision_id].nodes[self.node_id] \
                .updateContentLength()
            # it the hash value
            self.data.revisions[self.revision_id].nodes[self.node_id] \
                .updateHash()
            
            self.status.set("Node Content Saved")

    def showRevisionNodes(self, event):
        """ Show the nodes for the selected revisions """
        self.content.reset()
        self.revision_id = event.revision
        self.node_list.populate(self.data.revisions[self.revision_id].nodes)
    
    def showNodeContent(self, event):
        """ Show the content of the selected node """
        self.content.reset()
        self.node_id = event.node
        self.content.setContent(
            self.data.revisions[self.revision_id].nodes[self.node_id].text_data)
        
if __name__ == '__main__':    
    app = wx.PySimpleApp()
    frame = App(None, title="Subversion Editor", size=(600, 400))
    frame.Show()
    app.MainLoop()





