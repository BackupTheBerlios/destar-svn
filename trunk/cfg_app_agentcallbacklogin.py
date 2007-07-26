# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2007 by Holger Schurig
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

class CfgAppAgentCallbackLogin(CfgApp):

	shortName   = _("Agent Callback login/logout extensions")
	newObjectTitle  = _("New agent callback login and logout extensions")
	description = _("""This application allows an agent to log into the system.""")
	
	def createVariables(self):
		self.variables = [
			VarType("pbx",
					title=_("Virtual PBX"),
					type="choice",
					options=getChoice("CfgOptPBX")),

			VarType("ext",
					title=_("Login extension"),
					len=6),

			VarType("changeext",
					title=_("Change location"),
					len=6),

			VarType("logoutext",
					title=_("Logout extension"),
					len=6),

			VarType("silentlogin",
					title=_("Silent login"),
					type="bool",
					optional=True),
			]

		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
			]

	def createAsteriskConfig(self):
		needModule("chan_agent")
		needModule("chan_local")
	
		c = AstConf("extensions.conf")
		c.setSection(self.pbx)

		if self.silentlogin:
			opts = "s"
		else:
			opts = ""
		
		c.appendExten(self.ext, "AgentCallbackLogin(${CALLERIDNUM}|%s|${CALLERIDNUM}@%s)" % (opts, self.pbx), self.pbx )
		c.appendExten(self.ext, "DBdel(DND/%s/${CALLERIDNUM})", self.pbx)
		c.appendExten(self.ext, "Playback(do-not-disturb)", self.pbx)
		c.appendExten(self.ext, "Playback(cancelled)", self.pbx)
		c.appendExten(self.ext, "Hangup", self.pbx)

		c.appendExten(self.changeext, "AgentCallbackLogin(${CALLERIDNUM}|%s|'#')" % (opts), self.pbx )
		c.appendExten(self.logoutext, "Dial(Local/%s@%s/n,,D(#))" % (self.changeext, self.pbx), self.pbx)

