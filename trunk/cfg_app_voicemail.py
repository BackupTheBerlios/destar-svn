# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2005 by Holger Schurig
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


class CfgAppVoiceMail(CfgApp):

	shortName   = _("Voicemail dialog")
	newObjectTitle  = _("New voicemail dialog")
	description = _("""Extension to enter the voicemail system.""")
	
	def createVariables(self):
		self.variables   = [ VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
			VarType("ext", title=_("Extension"), len=6),
			VarType("mailbox", title=_("Ask for user mailbox?"), type="bool", optional=True),
		]

	def createAsteriskConfig(self):
		needModule("res_adsi")
		needModule("app_voicemail")

		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten(self.ext, "Answer")
		c.appendExten(self.ext, "Wait(1)")
		if not self.mailbox:
			c.appendExten(self.ext, "VoiceMailMain(${CALLERIDNUM}@%s)" % self.pbx)
		else:
			c.appendExten(self.ext, "VoiceMailMain(@%s)" % self.pbx)
		c.appendExten(self.ext, "Hangup")
