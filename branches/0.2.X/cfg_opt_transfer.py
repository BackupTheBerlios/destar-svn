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


class CfgOptTransfer(CfgOptSingle):

	shortName = _("Transfer Extensions")
	newObjectTitle= _("Transfer Extensions")
	description = _("Extensions to dial to transfer a call.")
	
	def createVariables(self):
		self.variables = [
				VarType("blindxfer", title=_("Blind Transfer Extension"), len=6, optional=True),
				VarType("atxfer", title=_("Attended Transfer Extension"), len=6, optional=True),
				VarType("transferdigittimeout", title=_("Number of seconds to wait between digits when transfering a call"), hint=_("Default is 3 seconds"), type="int", len=6, optional=True, default=3),
				VarType("atxfernoanswertimeout", title=_("Timeout for answer on attended transfer"), hint=_("Default is 15 seconds"), type="int", len=6, optional=True, default=15),
		    ]

	def row(self):
		return (self.shortName, "")
		
	def createAsteriskConfig(self):
		c = AstConf("features.conf")
        	c.setSection("general")
		if self.transferdigittimeout:
			c.appendValue(self, "transferdigittimeout")
		if self.atxfernoanswertimeout:
			c.appendValue(self, "atxfernoanswertimeout")
		c.setSection("featuremap")
		if self.blindxfer:
			c.appendValue(self, "blindxfer")
		if self.atxfer:
			c.appendValue(self, "atxfer")
