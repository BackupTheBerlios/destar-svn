# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Holger Schurig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import sys, os, time, string, socket, asyncore, asynchat
import configlets, backend 

#
# Oh, this beast is complex. In order to be able to comprehend it in
# two months I have to describe it.
#
# Initial connection and login
# ============================
#
#
# When we create the object, __init__() calls do_connect() which
# in turn connects to Asterisk, similar to the telnet session below:
#	$ telnet 127.0.0.1 5038
#	Trying 127.0.0.1...
#	Connected to localhost.localdomain (127.0.0.1).
#	Escape character is '^]'.
# Now we're connected. And Asterisk sends immediately it's header:
#	Asterisk Call Manager/1.0
# All text that we got is coming in via collect_incoming_data() and appended
# to buffer[]. In do_connect() we used set_terminator() to define that our
# chunk of data is finished after an CR/LF sequence. This has the effect
# that now found_terminator() get's called which can operator on buffer[].
#
# It looks for all lines and string-of-lines in buffer[] to see if there is
# an "ActionID: " in it. If yes, we store that in the local 'id' variable.
# If it is, we store all of the data in the dictionary 'action_data'.
#
# In this case, it's not, so we don't store anything.
#
# Instead, we see see that our data is exactly 'Asterisk Call Manager/1.0'.
# So we know that we have to login now. We change the terminator to the
# character sequence that marks an empty line and call call_nowait() with
# the action 'Login' and our login credentials. Therefore we send something
# like this:
#
#	Action: Login
#	ActionID: destar-16384-00000001
#	Username: destar
#	Secret: destar
#
# Assuming that the login was successfully, Asterisk sends something
# back:
#	
#	Response: Success
#	ActionID: destar-16384-00000001
#	Message: Authentication accepted
#
# Again the data ends in chunks in collect_incoming_data(), which put's
# it into buffer[] and once the empty line after the this data has been
# received, the function found_terminator() gets called.
#
# This time, found_terminator() find's an ActionID and therefore stores
# the whole 'data' into action_data[id].
#
# While all of this happens, the do_connect() method was running
# asyncore.poll() in a loop, which makes asyncore call all of the even
# handlers like collect_incoming_data() or found_terminator() for us. This
# polling loop also tests if the the action id 'destar-%d-00000001' is in
# the action_data[]. As soon as it it, the loop terminates.
#
# Now we have the data inside do_connect(), without the use of any not-so-
# easy-to-handle callback function. We now test in data if we find
# "Response: Error" and set 'loggedin' accordingly.
#	
#
# Calls to manager actions
# ========================
#
# Now suppose we're logged in and want to call manager methods. We do this
# by calling call(action, args). For example:
#	mgr.call('Ping')
#	mgr.call('Command', Command='sip show peers')
#
# Now almost the same happens as above, only that our poll-loop is now
# in call(), not in do_connect().
#

