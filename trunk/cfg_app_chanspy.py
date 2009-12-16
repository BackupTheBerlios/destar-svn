# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 by Diego Andrés Asenjo G.
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


class CfgAppChanspy(CfgApp):

	shortName   = _("Listen calls")
	newObjectTitle  = _("New spy extension")
	description = _("Listen all calls on the Asterisk server. Jump through calls pressing *.")
	
	def createVariables(self):
		self.variables   = [ 
			VarType("pbx",
				title=_("Virtual PBX allowed to dial"),
				type="choice",
				optional = True,
				options=getChoice("CfgOptPBX")),
			
			VarType("phone",
				title = _("Phone allowed to dial"),
				optional = True,
				type ="choice",
				options = getChoice("CfgPhone")),

			VarType("ext",
				title=_("Extension"),
				len=6),

			VarType("scanspec",
				title=_("Channel pattern to scan?"),
				hint="<scanspec>",
				optional=True,
				len=15),

			VarType("spygroup",
				title=_("Spy Group"),
				optional=True,
				len=15),

			VarType("password",
				type="int",
				title=_("Password"),
				len=6),

			VarType("quiet",
				title=_("Be quiet?"),
				type="bool",
				default=True)]

		self.dependencies = [ 
			DepType("pbx",
			type="hard",
			message = _("This is a Dependency")),]

	def createAsteriskConfig(self):
		needModule("app_chanspy")
		c = AstConf("extensions.conf")
		if self.pbx:
			c.setSection("%s-apps" % self.pbx)
		else:
			c.setSection("real-out-%s" % self.phone)
		if self.password:
			c.appendExten(self.ext, "Authenticate(%s)" % self.password, self.pbx)
		if self.quiet:
			quiet = "q"
		else:
			quiet = ""
		if self.spygroup:
			c.appendExten(self.ext, "Chanspy(,g(%s)%s)" % (self.spygroup,quiet), self.pbx)
		else:
			c.appendExten(self.ext, "Chanspy(%s,q%s" % (self.scanspec,quiet), self.pbx)
