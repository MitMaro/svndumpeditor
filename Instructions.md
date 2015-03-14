# Instructions #

  1. Create a subversion repository dump using svnadmin: `svnadmin dump /path/to/repository > svndump.dump`
  1. Launch Subversion Dump Editor and load the file into the program using the "Open Dump" button in the tool bar.
  1. Select a revision from the revisions drop down.
  1. Select a node from the nodes list.
  1. Edit the node content.
  1. Save your edits using the "Save Content" button in the tool bar.
  1. Repeat for all edits you wish to make.
  1. Click the "Export Dump" button in the tool bar and save the dump. (I recommend saving as a new file and not replacing the original)
  1. Create a new subversion repository. (You could delete the old repository and recreate it but do this at your own risk)
  1. Load your edited subversion repository using svnadmin: `svnadmin load /path/to/new/repository < new_svndump.dump`
