# -*- coding: iso-latin-1 -*-
#
# This module is Copyright (C) 2005 by Alejandro Rios
# Destar is Copyright (C) 2005 by Holger Schurig
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


class CfgDialoutNormal(CfgDialout):

	shortName = _("Normal dialout entry")
	description = _("""Used to route calls through trunks""")
	groupName = 'Dialout'
	variables = [
		VarType("name",   title=_("Name"), len=15),
		VarType("pattern", title=_("Pattern"), len=15),
		VarType("maxtime", title=_("Maximum call time in seconds"), type="int", len=15, default=300),
		VarType("ringtime", title=_("Ringing time in seconds"), type="int", len=15, default=25),
		
		VarType("Trunks", title=_("Trunks to use for routing this dialout entry"), type="label", len=15, hide=True),
		VarType("defaulttrunk", title=_("Default trunk:"), type="choice", optional=True, options=getChoice("CfgTrunk"))
		     ]
	
	def fixup(self):
		Cfg.fixup(self)
		import configlets
		for obj in configlets.config_entries:
			if obj.groupName == 'Trunks':
				alreadyappended = False
				for v in self.variables:	
					if v.name == "Trunks":
						v.hide = False
					if v.name == obj.name:
						alreadyappended = True
				if not alreadyappended:
					self.variables.append(VarType("%s" % obj.name, title=_("%s") % obj.name, type="bool", optional=True,render_br=False))
					self.variables.append(VarType("%sprice" % obj.name, title=_("Price for this pattern"), len=10, optional=True))


	def isAddable(self):
		"We can only add this object if we have at least one trunk defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.groupName == 'Trunks':
				return True
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("macros.inc")
		c.setSection("macro-%s" % self.name)
		c.append("; params: exten,secret,timeout")
		c.appendExten("s","Authenticate(${ARG2})")
		c.appendExten("s","AbsoluteTimeout(${ARG3})")
		import configlets
		for obj in configlets.config_entries:
			if obj.groupName == 'Trunks':
				if self.__getitem__(obj.name) and self.__getitem__("%sprice" % obj.name):
					c.appendExten("s","ResetCDR")	
					c.appendExten("s","SetAccount(%s)" % self.__getitem__("%sprice" % obj.name))	
					c.appendExten("s","Dial(%s,%d|TtL(${ARG3}:10000))" % (obj.dial,self.ringtime))
		c.appendExten("s","Congestion(5)")
		c.appendExten("s","Goto(2)")
		c.appendExten("T","ResetCDR(w)")
		c.appendExten("T","NoCDR")
		c.appendExten("T","Hangup")
		c.appendExten("t","ResetCDR(w)")
		c.appendExten("t","NoCDR")
		c.appendExten("t","Hangup")

