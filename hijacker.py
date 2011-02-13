# -*- coding: utf-8 -*-
# Copyright © 2010 Flávio Sales Truzzi
#
# This file is part of HiJacker.
#
# HiJacker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# HiJacker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HiJacker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from scapy.all import *
import sys, os, eyeD3, pygtk
pygtk.require('2.0')
import pynotify

class HiJacker():
	"""
	HiJack streams
	"""
	
	def __init__(self):
		self.port = ""
		self.ip = ""
		self.size = 0
		self.counter = 0
		self.packets = []		
		sniff(filter="tcp port 80", prn=self.callback)
		
	def callback(self,packet):		
		if hasattr(packet, 'load'):
			if "audio/mpeg" in packet.load:
				if (len(self.packets) > 0):
					self.dumpPackets()
				self.report("HiJacking!")
				self.port = packet.payload.payload.dport
				self.ip = packet.payload.src
				
				for key in packet.load.split("\r\n"):
					if ("Content-Length" in key):
						self.size = int(key.split()[1])						
						break
			if packet.payload.payload.dport == self.port and packet.payload.src == self.ip:
				self.packets.append(packet)
				self.counter += len(packet.load)
				if (self.counter >= self.size):
					self.dumpPackets()
					
	def dumpPackets(self):					
		temp = open('tempHiJacker.mp3','w')
		for packet in self.packets[1:]:
			temp.write(packet.load)
		temp.close()
		audioFile = eyeD3.Mp3AudioFile('tempHiJacker.mp3')
		tag = audioFile.getTag()
		artist = tag.getArtist()
		title = tag.getTitle()
		self.port = ""
		self.ip = ""
		self.size = 0
		self.counter = 0
		self.packets = []
		
		if (artist != None and title != None):
			if (len(artist) + len(title) > 3):
				message = artist + ' - ' + title + '.mp3'
				os.rename('tempHiJacker.mp3',message)				
				self.report(message)
			else:
				alphabet = 'abcdefghijklmnopqrstuvwxyz'
				message = ''
				for x in random.sample(alphabet,random.int(5,100)):
					message += x
				os.rename('tempHiJacker.mp3',message)
				self.report("Not possible to get ID3 information random name generated:" + message)
			
	def report(self, message):					
		if not pynotify.init("Basics"):
			sys.exit(1)
		
		n = pynotify.Notification("HiJacker", message)
		
		if not n.show():
			print "Failed to send notification"
			sys.exit(1)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	