class ManagerClient(asynchat.async_chat):

	def __init__(self, username, password):
		asynchat.async_chat.__init__(self)
		self.address = ('127.0.0.1',5038)
		self.buffer = []
		self.action_data = {}
		self.loggedin = False
		self.reconnect = False
		self.username = username
		self.password = password
		res = self.do_connect()


	def do_connect(self):
		"""Tries to connect, and implicitly to login. If that does
		work, we set self.loggedin to True."""

		#print "do_connect()"
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_terminator('\r\n')
		self.connect(self.address)

		self.seq = 0
		self.loggedin = False
		id = 'destar-%d-%08x' % (os.getpid(), 1)
		n = 0
		while not self.closing and n<20:
			if self.action_data.has_key(id) and self.action_data[id]:
				#print "do_connect() id", id, "found in action_data"
				break
			#print "do_connect() sleep, id:", id, "action_data:", self.action_data
			asyncore.poll(0.5, asyncore.socket_map)
			n = n + 1
		#print "do_connect() done with while"
		if self.action_data.has_key(id):
			self.loggedin = self.action_data[id][0].find("Response: Success") != -1
			#print "do_connect(), loggedin:", self.loggedin
		

	def close(self):
		"""Close event callback from asyncore/asynchat."""

		#print "close()"
		asynchat.async_chat.close(self)
		self.loggedin = False
		if self.reconnect:
			#print "close(), about to reconnect"
			self.do_connect()


	def handle_connect(self):
		"""Connect callback from asyncore/asynchat."""
	
		#print "handleconnected()"
		pass


	def handle_error(self):
		"""Exception callback from asyncore/asynchat."""

		self.closing = True
		t, v, tb = sys.exc_info()
		#print "handle_error(), t:",t
		#print "handle_error(), v:",v
		#print "handle_error(), tb:",tb
		#while tb:
		#	#print tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name, tb.tb_lineno
		#	tb = tb.next
		if t != socket.error:
			asynchat.async_chat.handle_error(self)


	def collect_incoming_data(self, data):
		"""Data callback from asyncore."""

		#print "incoming_data(), data:", data
		self.buffer.append(data)


	def handle_event(self, data):
		#print "handle_event()", "-"*40
		for l in data:
		#	print l
			continue
		#print


	def found_terminator(self):
		"""Data completed callback from asyncore."""

		id = None
		data = []
		for l in self.buffer:
			for ll in l.split('\n'):
				data.append(ll.strip())
				#print "found_terminator(), ll:", ll
				if ll.startswith("ActionID: "):
					id = ll[10:].strip()
					#print "found_terminator(), id:", id
		self.buffer = []

		#print "found_terminator()", "-"*40
		#for l in data: print l
		#print

		if data[0].startswith("Event: "):
			self.handle_event(data)

		if self.action_data.has_key(id):
			self.action_data[id] = data

		if data[0]=="Asterisk Call Manager/1.1":
			self.set_terminator('\r\n\r\n')
			self.call_nowait('Login', Username=self.username, Secret=self.password)


	def call_nowait(self, action, **args):
		"""This calls an Asterisk management command. It does not wait for any
		response, therefore it assumes that some other code calls asyncore.loop()
		or asyncore.poll() to keep the event callbacks happening."""

		self.seq = self.seq + 1
		id = 'destar-%d-%08x' % (os.getpid(), self.seq)
		#print "call_nowait(), id", id, "to None"
		self.action_data[id] = None
		self.push('Action: %s\r\n' % action)
		self.push('ActionID: %s\r\n' % id)
		for k in args:
			self.push('%s: %s\r\n' % (k,args[k]))
		self.push('\r\n')
		return id


	def call(self, action, **args):
		"""Executes a manager action, wait's until completion and
		returns the result as an array of strings."""

		id = self.call_nowait(action,**args)
		while not self.action_data[id]:
			#print "call(), sleep"
			asyncore.poll(0.1,asyncore.socket_map)
		res = self.action_data[id]
		#print "call(), delete",id,"in action_data"
		del self.action_data[id]
		return res


	def action(self, act, **args):
		"""Like call, but strips unneeded strings from the array."""

		#res = map(string.strip, self.call(act,**args).split('\n'))
		res = self.call(act, **args)
		#print "action(), res:", res
		if res[1].startswith('ActionID:'):
			del res[1]
		if res[0]=='Response: Follows':
			del res[0]
			del res[-1]
		elif res[0].startswith('Response: '):
			res[0] = res[0][10:]
		return res
		


def normalizeChannel(val):
	#print "normalizeChannel() with", val, type(val)
	if val.startswith('CAPI'):
		i = val.index('/')
		j = val.index(']')
		channel = "CAPI/%s.%s" % (val[i+1:j], val[j+2:])
	if val.startswith('IAX2'):
		i = val.find(':')
		channel = val[:i]
	else:
		channel = val[:-5]
	return channel


channels = {}
registry = {}
messages = {}

