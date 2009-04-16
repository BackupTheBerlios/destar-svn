# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005-2007 by Holger Schurig
# This file has Copyright (C) 2007 by Alejandro Rios P.
#
# The loadQueue method has some GPL code with
# Copyright (C) 2006 Earl Terwilliger  earl@micpc.com
# Tooked from Asterisk Queue Log Analyzer http://www.micpc.com/qloganalyzer/ 
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


import sys, os, string, time, re
from datetime import datetime
from time import strptime

class PRILogData:
	def __init__(self):
		#self.protocol_discriminator = ""
		self.reference = ""
		self.message_type = ""
		self.calling_number = 0
		self.called_number = 0
		self.progress_indicator = ""
		self.channel = 0
		self.display = ""
		self.cause = 0
		self.other_info = ""
		self.incoming = False
		self.outgoing = False
		self.messages = 0
	
	def addQueueCall(self, holdtime=0, calltime=0, disp=""):
		self.calls_number += 1
		self.seconds += int(calltime)
		self.holdtime += int(holdtime)
		if disp == "COMPLETEAGENT":
			self.completed_by_agent += 1
		elif disp == "COMPLETECALLER":
			self.completed_by_caller += 1
		elif disp == "uncompleted":
			self.uncompleted += 1


#try:
#	from pysqlite2 import dbapi2 as sqlite
#except ImportError:
#	print _("Note: you should install python-pysqlite2 to have Queue Stats functionality")

#try:
#	db_fn = "/var/log/asterisk/prilog.db"
#	if not os.access(db_fn, os.O_RDWR):
#		raise ImportError
#	db = sqlite.connect(db_fn)
#	db.isolation_level = None
#except:
#	print _("Note: you don't seem to have access to %s. See INSTALL.txt for details.") % db_fn
#	if __name__ == "__main__": sys.exit(0)
#	db = None

def loadPRILog ():
	try:
		q_fn = "/var/log/asterisk/pri_log"
		if not os.access(q_fn, os.O_RDWR):
			raise ImportError
	except:
		print _("Note: you don't seem to have access to %s.") % q_fn
		if __name__ == "__main__": sys.exit(0)

#	cursor = db.cursor()
	last_id = 227
	message_id=last_id+1
	rows = 0
	in_file = open(q_fn,"r")
	messages={}
	re_call_ref = re.compile(r'(.*)reference ((\d*)/0x([0-9a-fA-F]*))(.*)')
	re_msg_type = re.compile(r'(.*)Message type: ((\w*)\s(\w*))(.*)')
	re_calling = re.compile(r'(.*)Presentation: (.*)\'(\d*)\'(.*)')
	re_called = re.compile(r'(.*)Called Number (.*)\'(\d*)\'(.*)')
	re_cause = re.compile(r'(.*)Cause: (\D*)(\d*)(.*) ]')

	try:
		for in_line in in_file:
			if in_line.find("Protocol Discriminator") > 0:
				message_id += 1
				messages[message_id] = PRILogData()
			if in_line.startswith("< "):
				messages[message_id].incoming=True
			elif in_line.startswith("> "):
				messages[message_id].outgoing=True
			if in_line.find("Call Ref") > 0:
				m = re_call_ref.search(in_line)
				if m:
					messages[message_id].reference = m.groups()[1]
			if in_line.find("Message type") > 0:
				m = re_msg_type.search(in_line)
				if m:
					messages[message_id].message_type = m.groups()[1]
			if in_line.find("Presentation") > 0:
				m = re_calling.search(in_line)
				if m:
					messages[message_id].calling_number = m.groups()[2]
			if in_line.find("Called Number") > 0:
				m = re_called.search(in_line)
				if m:
					messages[message_id].called_number = m.groups()[2]
			if in_line.find("Cause:") > 0:
				m = re_cause.search(in_line)
				if m:
					messages[message_id].cause = m.groups()[2]
	finally:
		in_file.close()
	print "================================"
	print "========First Report (A)========"
	print "================================"
	for message_id in messages.keys():
		print "A: id: %s, in: %s, out: %s, call_ref=%s, mt: %s, calling: %s, called: %s, cause: %s" % (message_id, messages[message_id].incoming, messages[message_id].outgoing, messages[message_id].reference, messages[message_id].message_type, messages[message_id].calling_number, messages[message_id].called_number, messages[message_id].cause)
		rows += 1
