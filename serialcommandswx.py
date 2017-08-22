#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Serial Commands sends commands to comm ports. The commands
are identified in a configuration file.
"""
 
# serialcommandswx.py

import logging
import wx
import os, sys
from datetime import date
from time import ctime

from tombo.configfile import ConfigFile
from serialcommands import SerialCommands
#from tombo.timedstatusbar import TimedStatusBar

class MainWindow(wx.Frame):
	""" A frame that encloses a panel which encloses widgets. """
	def __init__(self, parent, title):
		""" Use the constructor to build the interface and show the window. """
		super(MainWindow, self).__init__(parent, title=title, size=(650, 400))
		self.gatherConfigInfo('serialcommandswx.conf')
		self.sc = SerialCommands(self.ports)
		self.widgetids = {}
		self.monitorwidgetids = []
		self.InitUI()
		self.Centre()
		self.Show()

	def gatherConfigInfo(self, configfile):
		config = ConfigFile(configfile)
		self.ports = config.getItems('Ports')
		self.commands = config.getItems('Commands')
		self.command_sequences = config.getItems('Command Sequences')
		self.buttons_per_row_max = config.getNumber('Misc', 'buttons_per_row_max')
		self.button_labels = config.getItems('Button Labels')
		self.poll_interval = config.getNumber('Misc', 'poll_interval')
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.setStatusMessage, self.timer)

	def InitUI(self):
		""" Organizes building the interface. """
		# Top level panel - holds all other windows
		vbox1 = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self)
		vbox1.Add(item=panel, proportion=1, flag=wx.ALL|wx.EXPAND)
		self.SetSizer(vbox1)
		vbox2 = wx.BoxSizer(wx.VERTICAL)
		panel.SetSizer(vbox2)
		vbox2.Add(item=self.buildButtonGrid(panel, self.button_labels), flag=wx.CENTER|wx.TOP, border=40)
		self.buildStatusBar()
		self.timer.Start(self.poll_interval)

	def buildStatusBar(self):
		""" Build a lowly status bar. """
		self.statusbar = wx.StatusBar(self)
		self.statusbar.SetFieldsCount(3)
		self.SetStatusBar(self.statusbar)

	def buildButtonGrid(self, parent, button_labels):
		fields = self.buildButtonFields(parent, button_labels)
		row_count = len(fields) / self.buttons_per_row_max
		if (len(fields) % self.buttons_per_row_max) > 0:
			row_count += 1
		entrygrid = wx.FlexGridSizer(rows=row_count, cols=self.buttons_per_row_max, hgap=3, vgap=10)
		entrygrid.AddMany(fields)
		return entrygrid

	def buildButtonFields(self, parent, button_labels):
		button_fields = []
		for button_name, button_data in button_labels.iteritems():
			button_data = button_data.split('|')
			if button_data[1]:
				button = wx.Button(parent=parent, label=button_data[0])
				button.Bind(wx.EVT_BUTTON, self.onButtonClick, id=button.GetId())
				self.widgetids[button.GetId()] = button_data[3]
				if button_data[4] == 'Y':
					self.monitorwidgetids.append([button.GetId()])
				button_fields.append((button))
		logger.info('widget ids created')
		print(self.monitorwidgetids)
		button = wx.Button(parent=parent, label='&Quit')
		button.Bind(wx.EVT_BUTTON, self.onQuit, id=button.GetId())
		button_fields.append((button))
		return button_fields
  
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

	def setStatusMessage(self, event):
		self.statusbar.SetStatusText(ctime(), 2)

if __name__ == '__main__':
	logger = logging.getLogger('SERIALCOMMANDSWX')
	logger.setLevel(logging.INFO)
	log_format = '%(asctime)s:%(lineno)s:%(levelname)s:%(name)s:%(message)s'
	formatter = logging.Formatter(log_format)
	file_handler = logging.FileHandler('serialcommandswx.log')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	app = wx.App()
	MainWindow(None, title='Serial Commands')
	app.MainLoop()
