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


def select(
		fields=['src','dst','answer','billsec','amaflags','disposition'],
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
	cu = select()
	while 1:
		row = cu.fetchone()
		if not row: break
		for s in row: print s,
		print
