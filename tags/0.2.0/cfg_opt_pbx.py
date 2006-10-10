# -*- coding: iso-latin-1 -*-
#
# This modules is Copyright (C) 2005 by Alejandro Rios,
# Destar is Copyright (C) 2005 by Holger Schurig,
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
import os

class CfgOptPBX(CfgOpt):

	shortName = _("Virtual PBX")
	newObjectTitle = _("New Virtual PBX")
	description = _("""You can have several logically separated PBX""")
	groupName = 'PBX'
		
	variables = [
		VarType("name",	  title=_("Name"), len=15),
			]

	def checkConfig(self):
                res = CfgOpt.checkConfig(self)
                if res:
                        return res
		
	def createAsteriskConfig(self):
		s = AstConf("extensions.conf")
		s.setSection(self.name)
		s.append(";Virtual PBX")
	
	def row(self):
		return (self.shortName,self.name)
