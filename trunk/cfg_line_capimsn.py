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
from language import _

class CfgLineCapiMSN(CfgLine):

	shortName = _("ISDN using CAPI, incoming")
	variables = [
		VarType("name",      title=_("Name"), len=15),

		VarType("Inbound",   title=_("Calls from the ISDN network"), type="label"),
		VarType("msn",       title=_("Subscriber number"), len=15),
		VarType("phone",     title=_("Phone to ring"), type="choice"),
		]

	technology = "CAPI"


	def isAddable(self):
		"We can only add this object if we have at least one outgoing CAPI channel defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.__class__.__name__ == 'CfgLineCapi':
				return True
		return False
	isAddable = classmethod(isAddable)


	def row(self):
		return (self.msn, self.name, self.shortName)


	def fixup(self):
		CfgLine.fixup(self)
		useContext("in-capi")


	def checkConfig(self):
		res = CfgLine.checkConfig(self)
		if res:
			return res
		else:
			import configlets
			for obj in configlets.config_entries:
				if obj.__class__.__name__ == 'CfgLineCapiMSN':
					if obj.msn == self.msn:
						return ("msn",_("MSN already assigned"))


	def createAsteriskConfiglet(self):
		needModule("chan_capi")

		c = AstConf("extensions.conf")
		c.setSection("in-capi")
		c.appendExten(self.msn, "Goto(phones,%s,1)" % self.phone)
