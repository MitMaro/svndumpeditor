A small python application that will allow the editing of a subversion dump file. This should allow you to make modifications to your repository (via svnadmin dump and load) to remove sensitive data from a file/revision without having to completely remove the file containing the sensitive data. A good example would be to remove the database password you accidentally committed several revisions ago.

The code from SVN should always be fairly stable so give it a try if you like.

# Update #
SVN Dump Editor 0.1 beta 2 has been released. This release has an improved interface and is more stable then the previous beta.

![http://www.mitmaro.ca/img/misc/svneditor-beta2.png](http://www.mitmaro.ca/img/misc/svneditor-beta2.png)