class ManagerEvents(ManagerClient):

	def handle_event(self, data):
		# First we convert the array into a dict:

		dict = configlets.Holder()
		#print "handle_event(), data:", data
		for s in data:
			if not s: continue
			#print "handle_event(), s: '%s'" % s
			# We can't use s.split(':') because of "Channel: IAX2/65.39.205.121:4569/1"
			i = s.find(':')
			if i==-1:
				key = s
				val = ""
			else:
				key = s[:i]
				val = s[i+1:].strip()
			dict[key] = val.strip()
		#print "handle_event(), dict:", dict
	
		# When we look if we have a handler function

		func = 'handle_%s' % dict['Event']
		try:
			exec "self.%s(dict)" % func
			#print "--> Called", func
		except AttributeError:
			#print "handle_event(), no method for", func
			for s in data:
				if not s: continue
				#print "", s
				continue
			return

		# Complete dump of all channel data
		for s in channels:
			#print "Channel", s
			obj = channels[s]
			for item in obj.__dict__:
				#print " ", item, obj[item]
				continue
		#print


	def updateChannels(self, dict):
		global channels
		chan = channels.setdefault(dict.Channel, configlets.Holder() )
		chan.__dict__.update(dict)
		chan.LastUpdate = time.time()


	def handle_Newchannel(self,dict):
		# Event: Newchannel
		# Channel: SIP/dnarotam-32a9
		# State: Ring
		# Callerid: Dave Narotam <26>
		# Uniqueid: 1091801704.50

		# Event: Newchannel
		# Channel: AsyncGoto/SIP/Doorphone-71bd
		# State: Up
		# Callerid: <unknown>
		# Uniqueid: 1091804181.95

		# reap old, hangup channels :-)
		global channels
		reapchannel = normalizeChannel(dict.Channel)
		toreap = []
		for c in channels:
			if c.startswith(reapchannel) and channels[c].State == 'Hangup':
				toreap.append(c)
		# we can't delete in one go, because then the dictionary size changes :-(
		for c in toreap:
			del channels[c]

		self.updateChannels(dict)


	handle_Newexten = updateChannels
		# Event: Newexten
		# Channel: SIP/dnarotam-b9ce
		# Context: out-intl
		# Extension: 91
		# Priority: 1
		# Application: Answer
		# AppData:
		# Uniqueid: 1091802458.64



	handle_Newstate = updateChannels
		# Event: Newstate
		# Channel: SIP/dnarotam-b9ce
		# State: Up
		# Callerid: Dave Narotam <26>
		# Uniqueid: 1091802458.64


	handle_Newcallerid = updateChannels
		# Event: Newcallerid
		# Channel: SIP/hschurig-b5e0
		# Callerid: "Holger Schurig" <254041>
		# Uniqueid: 1091822010.3


	def handle_Hangup(self, dict):
		#  Event: Hangup
		#  Channel: SIP/dnarotam-7209
		#  Uniqueid: 1091802667.65
		#  Cause: 0

		global channels

		if dict.Channel.endswith('<ZOMBIE>'):
			del channels[dict.Channel]
			return

		chan = channels.setdefault(dict.Channel, configlets.Holder() )

		chan.State      = 'Hangup'
		chan.Cause      = dict.Cause
		chan.Uniqueid   = dict.Uniqueid
		chan.LastUpdate = time.time()

		for s in [
			'AppData',
			'Application',
			'Callerid',
			'Channel',
			'Context',
			'Event',
			'Extension',
			'Priority',
			'Uniqueid',
			'Usernum',
			'Meetme',
		]:
			try:
				del chan.__dict__[s]
			except KeyError:
				#print "could not delete", s
				pass


	def handle_Link(self, dict):
		# Event: Link
		# Channel1: SIP/dnarotam-3533
		# Channel2: SIP/Doorphone-5180
		# Uniqueid1: 1091803550.81
		# Uniqueid2: 1091803550.82

		global channels
		chan = channels.setdefault(dict.Channel1, configlets.Holder() )
		chan.Link       = dict.Channel2
		chan.LastUpdate = time.time()
		chan = channels.setdefault(dict.Channel2, configlets.Holder() )
		chan.Link       = dict.Channel1
		chan.LastUpdate = time.time()


	def handle_Unlink(self, dict):
		# Event: Unlink
		# Channel1: SIP/dnarotam-3533
		# Channel2: SIP/Doorphone-5180
		# Uniqueid1: 1091803550.81
		# Uniqueid2: 1091803550.82

		global channels
		chan = channels.setdefault(dict.Channel1, configlets.Holder() )
		chan.LastUpdate = time.time()
		try:
			del chan.__dict__['Link']
		except KeyError:
			# This can happen when we start DeStar while Asterisk has connections
			pass

		chan = channels.setdefault(dict.Channel2, configlets.Holder() )
		chan.LastUpdate = time.time()
		try:
			del chan.__dict__['Link']
		except KeyError:
			pass


	def handle_Rename(self, dict):
		#  Event: Rename
		#  Oldname: SIP/Doorphone-985e
		#  Newname: SIP/Doorphone-985e<MASQ>

		global channels
		chan = channels.setdefault(dict.Oldname, configlets.Holder() )
		chan.LastUpdate = time.time()

		# We can't rename, so we have to do an add/delete operation
		channels[dict.Newname] = chan
		del channels[dict.Oldname]

		# Rename the links as well:
		try:
			linked = channels[chan.Link]
			linked.Link = dict.Newname
			linked.LastUpdate = time.time()
		except:
			pass


	handle_MeetmeJoin = updateChannels
		# Event: MeetmeJoin
		# Channel: SIP/dnarotam-1d0e
		# Uniqueid: 1091810161.184
		# Meetme: 1
		# Usernum: 1


	handle_MeetmeLeave = updateChannels
		# Event: MeetmeLeave
		# Channel: SIP/dnarotam-1d0e
		# Uniqueid: 1091810161.184
		# Meetme: 1
		# Usernum: 1


	def handle_PeerStatus(self,dict):
		# Event: PeerStatus
		# Peer: SIP/Doorphone
		# PeerStatus: Registered
		
		global registry
		reg = registry.setdefault(dict.Peer, configlets.Holder() )
		reg.__dict__.update(dict)
		reg.LastUpdate = time.time()

		for s in registry:
			#print "Registry", s
			obj = registry[s]
			for item in obj.__dict__:
				#print " ", item, obj[item]
				continue
		#print


	def handle_MessageWaiting(self, dict):
		# Event: MessageWaiting
		# Mailbox: 23@default
		# Waiting: 1

		# normalize Mailbox
		if dict.Mailbox.endswith('@default'):
			dict.Mailbox = dict.Mailbox[:-8]

		global messages
		msg = messages.setdefault(dict.Mailbox, configlets.Holder() )
		msg.__dict__.update(dict)
		msg.LastUpdate = time.time()

		for s in messages:
			#print "Message", s
			obj = messages[s]
			for item in obj.__dict__:
				#print " ", item, obj[item]
				continue
		#print


	def handle_Shutdown(self, dict):
		# Event: Shutdown
		# Shutdown: Cleanly
		# Restart: False

		global channels
		channels = {}
		global registy
		registry = {}

		#self.close()
		#self.do_connect()
		self.reconnect = True


	def handle_Reload(self, dict):
		# Event: Reload
		# Message: Reload Requested

		pass



