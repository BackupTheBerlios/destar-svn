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
from language import _


class CfgPermDeny(CfgPerm):
	shortName = _("Deny outgoing calls")
	variables = [VarType("name",       title=_("Name"), len=15),
		     VarType("include",    title=_("Include other permission(s)"), optional=True),
		     VarType("deny", 	   title=_("Deny calls to this extension(s)"))]
		

#	def fixup(self):
#		CfgPerm.fixup(self)
#		useContext(self.name)
#		for i in self.include.split(","):
#			useContext(i.strip())


	def createAsteriskConfiglet(self):
		c = AstConf("extensions.conf")
		c.setSection(self.name)

		if self.include:
			for i in self.include.split(","):
				c.append("include=>%s" % i.strip())

		for d in self.deny.split(","):
			c.appendExten(d,"Macro(dial-result,99)")
