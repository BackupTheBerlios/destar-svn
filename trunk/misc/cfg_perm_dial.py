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


from configlets import *
from language import _


class CfgPermDial(CfgPerm):
	shortName = _("Dial permission")
	variables = [VarType("name",       title=_("Name")),
		     VarType("desc",       title=_("Description"), optional=True),
		     VarType("ignorepat",  title=_("Keep dialtone for numbers starting with"), optional=True),
		     VarType("include",    title=_("Include other permission(s)"), optional=True),
		    ]


	def fixup(self):
		CfgPerm.fixup(self)
		useContext(self.name)
		for i in self.include.split(","):
			useContext(i.strip())


	def createAsteriskConfiglet(self):
		c = AstConf("extensions.conf")
		c.setSection(self.name)

		if self.ignorepat:
			for i in self.ignorepat.split(","):
				c.append("ignorepat=%s" % i.strip())

		if self.include:
			for i in self.include.split(","):
				c.append("include=>%s" % i.strip())

		c.appendExten("s","Answer")
		c.appendExten("s","DigitTimeout,3")
		c.appendExten("s","ReponseTimeout,30")
		c.appendExten("i","Macro(dial-result,5)")
		c.appendExten("t","Macro(dial-result)")
		c.appendExten("T","PlayTones(congestion)")
		c.appendExten("T","Wait(5)")
		c.appendExten("T","Hangup")
