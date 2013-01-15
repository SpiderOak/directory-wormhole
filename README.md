directory-wormhole
==================

The director wormhole is a simple Python3 program that watches a directory with inotify for files matching a glob pattern. When matching files exist, they are uploaded to Nimbus.io and then deleted. 