#	sys.stderr.write("[%s] prilog.db: %d rows were inserted\n" % (time.asctime(time.localtime()),(rows)))
	print "============================================"
	print "========Second Report (B),  cause 27 ======="
	print "============================================"
	for id1 in messages.keys():
		if messages[id1].cause == '27':
			for id2 in messages.keys():
				if messages[id2].reference == messages[id1].reference:
					if messages[id2].calling_number != 0:
						print "B. call_ref: %s, calling: %s, called: %s, id1: %s, id2: %s" % (messages[id1].reference, messages[id2].calling_number, messages[id2].called_number, id1, id2)
			
	return rows

	#s[0] = s[0].isoformat(' ')
		#try:
	#		cursor.execute( "INSERT INTO prilog (timestamp,callid,qname,agent,action,info1,info2,info3) VALUES  ('%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(s) )
	#	except:
	#		sys.stderr.write("[%s] queue.db: Failed to execute insert at timestamp %s\n" % (time.asctime(time.localtime()), s[0]))
	#		if __name__ == "__main__": sys.exit(0)

def loadPRILog2 ():
	try:
		q_fn = "/var/log/asterisk/pri_log"
		if not os.access(q_fn, os.O_RDWR):
			raise ImportError
	except:
		print _("Note: you don't seem to have access to %s.") % q_fn
		if __name__ == "__main__": sys.exit(0)

	cursor = db.cursor()
	message_id=0
	rows = 0
	in_file = open(q_fn,"r")
	calls={}
	re_call_ref = re.compile(r'(.*)reference ((\d*)/0x([0-9a-fA-F]*))(.*)')
	re_msg_type = re.compile(r'(.*)Message type: ((\w*)\s(\w*))(.*)')
	re_calling = re.compile(r'(.*)Presentation: (.*)\'(\d*)\'(.*)')
	re_called = re.compile(r'(.*)Called Number (.*)\'(\d*)\'(.*)')
	#re_cause = re.compile(r'(.*)Cause: (.*) ]')
	re_cause = re.compile(r'(.*)Cause: (\D*)(\d*)(.*) ]')

	try:
		for in_line in in_file:
			if in_line.find("Call Ref") > 0:
				m = re_call_ref.search(in_line)
				if m:
					call_ref = m.groups()[1]
					if not calls.has_key(call_ref):
						calls[call_ref] = PRILogData()
					calls[call_ref].messages += 1
			if in_line.find("Presentation") > 0:
				m = re_calling.search(in_line)
				if m:
					calls[call_ref].calling_number = m.groups()[2]
			if in_line.find("Called Number") > 0:
				m = re_called.search(in_line)
				if m:
					calls[call_ref].called_number = m.groups()[2]
			if in_line.find("Cause:") > 0:
				m = re_cause.search(in_line)
				if m:
					#calls[call_ref].cause = m.groups()[1]
					calls[call_ref].cause = m.groups()[2]

	finally:
		in_file.close()

	print "================================"
	print "========Third Report (C)========"
	print "================================"

	for call_ref in calls.keys():
		print "C: call_ref: %s, num_msgs: %s, calling: %s, called: %s, cause: %s" % (call_ref, calls[call_ref].messages, calls[call_ref].calling_number, calls[call_ref].called_number, calls[call_ref].cause)
		rows += 1
	#sys.stderr.write("[%s] prilog.db: %d rows were inserted\n" % (time.asctime(time.localtime()),(rows)))
	return rows


def N_(message): return message

if __name__ == "__main__":
	loadPRILog()
	#loadPRILog2()
