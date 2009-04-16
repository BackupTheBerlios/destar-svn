# -*- coding: utf-8 -*-
# Copyright (C) 2007 Alejandro Rios P.
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


class CfgTrunkSipSPA400(CfgTrunk):

	shortName   = _("SPA400 SIP Trunk")
	newObjectTitle  = _("New SPA400 SIP trunk")
	description = _("""Used to setup a SIP trunk to a SPA400 gateway.""")
	technology = "SIP"

	def createVariables(self):
		self.variables   = [
			VarType("name",
				title=_("Name"),
				len=15,
				default="siptrunk"),
			
			VarType("host",
				title=_("SIP host"),
				len=25),

			VarType("nat",
				title=_("Is the trunk behind NAT?"),
				type="bool"),
				
			VarType("panelLab",
				title=_("Operator Panel"),
				type="label",
				hide=True),
				
			VarType("panel",
				title=_("Show this trunk in the panel"),
				type="bool",
				hide=True),

			VarType("Inbound",
				title=_("For incoming calls through this trunk:"),
				type="label"),
				
			VarType("clid",
				title=_("Change Caller*Id to:"),
				len=25,
				optional=True),

			VarType("clidnumin",
				title=_("Change Caller*Id Number to:"),
				len=40,
				optional=True),
			
			VarType("contextin",
				title=_("Go to"),
				type="radio",
				default='phone',
				options=[('phone',_("Phone")),('ivr',_("IVR")),('pbx',_("Virtual PBX"))]),
			
			VarType("phone",
				title=_("Extension to ring"),
				type="choice",
				optional=True,
				options=getChoice("CfgPhone")),
			
			VarType("ivr",
				title=_("IVR to jump to"),
				type="choice",
				optional=True,
				options=getChoice("CfgIVR")),

			VarType("pbx",
				title=_("Allow dial extension from which Virtual PBX"),
				type="choice",
				optional=True,
				options=getChoice("CfgOptPBX")),

			VarType("dial",
				hide=True,
				len=80),]

		self.dependencies = [
			DepType("phone", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("ivr", 
					type="hard",
					message = _("This is a Dependency"))
		]


	def checkConfig(self):
		res = CfgTrunk.checkConfig(self)
		if res:
			return res
		
	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_sip")

		self.dial = "SIP/${ARG1}@%s" % (self.name)
		
		#What to do with incoming calls
		self.createIncomingContext()
		
		c = AstConf("sip.conf")

		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("username=%s" % self.name)
			c.append("user=%s" % self.name)
			c.append("host=%s" % self.host)
			c.append("context=in-%s" % self.name)
			c.append("canreinvite=no")
			c.append("dtmfmode=auto")
			if self.nat:
				c.append("nat=yes")
			c.append("insecure=very")

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
