# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2005 by Alejandro Rios
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

class CfgAppPickup(CfgApp):

	shortName   = _("Channel Pickup")
	newObjectTitle  = _("New extensions to pickup a ringing Channel")
	description = _("Extensions to pickup a ringing Channel.")
	
	def createVariables(self):
		self.variables   = [
			VarType("pbx",
				title=_("Virtual PBX"),
				type="choice",
				options=getChoice("CfgOptPBX")),
			VarType("prefix",
				title=_("Channel Pickup Prefix"),
				len=6,
				default="*8")
		       ]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]

	def row(self):
		return ("%s" % (self.prefix), self.shortName, self.pbx)
	
	def createAsteriskConfig(self):
		needModule("app_directed_pickup")
		c = AstConf("extensions.conf")
		c.setSection("%s-apps" % self.pbx)
		c.appendExten("_%s." % self.prefix, "Pickup(${EXTEN:%d}@PICKUPMARK)" % (len(self.prefix)), self.pbx)
		c.appendExten("_%s." % self.prefix, "Hangup", self.pbx)
