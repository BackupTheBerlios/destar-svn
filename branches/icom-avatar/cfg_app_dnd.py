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

class CfgAppDND(CfgApp):

	shortName   = _("Set/Unset DND")
	newObjectTitle  = _("New extensions to Set/Unset Do not disturb")
	description = _("Extensions to set/unset 'Do Not Disturb'.")
	
	def createVariables(self):
		self.variables   = [
			VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")), 
			VarType("set",      title=_("Setting extension"), len=6, default="*78"),
			VarType("unset",   title=_("Unsetting extension"), len=6, default="*79")
		       ]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]

	def row(self):
		return ("%s / %s" % (self.set,self.unset), self.shortName, self.pbx)
	
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
		import configlets
		tapisupport = False
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ == 'CfgOptSettings':
				if obj.tapi:
				    tapisupport = True
		c = AstConf("extensions.conf")
		c.setSection("%s-apps" % self.pbx)
		c.appendExten("%s" % self.set, "Set(DB(DND/%s/${CALLERID(num)})=True)" % self.pbx, self.pbx)
		if tapisupport:
			needModule("app_cut")
			c.appendExten("%s" % self.set, "Set(CHAN=${CUT(CHANNEL,-,1)})", self.pbx)
			c.appendExten("%s" % self.set, "UserEvent(ASTDB,Channel: ${CHAN}^Family: DND^Value: True)", self.pbx )
				
		c.appendExten("%s" % self.set, "Playback(do-not-disturb)", self.pbx)
		c.appendExten("%s" % self.set, "Playback(activated)", self.pbx)
		c.appendExten("%s" % self.set, "Hangup", self.pbx)

		c.appendExten("%s" % self.unset, "DBdel(DND/%s/${CALLERID(num)})" % self.pbx, self.pbx)
		if tapisupport:
			c.appendExten("%s" % self.unset, "Set(CHAN=${CUT(CHANNEL,-,1)})", self.pbx)
			c.appendExten("%s" % self.unset, "UserEvent(ASTDB,Channel: ${CHAN}^Family: DND^Value: ^)", self.pbx )
		c.appendExten("%s" % self.unset, "Playback(do-not-disturb)", self.pbx)
		c.appendExten("%s" % self.unset, "Playback(cancelled)", self.pbx)
		c.appendExten("%s" % self.unset, "Hangup", self.pbx)
