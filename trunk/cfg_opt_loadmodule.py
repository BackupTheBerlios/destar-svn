# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig
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


class CfgOptModule(CfgOpt):
	
	shortName = _("Load module")
	variables = [VarType("name", title=_("Module to load"), len=20)]


	def row(self):
		return (self.shortName, self.name)


	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
		if res:
			return res
		if self.name.find(".") != -1:
			return ("name", _("Please don't specify an extension"))


	def createAsteriskConfiglet(self):
		needModule(self.name)
