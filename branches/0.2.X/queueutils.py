# -*- coding: iso-latin-1 -*-
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


import sys, os, string
import language
from datetime import datetime
from time import strptime
language.setLanguage('en')


try:
	from pysqlite2 import dbapi2 as sqlite
except ImportError:
	print _("Note: you should install python-pysqlite2 to have Queue Stats functionality")

try:
	db_fn = "/var/log/asterisk/queue.db"
	if not os.access(db_fn, os.O_RDWR):
		raise ImportError
	db = sqlite.connect(db_fn)
	db.isolation_level = None
except:
	print _("Note: you don't seem to have access to %s. See INSTALL.txt for details.") % db_fn
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
	cursor.execute("select max(timestamp) from queuelog")
	row = cursor.fetchone()
	maxtime = datetime.fromtimestamp(float(0))
	if row[0]:
		try:
			maxtime = datetime(*strptime(row[0], "%Y-%m-%d %H:%M:%S")[0:6])
		except:
			continue

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
			cursor.execute( "INSERT INTO queuelog (timestamp,callid,qname,agent,action,info1,info2,info3) VALUES  ('%s','%s','%s','%s','%s','%s','%s','%s')" % tuple(s) )
		except:
			print "Failed to execute insert at timestamp %s" % s[0]
			if __name__ == "__main__": sys.exit(0)
		rows += 1
	in_file.close()
	print "%d rows were inserted" % rows
	return rows


def N_(message): return message

def select(
		fields=['date(timestamp)',
			'callid',
			'qname',
			'agent',
			'action',
			'info1',
			'info2',
			'info3'
			],
		groupby=[],
		having=[],
		where=[],
		order=['timestamp'],
		limit=0,
		offset=0,
	):
	cursor = db.cursor()

	sql = ['SELECT']
	sql.append( ','.join(fields) )
	sql.append('FROM queuelog')

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

	cursor.execute( ' '.join(sql) )
	return cursor

def count(
		where=[],
		groupby=[],
		having=[],
	):
	cursor = db.cursor()

	sql = ['SELECT count(*)']
	sql.append('FROM queuelog')

	if where:
		sql.append('WHERE ')
		sql.append( ' AND '.join(where) )

	if groupby:
		sql.append('GROUP BY')
		sql.append( ','.join(groupby) )

	if having:
		sql.append('HAVING')
		sql.append( ','.join(having) )
	
	cursor.execute( ' '.join(sql) )
	resultRow = cursor.fetchone()
	result = int(resultRow[0])

	return result

if __name__ == "__main__":
	loadQueueLog()
