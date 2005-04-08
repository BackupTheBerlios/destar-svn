# -*- coding: iso-latin-1 -*-
# Copyright (C) 2004 Michael Bielicki
# based on Free World Dialup Module by Hoger Schurig
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


class CfgLineDID(CfgLine):

	shortName   = _("direct inward dialing")

	description = _("""Used to route a DID to an extension or Auto-Attendant.""")

	variables	= [
		VarType("ext",       title=_("Extension"), len=15),
		VarType("name",	hide=True, default=""),
		VarType("phone",     title=_("Phone to ring"), optional=True, type="choice"),
		VarType("context",   title=_("Auto-Attendant"), optional=True, len=25)
		]

        def checkConfig(self):
                res = CfgLine.checkConfig(self)
                if res:
                        return res
		if self.phone and self.context:
                        return ("phone", _("Please don't specify both a phone and auto-attendant"))

	def createAsteriskConfig(self):
                c = AstConf("extensions.conf")
		c.setSection("dids")
                if self.phone:
			c.appendExten(self.ext,"Goto(phones,%s,1)" %  self.phone)
                elif self.context:
			c.appendExten(self.ext,"Goto(%s,s,1)" % self.context)
