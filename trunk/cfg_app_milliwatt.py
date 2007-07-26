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


from configlets import *


class CfgAppMilliwatt(CfgApp):

	shortName   = _("Milliwatt test")
	newObjectTitle  = _("New milliwatt test extension")
	description = _("""Generate a Constant 1000Hz tone at 0dbm (mu-law). Used for
			measuring.""")
			
	def createVariables(self):
		self.variables   = [	VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
					VarType("ext", title=_("Extension"), len=6)]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
		

	def createAsteriskConfig(self):
		needModule("app_milliwatt")

		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten(self.ext, "Answer", self.pbx)
		c.appendExten(self.ext, "Milliwatt", self.pbx)
		c.appendExten(self.ext, "Hangup", self.pbx)
