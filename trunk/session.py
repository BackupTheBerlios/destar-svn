# -*- coding: utf-8 -*-
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
		request.response.set_charset('utf-8')
		# Determine IP of originator, keep Squid in mind :-)
		try:
			self.ip = request.environ['HTTP_X_FORWARDED_FOR']
		except:
			self.ip = request.environ['REMOTE_ADDR']
		self.port = request.environ['REMOTE_PORT']


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
		if self.level == -1:
			# Only try auto-login once, so set it to lowest level
			self.level = 0

			users = backend.getConfiglets(name="CfgOptUser")
			if len(users) == 0:
				# be Admin if there are no users configured
				self.user  = "programmer"
				self.level = 4
				self.language = 'en'
				print ("[%s] Logging in with user 'programmer' from ip %s, port %s" % (time.asctime(time.localtime()), self.ip, self.port))
			else:
				for user in users:
					if user.pc == self.ip:
						self.user = user.name
						self.level = int(user.level)
						self.phone = user.phone
						self.language = user.language
						break
						
		language.setLanguage(self.language)				
#		request.session = session


	def has_info(self):
		return Session.has_info(self)

	is_dirty = has_info
	
