#!/usr/bin/env python
# encoding: utf-8
"""
EasyTV.py

Created by George on 2011-04-04.

Debugging commands
	#import pdb					
			#pdb.set_trace()

"""

import sys, os, time
import urllib, urllister
#import pdb	

def changeDir(nPath):         
	sPath = os.getcwd()
	os.chdir(nPath)
	return sPath


def revertDir(sPath):
	os.chdir(sPath)


def loadFile(file):
	"""Load shows into a list"""
	try:
		inputFile = open (file,"r")			# Open Shows.txt
	except:
		if file == "favouriteshows.txt":	
			createFavouriteShows()		# Create a new file with sample shows
			inputFile = open (file,"r")			# Open Shows.txt
		else:
			inputFile = open('oldshows.txt','a')	# Create a new file
			inputFile.write("/n")
			inputFile.close() #Close File
			inputFile = open('oldshows.txt','a')	# Create a new file
			
	while 1:
		try:
			line = inputFile.readline()
			if not line:	
				break
			if file == "favouriteshows.txt":	
				favouriteShows.append(line)		# Load shows into List
			else:
				oldShows.append(line)	
		except:
			print 'error at Loadfile %s' %file
		
	inputFile.close() #Close File


def createFavouriteShows():
	outputFile = open('favouriteshows.txt','a')		# Open oldshows.txt, append mode. If file doesnt exist it will be created
	for show in defaultFavouriteShows:
		outputFile.write(show)
	outputFile.close() 							#Close File
	
	
def writeEpisodetoOldShows(episode):
	"""Load show for Download into oldShows.txt file"""
	outputFile = open('oldshows.txt','a')		# Open oldshows.txt, append mode. If file doesnt exist it will be created
	outputFile.write(episode)
	outputFile.close() 							#Close File	
	oldShows = [] # reload the old shows list to also include the downloaded show above
	loadFile("oldshows.txt")

	
def createTorrent(fname, add):
	u = urllib.urlopen(address)
	f = open(file_name, 'w')
	f.write(u.read())
	print '1 torrent file written: %s' %file_name
	f.close()



# Definitions

newPath = "/Users/George/Dropbox/Torrents"
dicUrl = { }
favouriteShows = [] # list to store favourite TV shows
oldShows = [] # list to store the downloaded shows
defaultFavouriteShows = ('the-big-bang-theory\n', 'modern-family\n', 'mythbusters\n')
count = 1
nextLine = 0		# variable to help pickup url record after episode is found
timeoutHasOccurred = 0
print 'Run No. 1 '

while 1:


	# Load files into Lists
	favouriteShows = [] # list to store favourite TV shows
	oldShows = [] # list to store the downloaded shows
	loadFile("favouriteshows.txt")
	loadFile("oldshows.txt")

	#pdb.set_trace()
	# Extract eztv frontpage into parser.urls
	try:
		usock = urllib.urlopen('http://www.eztv.it')
		parser = urllister.URLLister()
		parser.feed(usock.read())
		usock.close()
		parser.close()
		timeoutHasOccurred = 0
	except:
		print "Timeout accessing www.eztv.it.\n Trying again in 15 mins..."
		timeoutHasOccurred = 1

	# find episodes needing to be downloaded
	if timeoutHasOccurred == 0:
		dicUrl.clear()
		for url in parser.urls:
			if nextLine == 1:				# we want to pickup the url record
				nextLine= 0					# since we picked up the url reset till we find the next episode record	
				dicUrl[saveUrl] = url	
			if url.find('/ep/') != -1 and url.find('720p') == -1 and url.find('x264') == -1:
				if url + '\n' not in oldShows:	 # make sure we have not downloaded this episode already
					for show in favouriteShows:
						cleanShow = show.strip('\n')
						findErr = url.find(cleanShow)
						if findErr > 1:			# is this a show that we like to watch 
							nextLine = 1		# we also want to pickup the next record that contains the url
							saveUrl = url
					
	# Download torrent for episode
		for name, address in dicUrl.items():			
			writeEpisodetoOldShows(name+'\n')	#write episode to oldshows file
			savedPath =	changeDir(newPath)				# save current path and change path to torrent path
			file_name = address.split('/')[-1]			# removes the last '/'
			createTorrent(file_name, address)			# process creates torrent file. 
			revertDir(savedPath)						# revert back to original path
		
		
		
	# Delay for 15 minutes before checking again 
	time.sleep(900)
	count = count + 1
	print 'Run No. %i ' % (count,)