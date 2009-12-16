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

class CfgAppPhoneQuickDial(CfgApp):

	shortName   = _("Private Quick Dial List")
	description = _("Extensions to add/remove from personal quick dial list. The add extension will be of the form prefix+2_digits_key+*+final_destination. The remove extension will be of the form prefix+2_digits_key. The personal quick dial list works for all extensions, by dialing dial_prefix+2_digits_key and only if the extension has an assigned dialout entry which pattern matches the final destination.")
	newObjectTitle = _("New extensions to add/remove/access personal quick dial list")
	
	def createVariables(self):
		self.variables   = [
			VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
			VarType("set",      title=_("Setting prefix"), len=6, default="*7"),
			VarType("unset",   title=_("Unsetting prefix"), len=6, default="#7#"),
			VarType("dialprefix",   title=_("Dial prefix"), len=6, default="**"),
		       ]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
	
	def row(self):
		return ("%s / %s" % (self.set,self.unset),self.shortName,self.pbx)

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection("%s-apps" % self.pbx)
		c.appendExten("_%sXX*X." % self.set, "Set(DB(QUICKDIALLIST/${CALLERID(num)}/${EXTEN:%d:2})=${EXTEN:%d})" % (len(self.set),len(self.set)+3), self.pbx)
		c.appendExten("_%sXX*X." % self.set, "Hangup", self.pbx)
		c.appendExten("_%sXX" % self.unset, "DBdel(QUICKDIALLIST/${CALLERID(num)}/${EXTEN:%d})" % len(self.unset), self.pbx)
		c.appendExten("_%sXX" % self.unset, "Hangup", self.pbx)