conn = None

def connect(username=None,password=None):
	global conn
	if conn and conn.loggedin: return

	# determine credentials to use for login
	if not username and not password:
		for mgr in backend.getConfiglets(name="CfgOptManager"):
			# use first username/password
			if not username: username = mgr.name
			if not password: password = mgr.secret
			# or use destar/password if one is found
			if mgr.name=="destar":
				username = mgr.name
				password = mgr.secret
				break
	if not username and not password:
		# We couldn't log in
		print "***** manager cant login"
		return

	conn = ManagerEvents(username,password)
	if not conn.loggedin:
		conn.close()
		conn = None


def isConnected():
	global conn
	return conn and conn.connected


def isLoggedIn():
	global conn
	return isConnected() and conn.loggedin


def getVar(family, key, default):
	for s in conn.action('Command', Command='database get %s %s' % (family,key)):
		if s.startswith('Value: '):
			return s[7:]
	return default

def setVar(family, key, val):
	if val:
		conn.action('Command', Command='database put %s %s %s' % (family,key,val))
	else:
		conn.action('Command', Command='database del %s %s' % (family,key))

def originateCallApp(channel,application,data):
	return conn.action('Originate', Channel=channel, Application=application)

def originateCallExt(channel,context,extension,priority,callerid):
	return conn.action('Originate', Channel=channel, Context=context, Exten=extension, Priority=priority, CallerID=callerid)

def getVarFamily(family):
	varlist = []
	for s in conn.action('Command', Command='database show %s' % family):
		if s.startswith("/%s" % family):
			varlist.append(s[len(family)+2:])
	return varlist
	
