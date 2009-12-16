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

class CfgAppCIDBlocking(CfgApp):

	shortName   = _("Caller Identifier Blocking List")
	description = _("Extensions to add/remove from personal CID blocking list. The add extension will be of the form prefix+*+number_to_block. The remove extension will be of the form prefix+*+number_to_block.")
	newObjectTitle = _("New extensions to add/remove/access personal CID blocking list")
	
	def createVariables(self):
		self.variables   = [
			VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
			VarType("set",      title=_("Setting prefix"), len=6, default="*9"),
			VarType("unset",   title=_("Unsetting prefix"), len=6, default="#9"),
		       ]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
	
	def row(self):
		return ("%s / %s" % (self.set,self.unset),self.shortName,self.pbx)

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten("_%s*X." % self.set, "Set(DB(CIDBLOCKLIST/${CALLERID(num)}/${EXTEN:%d})=${EXTEN:%d})" % (len(self.set)+1,len(self.set)+1))
		c.appendExten("_%s*X." % self.set, "Hangup")
		c.appendExten("_%s*X" % self.unset, "DBdel(CIDBLOCKLIST/${CALLERID(num)}/${EXTEN:%d})" % len(self.unset)+1)
		c.appendExten("_%s*X" % self.unset, "Hangup")
