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
		self.variables = [ 
			VarType("pbx",	  title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
			VarType("type", title=_("Type"), type="choice", options=( ("CFIM", _("Call Forwarding Unconditional")), \
			("CFBS", _("Call Forwarding if Busy")), ("CFTO", _("Call Forwarding if Timeout/Unavailable")) )),
			VarType("set",      title=_("Setting preffix"), len=6, default="*21"),
			VarType("ext",   title=_("Unsetting extension"), len=6, default="*22"),
			VarType("toggle",   title=_("Set function toggleable"), type="bool"),
			VarType("devstateprefix",   title=_("Create Devstate extension. Devstate Prefix:"), len=8, default="")
		       	]

		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
	
	def row(self):
		return ("%s / %s" % (self.set,self.ext),"%s %s" % (self.shortName, self.type), self.pbx)

	def createAsteriskConfig(self):
		if self.devstateprefix:
		    needModule("app_devstate")
		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten("_%s" % self.set, "Set(testcf=${DB(%s/%s/${CALLERIDNUM})})" % (self.type, self.pbx))
		c.appendExten("_%s" % self.set, 'GotoIf($["${testcf}" != ""]?switchoff)')	
		c.appendExten("_%s" % self.set, "Set(lastnum=${DB(%s_LASTNUM/%s/${CALLERIDNUM})})" % (self.type, self.pbx))
		c.appendExten("_%s" % self.set, 'GotoIf($["${lastnum}" = ""]?nonumber)')
		c.appendExten("_%s" % self.set, "Goto(%s,%s${lastnum},1)" % (self.pbx, self.set))
		c.appendExten("_%s" % self.set, "Goto(%s,%s,1)" % (self.pbx, self.ext), label="nonumber")
		c.appendExten("_%s" % self.set, "Goto(%s,%s,1)" % (self.pbx, self.ext), label="switchoff")
		c.appendExten("_%s." % self.set, "Answer()")
		if self.toggle:
			c.appendExten("_%s." % self.set, "Set(testcf=${DB(%s/%s/${CALLERIDNUM})})" % (self.type, self.pbx))
			c.appendExten("_%s." % self.set, 'GotoIf($["${testcf}" != ""]?switchoff)')	
		c.appendExten("_%s." % self.set, "Set(DB(%s/%s/${CALLERIDNUM})=${EXTEN:%d})" % (self.type, self.pbx,len(self.set)))
		c.appendExten("_%s." % self.set, "Set(DB(%s_LASTNUM/%s/${CALLERIDNUM})=${EXTEN:%d})" % (self.type, self.pbx,len(self.set)))
		if self.devstateprefix:
			c.appendExten("_%s." % self.set, "Devstate(%s_%s_${CALLERIDNUM},2)" % (self.type.lower(), self.pbx))
		if self.type == "CFIM":
			c.appendExten("_%s." % self.set, "Playback(call-fwd-unconditional)")
		elif self.type == "CFTO":
			c.appendExten("_%s." % self.set, "Playback(call-fwd-no-ans)")
		else:
			c.appendExten("_%s." % self.set, "Playback(call-fwd-on-busy)")
		c.appendExten("_%s." % self.set, "Wait(1)")
		c.appendExten("_%s." % self.set, "Hangup")
		c.appendExten("_%s." % self.set, "Goto(%s,%s,1)" % (self.pbx, self.ext), label="switchoff")

		c.appendExten("%s" % self.ext, "Answer()")
		c.appendExten("%s" % self.ext, "DBdel(%s/%s/${CALLERIDNUM})" % (self.type, self.pbx))
		if self.devstateprefix:
			c.appendExten("%s" % self.ext, "Devstate(%s_%s_${CALLERIDNUM},0)" % (self.type.lower(), self.pbx))
		c.appendExten("%s" % self.ext, "Playback(call-fwd-cancelled)")
		c.appendExten("%s" % self.ext, "Wait(1)")
		c.appendExten("%s" % self.ext, "Hangup")
