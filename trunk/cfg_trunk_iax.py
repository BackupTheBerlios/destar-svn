# -*- coding: iso-latin-1 -*-
# Copyright (C) 2004 Michael Bielicki
# based on Free World Dialup Module by Hoger Schurig
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
import panelutils


class CfgTrunkIaxtrunk(CfgTrunk):

	shortName   = _("Standard IAX Trunk")

	description = _("""Used to setup an IAX trunk to another Asterisk server or an IAX termination.""")

	variables	= [
		VarType("name",       title=_("Name"), len=15, default="iaxtrunk"),
		VarType("id",         title=_("IAX username"),   len=6),
		VarType("pw",         title=_("IAX password"), len=15),
		VarType("host",       title=_("IAX host"), len=25),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True),

		VarType("Inbound",    title=_("Calls from IAX trunk"), type="label"),
		VarType("contextin",      title=_("Go to"), type="radio", hide=True, default='phone',
		                               options=[('phone',_("Phone")),('autoatt',_("Auto_Attendant"))]),
		VarType("phone",      title=_("Extension to ring"), type="choice", optional=False,
		                               options=getChoice("CfgPhone")),
		VarType("dial", hide=True, len=50),
		]

	technology = "IAX2"
	
	def fixup(self):
		CfgTrunk.fixup(self)
		
        def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res

       	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_iax2")
		#Dial part to use on dialout macro
		self.dial = "IAX2/%s:%s@%s/${ARG1}" % (self.id, self.pw, self.host)
		#What to do with incoming calls
		self.createIncomingContext()
		
		c = AstConf("iax.conf")
		c.setSection("general")
		c.append("register=%s:%s@%s" % (self.id, self.pw, self.host))
		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("context=in-%s" % self.name)
			c.append("auth=md5")
			c.append("host=%s" % self.host)
			c.append("secret= %s" % self.pw)
		
		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
