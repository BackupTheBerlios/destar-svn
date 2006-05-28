# -*- coding: iso-latin-1 -*-
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


import sys, os


try:
	from pysqlite2 import dbapi2 as sqlite
except ImportError:
	print "Note: you should install python-pysqlite2 to have CDR functionality"

try:
	db_fn = "/var/log/asterisk/master.db"
	if not os.access(db_fn, os.O_RDWR):
		raise ImportError
	db = sqlite.connect(db_fn, isolation_level="IMMEDIATE")
except:
	print "Note: you don't seem to have access to /var/log/asterisk/master.db yet"
	if __name__ == "__main__": sys.exit(0)
	db = None

def N_(message): return message

def select(
		fields=['start as %s' % N_("Time_of_start"),
			'src as %s' % N_("Source"),
			'clid as %s' % N_("Caller_ID"),
			'dst as %s' % N_("Destination"),
			'answer as %s' % N_("Time_of_answer"),
			'billsec as %s' % N_("Duration"),
			'disposition as %s' % N_("Result"),
			'pbx as %s' % N_("PBX"),
			'accountcode as %s' % N_("Account_code")],
		groupby=[],
		having=[],
		where=[],
		order=['Acctid'],
		limit=0,
		offset=0,
	):
	cursor = db.cursor()

	sql = ['SELECT']
	sql.append( ','.join(fields) )
	sql.append('FROM cdr')

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
	sql.append('FROM cdr')

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
	cu = select()
	while 1:
		row = cu.fetchone()
		if not row: break
		for s in row: print s,
		print
