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

class CfgAppGlobalQuickDial(CfgApp):

	shortName   = _("Global Quick Dial List")
	description = _("Extensions to add/remove from global quick dial list. The add extension will be of the form prefix+2_digits_key+*+final_destination. The remove extension will be of the form prefix+2_digits_key. The global list only works if the calling estension has been assigned a dialout with the quick dial lookup option activated.")
	newObjectTitle = _("New extensions to add/remove from global quick dial list") 
	
	def createVariables(self):
		self.variables   = [
				VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
				VarType("pin", title=_("Password"), len=20, optional=True),
				VarType("set",      title=_("Setting prefix"), len=6, default="*9"),
				VarType("unset",   title=_("Unsetting prefix"), len=6, default="#9#")
		       ]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
	
	def row(self):
		return ("%s / %s" % (self.set,self.unset),self.shortName,self.pbx)

	def checkConfig(self):
		import configlets
		for o in configlets.configlet_tree:
			if o==self: continue
			try:
				if o.ext == self.set:
					return ("set", _("Extension already in use"))
				if o.ext == self.unset:
					return ("unset", _("Extension already in use"))
			except AttributeError:
				pass

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		if self.pin:
			needModule("app_authenticate")
			c.appendExten("_%sXX*X." % self.set, "Authenticate(%s)" % self.pin, self.pbx)
		c.appendExten("_%sXX*X." % self.set, "Set(DB(QUICKDIALLIST/GLOBAL/${EXTEN:%d:2})=${EXTEN:%d})" % (len(self.set),len(self.set)+3), self.pbx)
		c.appendExten("_%sXX*X." % self.set, "Hangup", self.pbx)
		c.appendExten("_%sXX" % self.unset, "DBdel(QUICKDIALLIST/GLOBAL/${EXTEN:%d})" % len(self.unset), self.pbx)
		c.appendExten("_%sXX" % self.unset, "Hangup", self.pbx)
