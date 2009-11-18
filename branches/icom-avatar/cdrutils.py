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


import sys, os
import language
from configlets import needModule
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

def N_(message): return message

def select(
		fields=['calldate as %s' % N_("Time_of_start"),
			'src as %s' % N_("Source"),
			'clid as %s' % N_("Caller_ID"),
			'dst as %s' % N_("Destination"),
			'billsec as %s' % N_("Duration"),
			'billsec as %s' % N_("Seconds"),
			'disposition as %s' % N_("Result"),
			'pbx as %s' % N_("PBX"),
			'uniqueid as %s' % N_("UniqueId"),
			'record as %s' % N_("Record")],
		groupby=[],
		having=[],
		where=[],
		order=[],
#		order=['Acctid'],
		limit=0,
		offset=0,
	):
	db = mysql.connect(host = DBHOST, db = DBNAME, user = DBUSER, passwd = DBPASSWD)
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
	
	#print ' '.join(sql)
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
