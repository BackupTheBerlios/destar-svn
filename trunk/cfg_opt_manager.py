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


from configlets import *


class CfgOptManager(CfgOpt):

	_opt = ("system", "call", "log", "verbose", "command", "agent", "user")
	shortName = _("Management API access")
	variables = [VarType("name",   title=_("Name"), len=15),
		     VarType("secret", title=_("Secret"), len=15, default=generatePassword(8)),
		     VarType("deny",   title=_("IP disable mask"), len=31, default="0.0.0.0/0.0.0.0"),
		     VarType("permit", title=_("IP enable mask"), len=31,   default="127.0.0.1/255.255.255.0"),
		     VarType("read",   title=_("Read"),  type="mchoice", optional=True, options=_opt),
		     VarType("write",  title=_("Write"), type="mchoice", optional=True, options=_opt, default=','.join(_opt)),
		    ]

	def fixup(self):
		CfgOpt.fixup(self)
		if not self.secret:
			# TODO: invent a real password by getting bytes
			# from /dev/urandom and massaging them with
			# binhex or something like this
			self.secret = "secret"


	def createAsteriskConfiglet(self):
		c = AstConf("manager.conf")
		
		c.setSection("general")
		c.append("enabled=yes")
		#c.append("portno=5038")
		#c.append("bindaddr=127.0.0.1")

		c.setSection(self.name)
		for s in self.variables:
			if s.name=="name": continue
			c.append("%s=%s" % (s.name,self.__dict__[s.name] or ''))

	def row(self):
		return (self.shortName, self.name)
