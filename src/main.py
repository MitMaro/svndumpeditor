"""
     File: /src/main.py
  Project: Subversion Dump Editor
       By: Tim Oram [t.oram@mitmaro.ca]
  Website: http://www.mitmaro.ca/svneditor
    Email: svndump@mitmaro.ca
  Created: June 26, 2009; Updated June 29, 2009
  Purpose: The GUI that wraps the parser module
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

import parser # the parser/writer

class LeftPanel(wx.Panel):
    """ The left side of the GUI"""
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        
        #self.rev_id = wx.NewId()
        
        # labels, not very exciting
        label1 = wx.StaticText(self, label = "Revisions:")
        label2 = wx.StaticText(self, label = "Nodes:")
        
        # the revisions drop down boxes
        self.revisions = wx.ComboBox(self, \
                                     style=wx.CB_DROPDOWN | wx.CB_READONLY)
        # the nodes list
        self.nodes = wx.ListBox(self, wx.LB_SINGLE)
        # the load and save dump buttons
        self.load = wx.Button(self, label = "Load SVN Dump")
        self.save = wx.Button(self, label = "Save SVN Dump")
        
        # bind some events
        self.revisions.Bind(wx.EVT_COMBOBOX, parent.revisionSelect)
        self.nodes.Bind(wx.EVT_LISTBOX, parent.nodeSelect)
        self.load.Bind(wx.EVT_BUTTON, parent.loadFile)
        self.save.Bind(wx.EVT_BUTTON, parent.saveFile)
        
        # place the widgets
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.AddStretchSpacer()
        sizer2.Add(self.load, 0)
        sizer2.Add(self.save, 0)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(label1, 0, wx.EXPAND)
        sizer1.Add(self.revisions, 0, wx.EXPAND)
        sizer1.Add(label2, 0, wx.EXPAND)
        sizer1.Add(self.nodes, 1, wx.EXPAND)
        sizer1.Add(sizer2, 0, wx.EXPAND)
        
        self.SetSizerAndFit(sizer1)
        
class RightPanel(wx.Panel):
    """ The right panel """
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        # Another label
        label = wx.StaticText(self, label = "Revision File Text:")
        # the content textarea
        self.textarea = wx.TextCtrl(self, style = wx.TE_MULTILINE  | wx.HSCROLL)
        # the save button
        self.save = wx.Button(self, label = "Save File")
        # Remove the cancel button for now
        # the cancel/reset button for editing
        #self.cancel = wx.Button(self, label = "Cancel")
        
        # bind the save button
        self.save.Bind(wx.EVT_BUTTON, parent.saveContent)
        
        # place the widgets
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.AddStretchSpacer()
        sizer2.Add(self.save, 0)
        #sizer2.Add(self.cancel, 0)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(label, 0, wx.EXPAND)
        sizer1.Add(self.textarea, 1, wx.EXPAND)
        sizer1.Add(sizer2, 0, wx.EXPAND)
        
        self.SetSizerAndFit(sizer1)


class MainFrame(wx.Frame):
    """ the applications window/frame """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # used to transform the list and combo boxes text into something usesful 
        self.node_lookup = {}
        self.revision_lookup = {}
        
        # will contain the parsed svn dump data
        self.data = None
        
        # current working revision and node
        self.rev = None
        self.node = None
        
        # create the two panels
        self.left_panel = LeftPanel(self)
        self.right_panel = RightPanel(self)
        
        # and place them
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.left_panel, 0, wx.EXPAND)
        sizer.Add(self.right_panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.CenterOnScreen()
        
    def __populateRevisions(self):
        """ Populate the revisions drop down """
        self.revision_lookup.clear()
        self.left_panel.revisions.Clear()
        self.left_panel.nodes.Clear()
        
        for i, r in enumerate(self.data.revisions):
            data_found = False
            # check nodes for data
            for n in r.nodes:
                if n.text_data is not None:
                    data_found = True
                    break
            # this runs when data was found
            if data_found:
                self.revision_lookup["Revision: " + str(r.revision_number)] = i
                self.left_panel.revisions \
                                  .Append("Revision: " + str(r.revision_number))
            
    def __populateNodes(self):
        """ Populates the nodes list """
        self.node_lookup.clear()
        self.left_panel.nodes.Clear()
        for i, n in enumerate(self.data.revisions[self.rev].nodes):
            # only show nodes with editable data
            if n.text_data is not None:
                self.node_lookup[n.properties['Node-path']] = i
                self.left_panel.nodes.Append(n.properties['Node-path'])
            
    def __populateContent(self, content):
        """ Populates the content text area """
        self.right_panel.textarea.ChangeValue(content)

    def loadFile(self, event):
        """ Loads the dump file and parses it """
        # create the dialog
        dialog = wx.FileDialog(self,
                               message = "Please Select a Subversion Dump File",
                               style = wx.FD_FILE_MUST_EXIST | wx.FD_OPEN)
        
        # if file was selected
        if dialog.ShowModal() == wx.ID_OK:
            f = open(dialog.GetPath(), 'rb')
            # load and parse the file
            self.data = parser.SVNDumpFileParser(f.read())
            self.data.parse()
            self.__populateRevisions()
            f.close()
            
    def saveFile(self, event):
        """ Save the dump to a new file """
        
        # create the dialog
        dialog = wx.FileDialog(self,
                               message = "Please Select a Subversion Dump File",
                               style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        # if ok was clicked
        if dialog.ShowModal() == wx.ID_OK:
            # load the data into the parser and write the file
            w = parser.SVNDumpFileWriter(self.data)
            w.writeFile(dialog.GetPath())
        
    def revisionSelect(self, event):
        """ Fired when a revision is selected """
        # load the revision index from the lookup dict
        self.rev = \
            self.revision_lookup[self.left_panel.revisions.GetValue()]
        self.__populateNodes()
        
    def nodeSelect(self, event):
        """ Fired when a node is selected """
        # load the node index from the lookup dict
        self.node = self.node_lookup[self.left_panel.nodes.GetStringSelection()]
        self.__populateContent(self.data.revisions[self.rev].nodes[self.node]
                               .text_data)
    
    def saveContent(self, event):
        """ Saves the edited file """
        # Update the text
        self.data.revisions[self.rev].nodes[self.node] \
                               .updateText(self.right_panel.textarea.GetValue())
        # recalculate the contents length
        self.data.revisions[self.rev].nodes[self.node].updateContentLength()
        # it the hash value
        self.data.revisions[self.rev].nodes[self.node].updateTextMD5()
        

if __name__ == '__main__':
    
    # calculate the size of the window to be 80% of the screen size
    app = wx.PySimpleApp() # for mac only
    #app = wx.App()
    
    rect = wx.ClientDisplayRect()
    frame = MainFrame(None, title="Subversion Editor", \
                      size=(rect[2] * .60, rect[3] * .80))
    frame.Show()
    #frame.populateRevisions(d.revisions)
    #frame.populateNodes(d.revisions[2].nodes)
    #frame.populateContent(str(d.revisions[2].nodes[1].text_data))
    
    app.MainLoop()





