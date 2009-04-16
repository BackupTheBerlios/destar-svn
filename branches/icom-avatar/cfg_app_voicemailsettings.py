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

class CfgAppVoicemailSettings(CfgApp):

	shortName   = _("Voicemail settings")
	description = _("Extensions to set/unset voicemail.")
	newObjectTitle = _("New extensions to set/unset voicemail")

	def createVariables(self):
		self.variables = [ 
			VarType("pbx",
				title=_("Virtual PBX"),
				type="choice",
				options=getChoice("CfgOptPBX")),
			VarType("type",
				title=_("Type"),
				type="choice",
					options=( ("VMIM", _("Voicemail Unconditional")), \
					("VMBS", _("Voicemail if Busy")),
					("VMU", _("Voicemail if Timeout/Unavailable")) )),
			VarType("set",
				title=_("Setting preffix"),
				len=6,
				default="*94"),
			VarType("ext",
				title=_("Unsetting extension"),
				len=6,
				default="*95"),
			VarType("toggle",
				title=_("Set function toggleable"),
				type="bool"),
			VarType("devstateprefix",
				title=_("Create Devstate extension. Devstate Prefix:"),
				len=8,
				optional=True,
				default="")
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
		c.setSection("%s-apps" % self.pbx)
		c.appendExten("%s" % self.set, "Answer()", self.pbx)
		if self.toggle:
			c.appendExten("%s" % self.set, "Set(togglestate=${DB(%s/%s/${CALLERID(num)})})" % (self.type, self.pbx), self.pbx)
			c.appendExten("%s" % self.set, 'GotoIf($["${togglestate}" != ""]?switchoff)', self.pbx)
		c.appendExten("%s" % self.set, "Set(DB(%s/%s/${CALLERID(num)})=1)" % (self.type, self.pbx), self.pbx)
		if self.devstateprefix:
			c.appendExten("%s" % self.set, "Devstate(%s_%s_${CALLERID(num)},2)" % (self.type.lower(), self.pbx), self.pbx)
		if self.type == "VMIM":
			c.appendExten("%s" % self.set, "Playback(voice-mail-system)", self.pbx)
			c.appendExten("%s" % self.set, "Playback(activated)", self.pbx)
		elif self.type == "VMU":
			c.appendExten("%s" % self.set, "Playback(voice-mail-system)", self.pbx)
			c.appendExten("%s" % self.set, "Playback(activated)", self.pbx)
		else:
			c.appendExten("%s" % self.set, "Playback(voice-mail-system)", self.pbx)
			c.appendExten("%s" % self.set, "Playback(activated)", self.pbx)
		c.appendExten("%s" % self.set, "Wait(1)", self.pbx)
		c.appendExten("%s" % self.set, "Hangup", self.pbx)
		c.appendExten("%s" % self.set, "Goto(%s,%s,1)" % (self.pbx, self.ext), self.pbx, label="switchoff")
		c.appendExten("%s" % self.ext, "Answer()", self.pbx)
		c.appendExten("%s" % self.ext, "DBdel(%s/%s/${CALLERID(num)})" % (self.type, self.pbx), self.pbx)
		if self.devstateprefix:
			c.appendExten("%s" % self.ext, "Devstate(%s_%s_${CALLERID(num)},0)" % (self.type.lower(), self.pbx), self.pbx)
		c.appendExten("%s" % self.ext, "Playback(voice-mail-system)", self.pbx)
		c.appendExten("%s" % self.ext, "Playback(cancelled)", self.pbx)
		c.appendExten("%s" % self.ext, "Wait(1)", self.pbx)
		c.appendExten("%s" % self.ext, "Hangup", self.pbx)
