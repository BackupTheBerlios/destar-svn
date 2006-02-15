# -*- coding: iso-latin-1 -*-
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
			VarType("set",      title=_("Setting extension"), len=6, default="*78"),
			VarType("unset",   title=_("Unsetting extension"), len=6, default="*79")
		       ]

	def row(self):
		return ("%s / %s" % (self.set,self.unset), self.shortName)
	
	def checkConfig(self):
		import configlets
		for o in configlets.configlet_tree:
			if o==self: continue
			try:
				if o.ext == self.set or o.ext == self.unset:
					return ("ext", _("Extension already in use"))
			except AttributeError:
				pass

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection("apps")
		c.appendExten("%s" % self.set, "DBput(DND/${CALLERIDNUM})")
		c.appendExten("%s" % self.set, "Playback(do-not-disturb)")
		c.appendExten("%s" % self.set, "Hangup")
		c.appendExten("%s" % self.unset, "DBdel(DND/${CALLERIDNUM})")
		c.appendExten("%s" % self.unset, "Playback(do-not-disturb)")
		c.appendExten("%s" % self.unset, "Playback(cancelled)")
		c.appendExten("%s" % self.unset, "Hangup")
