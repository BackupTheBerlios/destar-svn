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


import sys, os, string, time
import language
from datetime import datetime
from time import strptime
language.setLanguage('en')
from config import *

try:
	import MySQLdb as mysql
except ImportError:
	print _("Note: you should install python mysql libs to have CDR Stats in MySQL")

try:
	if not  os.access("/usr/lib/asterisk/modules/cdr_addon_mysql.so", os.F_OK):
		raise ImportError
	needModule("cdr_addon_mysql")
except:
	print _("Note: you need the cdr_addon_mysql module to have CDR and Stats functionalities")
	
try:
	db = mysql.connect(host = DBHOST, db = DBNAME, user = DBUSER, passwd = DBPASSWD)
#	db3.isolation_level = None
except:
	print _("Note: you don't seem to have access to mysql.")
	if __name__ == "__main__": sys.exit(0)
	db = None



def loadQueueLog ():
	try:
		q_fn = "/var/log/asterisk/queue_log"
		if not os.access(q_fn, os.O_RDWR):
			raise ImportError
	except:
		print _("Note: you don't seem to have access to %s.") % q_fn
		if __name__ == "__main__": sys.exit(0)

	cursor = db.cursor()
	cursor.execute("select max(time) from queuelog")
	row = cursor.fetchone()
	maxtime = datetime.fromtimestamp(float(0))
	if row[0]:
		try:
			maxtime = datetime(*strptime(row[0], "%Y-%m-%d %H:%M:%S")[0:6])
		except:
			pass

	rows = 0
	in_file = open(q_fn,"r")
	for in_line in in_file.readlines():
		in_line = string.strip(in_line[:-1])
		if (in_line[-1] == "|"):
			in_line = in_line[0:-1]
		s = string.split(in_line,"|")
		s[0] = datetime.fromtimestamp(float(s[0]))
		if (maxtime >= s[0]):
			continue
		s[0] = s[0].isoformat(' ')
		length = len(s)
		if (length < 6):
			s.append('')
		if (length < 7):
			s.append('')
		if (length < 8):
			s.append('')
		try:
			cursor.execute( "INSERT INTO queue_log (time,callid,queuename,agent,event,info1,info2,info3) VALUES  ('%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(s) )
		except:
			sys.stderr.write("[%s] queue.db: Failed to execute insert at timestamp %s\n" % (time.asctime(time.localtime()), s[0]))
			if __name__ == "__main__": sys.exit(0)
		rows += 1
	in_file.close()
	sys.stderr.write("[%s] queue.db: %d rows were inserted\n" % (time.asctime(time.localtime()),(rows)))
	return rows


def N_(message): return message

def select(
		fields=['FROM_UNIXTIME(time) as time',
			'callid',
			'queuename',
			'agent',
			'event',
			'info1',
			'info2',
			'info3',
			'info4'
			],
		groupby=[],
		having=[],
		where=[],
		order=['time'],
		limit=0,
		offset=0,
	):
	db = mysql.connect(host = DBHOST, db = DBNAME, user = DBUSER, passwd = DBPASSWD)
	cursor = db.cursor()

	sql = ['SELECT']
	sql.append( ','.join(fields) )
	sql.append('FROM queue_log')

	if where:
		sql.append('WHERE ')
		sql.append( ' AND '.join(where) )

	if groupby:
		sql.append('GROUP BY')
		sql.append( ','.join(groupby) )

	if having:
		sql.append('HAVING')
		sql.append( ','.join(having) )

	if order:
		sql.append('ORDER BY')
		sql.append( ','.join(order) )

	if limit:
		sql.append('LIMIT %d' % limit)
		if offset:
			sql.append('OFFSET %d' % offset)

	print ' '.join(sql) 
	cursor.execute( ' '.join(sql) )
	return cursor

def count(
		where=[],
		groupby=[],
		having=[],
	):
	db = mysql.connect(host = DBHOST, db = DBNAME, user = DBUSER, passwd = DBPASSWD)
	cursor = db.cursor()

	sql = ['SELECT count(*)']
	sql.append('FROM queue_log')

	if where:
		sql.append('WHERE ')
		sql.append( ' AND '.join(where) )

	if groupby:
		sql.append('GROUP BY')
		sql.append( ','.join(groupby) )

	if having:
		sql.append('HAVING')
		sql.append( ','.join(having) )
	
	print ' '.join(sql) 
	cursor.execute( ' '.join(sql) )
	resultRow = cursor.fetchone()
	result = int(resultRow[0])

	return result

#if __name__ == "__main__":
	#loadQueueLog()
