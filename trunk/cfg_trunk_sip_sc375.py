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


class CfgTrunkSipSC375(CfgTrunk):

	shortName   = _("SC-375 SIP Trunk")
	newObjectTitle  = _("New SC375 SIP trunk")
	description = _("""Used to setup a SC-375 SunComm's GSM GW.""")
	technology = "SIP"
	
	def createVariables(self):
		self.variables   = [
			VarType("name",
				title=_("Name"),
				len=15,
				default="siptrunk"),
			
			VarType("pw",
				title=_("SIP password"),
				len=15),

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
				title=_("Calls from SIP trunk"),
				type="label"),
				
			VarType("clid",
				title=_("Change Caller*Id to:"),
				len=25,
				optional=True),
			
			VarType("contextin",
				title=_("Go to"),
				type="radio",
				default='phone',
				options=[('phone',_("Phone")),('ivr',_("IVR")),('pbx',_("Virtual PBX"))]),
			
			VarType("phone",
				title=_("Extension to ring"),
				type="choice",
				optional=False,
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

		#Dial part to use on dialout macro
		#If we use the host it will not use authentication
		#it's safe to use the peer name 
		self.dial = "SIP/${ARG1}@%s" % (self.name)
		
		#What to do with incoming calls
		self.createIncomingContext()
		
		c = AstConf("sip.conf")
		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("username=%s" % self.name)
			c.append("regexten=%s" % self.name)
			c.append("fromuser=%s" % self.name)
			c.append("secret=%s" % self.pw)
			c.append("host=dynamic")
			c.append("insecure=very")
			c.append("context=in-%s" % self.name)
			c.append("canreinvite=no")
			c.append("dtmfmode=inband")
			c.append("call-limit=1")
			if self.nat:
				c.append("nat=yes")
			c.append("qualify=yes")
			c.append("disallow=all")
			c.append("allow=ulaw")
			c.append("allow=alaw")

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
