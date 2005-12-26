# -*- coding: iso-latin-1 -*-
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


class CfgOptPickup(CfgOptSingle):

	shortName = _("Pickup Extension")
	newObjectTitle= _("Pickup Extension")
	description = _("Extension to dial to pick-up a call in the same group.")
	variables = [VarType("ext", title=_("Extension"), len=6)
		    ]

	def row(self):
		return (self.shortName, self.ext)
		
	def createAsteriskConfig(self):
		c = AstConf("features.conf")
        	c.setSection("general")
		c.append("pickupexten=%s" % self.ext)
