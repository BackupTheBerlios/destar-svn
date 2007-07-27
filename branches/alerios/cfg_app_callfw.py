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
			VarType("unset",   title=_("Unsetting extension"), len=6, default="*22"),
			VarType("toggle",   title=_("Set function toggleable"), type="bool"),
			VarType("devstateprefix",   title=_("Create Devstate extension. Devstate Prefix:"), len=8, optional=True, default="")
		       	]

		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
	
	def row(self):
		return ("%s / %s" % (self.set,self.unset),"%s %s" % (self.shortName, self.type), self.pbx)

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
		if self.type == "CFIM":
			msg = "call-fwd-unconditional"
		elif self.type == "CFTO":
			msg = "call-fwd-no-ans"
		else:
			msg = "call-fwd-on-busy"
		if self.devstateprefix:
		    needModule("app_devstate")
		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten(self.set, "Goto(cfw-%s,s,1)" % self.set, self.pbx)
		c.appendExten(self.set, "Hangup", self.pbx)
		c.appendExten("_%s." % self.set, "Macro(call-forward,%s,%s,${EXTEN:%d},%s)" % (self.type,self.pbx,len(self.set),msg), self.pbx)
		c.appendExten("_%s." % self.set, "Hangup", self.pbx)
		c.appendExten("%s" % self.unset, "Answer()", self.pbx)
		c.appendExten("%s" % self.unset, "DBdel(%s/%s/${CALLERIDNUM})" % (self.type, self.pbx), self.pbx)
		if self.devstateprefix:
			c.appendExten("%s" % self.unset, "Devstate(%s_%s_${CALLERIDNUM},0)" % (self.type, self.pbx), self.pbx)
		c.appendExten("%s" % self.unset, "Playback(call-fwd-cancelled)", self.pbx)
		c.appendExten("%s" % self.unset, "Wait(1)", self.pbx)
		c.appendExten("%s" % self.unset, "Hangup", self.pbx)

		context="cfw-%s" % self.set
		c.setSection(context)
		if self.toggle:
			c.appendExten("s", "Set(testcf=${DB(%s/%s/${CALLERIDNUM})})" % (self.type, self.pbx), context)
			c.appendExten("s", 'GotoIf($["${testcf}" != ""]?switchoff)', context)	
		c.appendExten("s", "Set(TIMEOUT(digit)=2)", context)
		c.appendExten("s", "Set(lastnum=${DB(%s_LASTNUM/%s/${CALLERIDNUM})})" % (self.type, self.pbx), context)
		c.appendExten("s", 'GotoIf($["${lastnum}" = ""]?nonumber)', context)
		c.appendExten("s","Background(press-1&to-enter-a-number&or&press-2&for&vm-last&number)", context)
		c.appendExten("s","WaitExten(3)", context)
		c.appendExten("s","Hangup()", context)
		c.appendExten("s", "Goto(1,1)", context, label="nonumber")
		c.appendExten("s", "Goto(%s,%s,1)" % (self.pbx, self.unset), context, label="switchoff")
		c.appendExten("2","Macro(call-forward,%s,%s,${lastnum},%s)" % (self.type,self.pbx,msg), context)
		if self.devstateprefix:
			c.appendExten("2", "Devstate(%s_%s_${CALLERIDNUM},2)" % (self.type.lower(), self.pbx), context)
		c.appendExten("1", "Playback(please-enter-the&number&after-the-tone&beep)", context)
		c.appendExten("1","WaitExten(5)", context)
		c.appendExten("_X.","Macro(call-forward,%s,%s,${EXTEN},%s)" % (self.type,self.pbx,msg), context)
		if self.devstateprefix:
			c.appendExten("_X.", "Devstate(%s_%s_${CALLERIDNUM},2)" % (self.type.lower(), self.pbx), context)

