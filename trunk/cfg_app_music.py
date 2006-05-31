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


class CfgAppMusic(CfgApp):

	shortName   = _("Listen to music-on-hold")
	newObjectTitle  = _("New music-on-hold extension")
	description = _("Play Play Music On Hold until you hang up.")
	
	def createVariables(self):
		self.variables   = [ VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
			VarType("ext", title=_("Extension"), len=6),
			VarType("moh",	  title=_("Music-on-hold class"), type="choice", optional=True,
			options=getChoice("CfgOptMusic"))]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten(self.ext, "Answer")
		c.appendExten(self.ext, "Wait(1)")
		if self.moh:
			c.appendExten(self.ext, "MusicOnHold(%s)" % self.moh)
		else: 
			c.appendExten(self.ext, "MusicOnHold")
