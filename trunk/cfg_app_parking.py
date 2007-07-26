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
import panelutils

class CfgAppParking(CfgApp):

	shortName   = _("Park calls")
	newObjectTitle  = _("New call parking extension")
	description = _("Call Parking extension")
	
	def createVariables(self):
		self.variables   = [	VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
					VarType("ext",    title=_("Extension"), len=6),
					VarType("places", title=_("Parking places"), type="int", default=9, len=2)
					]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]

	def createAsteriskConfig(self):
		c = AstConf("features.conf")
		c.setSection("general")

		c.append("parkext=%s" % self.ext)
		c.append("context=%s" % self.pbx)
		# parkingtime
		first = int(self.ext)+1
		c.append("parkpos=%d-%d" % (first, first + self.places))
		# transferdigittimeout

		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten(self.ext, "Park(%s)" % self.ext, self.pbx)
		
		panelutils.createParkButton(self)
