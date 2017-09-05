#!/bin/python
##############################################################################
# Create M3U playlists from folder content. Recursive.
# One playlist is created for each folder that is traversed.
# Playlist are named after their relative path from the start path with the
# path delimiter replaced by underscore, e.g. ./foo/bar becomes foo_bar.m3u
##############################################################################

import io
import os
import sys

def m3u_playlist_create(startPath):
  """Create m3u playlist from mp3 files within given folders. Recursive."""
  os.chdir(startPath)
  for path, dirs, files in os.walk(startPath):
    mp3s = [x for x in files if x.endswith(".mp3")]
    m3us = [x for x in files if x.endswith(".m3u")]
    if len(mp3s) == 0:
      print("# Skipping folder which contains no MP3s files: "+path)
      continue
    elif len(m3us) != 0:
      print("# Skipping folder which already contains a M3U playlist file: "+path)
    else:
      splitPath = path.split(os.path.sep)
      splitPath = splitPath[1:] # Omit '.'
      m3uName = "_".join(splitPath)
      m3uName = m3uName.replace(' ', '_')
      m3uName += ".m3u"
      print("# Creating playlist: "+m3uName)
      m3uPath = os.path.join(path, m3uName)
      m3uFile = open(m3uPath, 'w')
      m3uFile.write('#M3UEXT\n')
      mp3s.sort()
      for mp3 in mp3s:
        print("Adding file: "+mp3)
        m3uFile.write(mp3+'\n')
      m3uFile.close()

if __name__ == '__main__':
  if len(sys.argv) > 1:
    startPath = sys.argv[1]
  else:
    startPath = "."
  m3u_playlist_create(startPath)
