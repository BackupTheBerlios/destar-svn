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


class CfgOptRawCfg(CfgOpt):

	shortName = _("Raw config file snipped")
	variables = [
		VarType("name", title=_("Name"), len=15),
		VarType("file", title=_("File name"), len=15),
		VarType("sect", title=_("Section/Context"), len=15),
		VarType("txt",  title=_("Contents"), type="text", size=8, cols=40),
	]

	def createAsteriskConfiglet(self):
		file = self.file
		if file.find('.')==-1:
			file += '.conf'
		c = AstConf(file)
		c.setSection(self.sect)
		c.append(self.txt)

	def row(self):
		return (self.shortName, "%s %s:%s" % (self.name, self.file, self.sect))
