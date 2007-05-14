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
	description = _("Listen all calls on the CallWeaver server. Jump through calls pressing *.")
	
	def createVariables(self):
		self.variables   = [ 
			VarType("pbx",
				title=_("Virtual PBX"),
				type="choice",
				options=getChoice("CfgOptPBX")),
			
			VarType("ext",
				title=_("Extension"),
				len=6),

			VarType("scanspec",
				title=_("Channel pattern to scan?"),
				hint="<scanspec>",
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
		c.setSection(self.pbx)
		if self.password:
			c.appendExten(self.ext, "Authenticate(%s)" % self.password)
		if self.quiet:
			c.appendExten(self.ext, "Chanspy(%s|q)" % self.scanspec)
		else: 
			c.appendExten(self.ext, "Chanspy(%s)" % self.scanspec)
