# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig
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


import sys, os
#from language import _

try:
	import sqlite
	db_fn = "/var/log/asterisk/cdr.db"
	if not os.access(db_fn, os.O_RDWR):
		raise ImportError
	db = sqlite.connect(db_fn, autocommit=False, command_logfile=sys.stdout)
except ImportError:
	print "Note: you should install sqlite, pysqlite and res_sqlite to have CDR functionality"
	if __name__ == "__main__": sys.exit(0)
	db = None


def checkLookupTableAmaflags():
	try:
		curs = db.cursor()
		curs.execute("select count(1) from l_amaflags")
		return
	except sqlite._sqlite.DatabaseError:
		pass

	curs.execute("CREATE TABLE l_amaflags (amaflags INTEGER, flags CHAR(8), PRIMARY KEY(amaflags))")
	curs.execute("INSERT INTO l_amaflags VALUES (1,'omit')")
	curs.execute("INSERT INTO l_amaflags VALUES (2,'bill')")
	curs.execute("INSERT INTO l_amaflags VALUES (3,'doc')")
	#CREATE UNIQUE INDEX i_amaflags_amaflags on l_amaflags(amaflags);
	db.commit()


def checkLookupTableDisposition():
	try:
		curs = db.cursor()
		curs.execute("select count(1) from l_disposition")
		return
	except sqlite._sqlite.DatabaseError:
		pass

	curs.execute("CREATE TABLE l_disposition (disposition INTEGER, state CHAR(8), PRIMARY KEY(disposition))")
	curs.execute("INSERT INTO l_disposition VALUES (0,'none')")
	curs.execute("INSERT INTO l_disposition VALUES (1,'noanswer')")
	curs.execute("INSERT INTO l_disposition VALUES (2,'busy')")
	curs.execute("INSERT INTO l_disposition VALUES (3,'noanswer,busy')")
	curs.execute("INSERT INTO l_disposition VALUES (4,'answered')")
	curs.execute("INSERT INTO l_disposition VALUES (5,'answered,noanswer')")
	curs.execute("INSERT INTO l_disposition VALUES (6,'answered,busy')")
	curs.execute("INSERT INTO l_disposition VALUES (7,'answered,noanswer,busy')")
	curs.execute("INSERT INTO l_disposition VALUES (8,'failed')")
	curs.execute("INSERT INTO l_disposition VALUES (9,'failed,noanswer')")
	curs.execute("INSERT INTO l_disposition VALUES (10,'failed,busy')")
	curs.execute("INSERT INTO l_disposition VALUES (11,'failed,noanswer,busy')")
	curs.execute("INSERT INTO l_disposition VALUES (12,'failed,answered')")
	curs.execute("INSERT INTO l_disposition VALUES (13,'failed,answered,noanswer')")
	curs.execute("INSERT INTO l_disposition VALUES (14,'failed,answered,busy')")
	curs.execute("INSERT INTO l_disposition VALUES (15,'failed,answered,noanswer,busy')")
	#CREATE UNIQUE INDEX INDEX i_disposition_disposition ON l_disposition(disposition);
	db.commit()


def select(
		fields=['src','dst','answer','billsec','flags','state'],
		groupby=[],
		having=[],
		order=['Acctid'],
		limit=0,
		offset=0,
	):
	cursor = db.cursor()

	sql = ['SELECT']
	sql.append( ','.join(fields) )
	sql.append('FROM cdr')

	flag = False
	if 'flags' in fields:
		sql.append('LEFT JOIN l_amaflags')
		flag = True
	if 'state' in fields:
		sql.append('LEFT JOIN l_disposition')
		flag = True
	if flag:
		sql.append('WHERE')

	flag = False
	if 'flags' in fields:
		sql.append('cdr.amaflags = l_amaflags.amaflags')
		flag = True
	if 'state' in fields:
		if flag: sql.append('AND')
		sql.append('cdr.disposition = l_disposition.disposition')

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


if __name__ == "__main__":
	cu = checkLookupTableAmaflags()
	cu = checkLookupTableDisposition()

	cu = select()
	while 1:
		row = cu.fetchone()
		if not row: break
		for s in row: print s,
		print
