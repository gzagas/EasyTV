#!/usr/bin/env python
# encoding: utf-8
"""
urllister.py

Created by George on 2011-04-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from sgmllib import SGMLParser
#import pdb

class URLLister(SGMLParser):
	def reset(self):
		#pdb.set_trace()
		SGMLParser.reset(self)
		self.urls = [ ]
		
	def start_a(self, attrs):
		#pdb.set_trace()
		href = [v for k, v in attrs if k == 'href']
		
		if href:
			self.urls.extend(href)