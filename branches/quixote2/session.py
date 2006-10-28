# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2006 by Holger Schurig
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


from quixote.session import Session, SessionManager
from quixote import get_request
import configlets, backend, language
import time

class DestarSession(Session):
	def __init__(self, id):
		Session.__init__(self, id)
		self.level = -1
		self.language = 'en'

	def start_request (self):
		Session.start_request(self)

		request = get_request()
		t = time.time()

		# Determine IP of originator, keep Squid in mind :-)
		try:
			ip = request.environ['HTTP_X_FORWARDED_FOR']
		except:
			ip = request.environ['REMOTE_ADDR']


		#session = sessions.setdefault(ip,
		#	configlets.Holder(
		#		firstaccess=t,
		#		user=None,
		#		phone='',
		#		language='en',
		#		level=-1,		# Try to auto-login, based on IP
		#	))

		# level==-1 means we should auto-login
		# This works by searching for the first CfgOptUser configlet where
		# the 'pc' variable matches the request originating IP:
#		if session.level == -1:
			# Only try auto-login once, so set it to lowest level
#			session.level = 0

#			users = backend.getConfiglets(name="CfgOptUser")
#			if len(users) == 0:
				# be Admin if there are no users configured
#				session.user  = "programmer"
#				session.level = 4
#				session.language = 'en'
#			else:
#				for user in users:
#					if user.pc == ip:
#						session.user = user.name
#						session.level = int(user.level)
#						session.phone = user.phone
#						session.language = user.language
#						break
						
#		language.setLanguage(session.language)				
#		request.session = session


	def has_info(self):
		return Session.has_info(self)

	is_dirty = has_info
	
