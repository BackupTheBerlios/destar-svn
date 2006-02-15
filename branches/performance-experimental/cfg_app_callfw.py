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

class CfgAppCallFW(CfgApp):

	shortName   = _("Call forwarding")
	description = _("Extensions to set/unset call forwarding.")
	newObjectTitle = _("New extensions to set/unset call forwarding") 
				   
	def createVariables(self):
		self.variables   = [ VarType("type", title=_("Type"), type="choice", options=( ("CFIM", _("Call Forwarding Unconditional")), ("CFBS",_("Call Forwarding if Busy/Unavailable")) )),
			VarType("set",      title=_("Setting preffix"), len=6, default="*21*"),
			VarType("ext",   title=_("Unsetting extension"), len=6, default="#21#")
		       ]
	
	def row(self):
		return ("%s / %s" % (self.set,self.ext),self.shortName, self.type)

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection("apps")
		c.appendExten("_%sX." % self.set, "DBput(%s/${CALLERIDNUM}=${EXTEN:%d})" % (self.type, len(self.set)))
		if self.type == "CFIM":
			c.appendExten("_%sX." % self.set, "Playback(call-fwd-unconditional)")
		else:
			c.appendExten("_%sX." % self.set, "Playback(call-fwd-on-busy)")
		c.appendExten("_%sX." % self.set, "Hangup")
		c.appendExten("%s" % self.ext, "DBdel(%s/${CALLERIDNUM})" % self.type)
		c.appendExten("%s" % self.ext, "Playback(call-fwd-cancelled)")
		c.appendExten("%s" % self.ext, "Hangup")
