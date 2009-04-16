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
import language,queueutils
from datetime import datetime
from time import strptime
language.setLanguage('en')


try:
	from pysqlite2 import dbapi2 as sqlite
except ImportError:
	print _("Note: you should install python-pysqlite2 to have Queue Stats functionality")

try:
	db1_fn = "/var/log/asterisk/master.db"
	if not os.access(db1_fn, os.O_RDWR):
		raise ImportError
	db1 = sqlite.connect(db1_fn)
	db1.isolation_level = None
except:
	print _("Note: you don't seem to have access to %s. See INSTALL.txt for details.") % db1_fn
	if __name__ == "__main__": sys.exit(0)
	db1 = None

try:
	db2_fn = "/var/log/asterisk/queue.db"
	if not os.access(db2_fn, os.O_RDWR):
		raise ImportError
	db2 = sqlite.connect(db2_fn)
	db2.isolation_level = None
except:
	print _("Note: you don't seem to have access to %s. See INSTALL.txt for details.") % db2_fn
	if __name__ == "__main__": sys.exit(0)
	db2 = None

try:
	db3_fn = "/var/log/asterisk/queue-master.db"
	if not os.access(db3_fn, os.O_RDWR):
		raise ImportError
	db3 = sqlite.connect(db3_fn)
	db3.isolation_level = None
except:
	print _("Note: you don't seem to have access to %s. See INSTALL.txt for details.") % db3_fn
	if __name__ == "__main__": sys.exit(0)
	db3 = None

def populateMaster ():
	cursor3 = db3.cursor()
	cursor3.execute("select max(AcctId) from queuecdr")
	row3 = cursor3.fetchone()
	maxAcctId = 0
	if row3[0]:
		try:
			maxAcctId = row3[0]
		except:
			pass
	rows = 0
	cursor1 = db1.cursor()
	cursor1.execute("select AcctId, uniqueid, clid, src, dst, start, answer, end, duration, disposition from cdr where AcctId>%d and intrunk>''" % maxAcctId)
	while 1:
		values=[]
		row1 = cursor1.fetchone()
		if not row1: break
		if not row1[1] > '0': continue
		values = list(row1)
		for i in range(13):
			values.append('0')
		#print values
		cursor2 = db2.cursor()
		sql1 = 'select timestamp, qname, agent, action, info1, info2, info3 from queuelog where callid like "%s"' % row1[1]
		#print sql1
		cursor2.execute(sql1)
		while 1:
			row2 = cursor2.fetchone()
			if not row2: break
			if row2[3] == '0': break
			if row2[3] == 'NONE': break
			values[21]= row2[1]
			values[22]= row2[2]
			values[9]= "No atendida"
			if row2[3] == "ABANDON":
				values[12]= row2[0]
				values[9]= "No atendida"
			elif row2[3] == "AGENTDUMP":
				values[14]= row2[0]
				values[9]= "No atendida"
			elif row2[3] == "COMPLETEAGENT":
				values[16]= row2[0]
				values[15]= row2[5]
				values[9]= "Atendida"
			elif row2[3] == "COMPLETECALLER":
				values[17]= row2[0]
				values[15]= row2[5]
				values[9]= "Atendida"
			elif row2[3] == "CONNECT":
				values[11]= row2[0]
				values[9]= "Atendida"
			elif row2[3] == "ENTERQUEUE":
				if values[10] == "0":
					values[10]= row2[0]
			elif row2[3] == "EXITWITHKEY":
				values[13]= row2[0]
				values[9]= "No atendida"
			elif row2[3] == "EXITWITHTIMEOUT":
				values[18]= row2[0]
				values[9]= "No atendida"
			elif row2[3] == "TRANSFER":
				values[19]= row2[0]
				values[20]= row2[4]
				values[9]= "Atendida"
		#print values
		#if values[21] == '0':
		#	values[9]= "Interrumpida"
		#if values[21] == 'NONE':
		#	values[9]= "Interrumpida"
		if values[21] == '0': continue
		if values[21] == 'NONE': continue
		try:
			sql = """INSERT INTO queuecdr (
			AcctId,
			uniqueid,
			clid,
			src,
			dst,
			start,
			answer,
			end,
			duration,
			disposition,
			enterqueue,
			connect,
			abandon,
			exitwithkey,
			agentdump,
			calltime,
			completeagent,
			completecaller,
			exitwithtimeout,
			transfer,
			transferext,
			qname,
			agent
			) VALUES  (%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % tuple(values) 
			#print sql
			cursor3.execute(sql)
		except:
			sys.stderr.write("[%s] queue-master.db: Failed to execute insert at AcctId: %s\n" % (time.asctime(time.localtime()), values[0]))
			if __name__ == "__main__": sys.exit(0)
		rows += 1
	sys.stderr.write("[%s] queue-master.db: %d rows were inserted\n" % (time.asctime(time.localtime()),(rows)))
	return rows


def N_(message): return message

def select(
		fields=[],
		groupby=[],
		having=[],
		where=[],
		order=['Acctid'],
		limit=0,
		offset=0,
	):
	cursor = db3.cursor()

	sql = ['SELECT']
	if fields==[]:
		sql.append('* FROM queuecdr')
	else:
		sql.append( ','.join(fields) )
		sql.append(' FROM queuecdr')

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
	cursor = db3.cursor()

	sql = ['SELECT count(*)']
	sql.append('FROM queuecdr')

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
	queueutils.loadQueueLog()
	populateMaster()
