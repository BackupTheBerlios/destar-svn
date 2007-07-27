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


"""
DeStarPublisher also has it's own session management. For simplicity, I put
the session stuff directly into the Publisher object, so I don't use
Quixote's classes 'Session' and 'SessionPublisher'.

Reasons:

a) they set a cookie, some browsers don't allow cookies

b) if you stop and start DeStar (which happens very often during
   Development) Quixote's session handler would give you ugly error messages

c) Keeping the session data in the publisher object scales quite ok, because
   DeStar will usually only be used inside the LAN anyway

But keep in mind that a session here is not a (user, host, browser_process)
tuple, but a (user, host) tuple.

TODO: the default implementation provided here is not persistent. There is
also no cleanup code to remove old sessions.


The Session holds several values:

request.session.user         User name
request.session.level        User level (0=disabled/not logged in
                                         1=normal PBX user
                                         2=PBX Administrator
                                         3=PBX Configurator
                                         4=Programmer
request.session.language     User language
"""


from quixote import enable_ptl, get_request
from quixote.publish import Publisher
from quixote.session import SessionManager
import configlets, backend, language
from session import DestarSession
import time
enable_ptl()

class DeStarPublisher(Publisher):


	def filter_output(self, request, output):
		output = Publisher.filter_output(self, request, output)
		#resp = request.response
		#if resp.get_header('Content-Type') in (None, 'text/html'):
		#	resp.set_header('Content-Type','text/html; charset=%s' % language.encoding() )
		return output


def create_publisher():
	from page_main import Page
	return DeStarPublisher(Page(),
		session_manager=SessionManager(session_class=DestarSession),
		display_exceptions='plain')

