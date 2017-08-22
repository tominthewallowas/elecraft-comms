#!/usr/bin/python
# -*- coding: utf-8 -*-

# monitorradio.py

import logging
import wx
import os, sys
from datetime import date
from time import ctime

from tombo.configfile import ConfigFile
from serialcommands import SerialCommands
#from tombo.timedstatusbar import TimedStatusBar
import elecraft

''' Responses from the MD; command:
	Voice Modes:	LSB = 1, USB = 2, AM = 5
	CW Modes:		CW = 3, CW-REV = 7
	DATA Modes:		DATA = 6, DATA-REV = 9
'''

modes = {
	'MD1;':['VOICE_MODE', 'LSB'],
	'MD2;':['VOICE_MODE', 'USB'],
	'MD5;':['VOICE_MODE', 'AM'],
	'MD3;':['CW_MODE', 'CW'],
	'MD7;':['CW_MODE', 'CW-REV'],
	'MD6;':['DATA_MODE', 'DATA'],
	'MD9;':['DATA_MODE', 'DATA-REV']
}

class MainWindow(wx.Frame):
	""" A frame that encloses a panel which encloses widgets. """
	def __init__(self, parent, title):
		""" Use the constructor to build the interface and show the window. """
		super(MainWindow, self).__init__(parent, title=title, size=(650, 400))
		self.gatherConfigInfo('serialcommandswx.conf')
		self.sc = SerialCommands(self.ports)
		self.InitUI()
		self.Centre()
		self.Show()

	def gatherConfigInfo(self, configfile):
		config = ConfigFile(configfile)
		self.ports = config.getItems('Ports')
		self.poll_interval = config.getNumber('Misc', 'poll_interval')
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.checkStatus, self.timer)

	def InitUI(self):
		""" Organizes building the interface. """
		# Top level panel - holds all other windows
		vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.panel = wx.Panel(self)
		vbox1.Add(item=self.panel, proportion=1, flag=wx.ALL|wx.EXPAND)
		self.SetSizer(vbox1)
		vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.panel.SetSizer(vbox2)
		vbox2.Add(item=self.buildLabelGrid(self.panel), flag=wx.CENTER|wx.TOP, border=40)
		
		self.buildStatusBar()
		self.timer.Start(self.poll_interval)

	def buildLabelGrid(self, owner):
		label_grid = wx.FlexGridSizer(rows=2, cols=2, hgap=3, vgap=10)
		label_grid.AddMany(self.buildLabels(owner))
		return label_grid

	def buildLabels(self, owner):
		return [
			(wx.StaticText(owner, id=wx.ID_ANY, label='Test Mode'), 0),
			(wx.StaticText(owner, id=wx.ID_ANY, label='On'), 0),
			(wx.StaticText(owner, id=wx.ID_ANY, label='VOX'), 0),
			(wx.StaticText(owner, id=wx.ID_ANY, label='On'), 0),
		]

	def buildStatusBar(self):
		""" Build a lowly status bar. """
		self.statusbar = wx.StatusBar(self)
		self.statusbar.SetFieldsCount(3)
		self.SetStatusBar(self.statusbar)

  
	# Methods related to a button click
	def onQuit(self, event):
		self.sc.closePorts()
		self.Close()

	def onButtonClick(self, event):
		eventid = event.GetId()
		
		self.runCommand(self.widgetids[eventid])

	def runCommand(self, command):
		command_names = self.command_sequences[command].split('|')
		for command_name in command_names:
			command_list = self.commands[command_name].split('|')
			self.sc.runCommand(command_list)

	def checkStatus(self, event):
		self.statusbar.SetStatusText(ctime(), 2)
		numeric_mode = self.sc.readPort(['COM13', 'MD;'])
		mode_main_specific = modes.get(numeric_mode)
		self.statusbar.SetStatusText(mode_main_specific[0], 0)
		self.statusbar.SetStatusText(mode_main_specific[1], 1)
		response = self.sc.readPort(['COM13', 'IC;'])
		status = elecraft.listifyHexstring(response)
		print(status)
		


if __name__ == '__main__':
	logger = logging.getLogger('SERIALCOMMANDSWX')
	logger.setLevel(logging.INFO)
	log_format = '%(asctime)s:%(lineno)s:%(levelname)s:%(name)s:%(message)s'
	formatter = logging.Formatter(log_format)
	file_handler = logging.FileHandler('serialcommandswx.log')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	app = wx.App()
	MainWindow(None, title='Monitor Radio')
	app.MainLoop()
