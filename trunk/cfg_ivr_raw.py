# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# this file has Copyright (C) 2005 by Alejandro Rios P.
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


class CfgIVRRaw(CfgIVR):

	shortName = _("Raw IVR")
	newObjectTitle= _("New raw IVR")
	
	def createVariables(self):
		self.variables = [
			VarType("name", title=_("Name"), len=15),
			VarType("txt",  title=_("Contents"), type="text", size=8, cols=40),
		]

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection(self.name)
		contents=self.txt.split("\n")
		for line in contents:
			c.append(line)