def getSIPPeers():
	return conn.action('Command', Command='sip show peers')


def checkMailBox(ext):
	vmstate = {}
	for s in conn.action('MailboxCount', Mailbox=ext):
		if s.startswith('NewMessages: '):
			vmstate['New'] = s[13:]
		if s.startswith('OldMessages: '):
			vmstate['Old'] = s[13:]
	return vmstate
	
def reloadAsterisk():
	return conn.action('Command', Command='reload')

def reloadMoH():
	return conn.action('Command', Command='moh reload')

if __name__ == '__main__':
	connect()
	if not isConnected():
		print "Not connected"
	else:
		res = []

		############################ manager.c:

		# Action:     Ping
		# Parameters: none
		#res = conn.action('Ping')

		# Action:     ListCommands
		# Parameters: none
		#res = conn.action('ListCommands')

		# Action:     Events
		# Parameters: EventMask (on, off, system,call,log etc)
		#res = conn.action('Events', EventMask='off'

		# Action:     Logoff
		# Parameters: none
		#res = conn.action('Logoff')

		# Action:     Hangup
		# Parameters: Channel
		#res = conn.action('Hangup', ...)

		# Action:     SetVar
		# Parameter:  Channel, Variable, Value
		#res = conn.action('SetVar', ...)

		# Action:     GetVar
		# Parameter:  Channel, Variable
		#res = conn.action('GetVar', ...)

		# Action:     Status
		# Parameter:  Channel
		#res = conn.action('Status', Channel=...)

		# Action:     Redirect
		# Parameters: Channel, ExtraChannel, Exten, Context, Priority
		#res = conn.action('Redirect', ...)

		# Action:     Command
		# Parameters: Command
		res = conn.action('Command', Command='show channels concise')

		# Action:     Originate
		# Parameters: Channel, Exten, Context, Priority, Timeout (in ms),
		#             CallerID, Variable, Account, Application, Data, Async
		#res = conn.action('Originate', Channel='SIP/dnarotam', Application='Milliwatt')

		# Action:     MailboxStatus
		# Parameters: Mailbox
		#res = conn.action('MailboxStatus', Mailbox='1234')

		# Action:     MailboxCount
		# Parameters: Mailbox
		#res = conn.action('MailboxCount', Mailbox='1234')

		# Action:     ExtenstionState
		# Parameters: Exten, Context
		#res = conn.action('ExtensionState', Exten='26', Context='default')

		# Action:     Timeout
		# Parameters: Channel, Timeout (in ms?)
		#res = conn.action('Timeout', Timeout=30)


		############################ apps/app_queue.c:

		# Action:     Queues
		# Parameters: none
		#res = conn.action('Queues')

		# Action:     QueueStatus
		# Parameters: none
		#res = conn.action('QueueStatus')


		############################ apps/app_setcdruserfield.c:

		# Action:     SetCDRUserField
		# Parameters: Channel, UserField, Append


		############################ channels/chan_iax.c:

		# Action:     IAX1peers
		# Parameters: none


		############################ channels/chan_iax2.c:

		# Action:     IAXpeers
		# Parameters: none


		############################ channels/chan_zap.c:

		# Action:     ZapTransfer
		# Parameters: ZapChannel

		# Action:     ZapHangup
		# Parameters: ZapChannel

		# Action:     ZapDialOffhook
		# Parameters: ZapChannel

		# Action:     ZapDNDon
		# Parameters: ZapChannel

		# Action:     ZapDNDoff
		# Parameters: ZapChannel

		# Action:     ZapShowChannels
		# Parameters: none


		############################ res/res_monitor.c

		# Action:     Monitor
		# Parameters: Channel, File, Format, Mix

		# Action:     StopMonitor
		# Parameters: Channel

		# Action:     ChangeMonitor
		# Parameters: Channel, File


		############################ res/res_features.c:

		# Action:     ParkedCalls
		# Parameters: none


		############################ app_valetparking.c:

		# Action:     ValetparkedCalls
		# Parameters: none


		for s in res:
			print s

		print "Waiting for events ...\n"
		try:
			asyncore.loop()
		except KeyboardInterrupt:
			pass
