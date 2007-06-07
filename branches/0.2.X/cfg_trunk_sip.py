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


class CfgTrunkSiptrunk(CfgTrunk):

	shortName   = _("Standard SIP Trunk")
	newObjectTitle  = _("New standard SIP trunk")
	description = _("""Used to setup a SIP trunk to a SIP provider or a different SIP server.""")
	technology = "SIP"
	
	def createVariables(self):
		self.variables   = [
			VarType("name",
				title=_("Name"),
				len=15,
				default="siptrunk"),
			
			VarType("id",
				title=_("SIP username"),
				len=15),
			
			VarType("pw",
				title=_("SIP password"),
				len=15),

			VarType("host",
				title=_("SIP host"),
				len=25),

			VarType("port",
				title=_("SIP port"),
				type="int",
				default=5060,
				len=5),				
				
			VarType("register",
				title=_("Register with remote host?"),
				type="bool"),
				
			VarType("forward",
				title=_("Enable forward address type?"),
				type="bool"),

			VarType("nat",
				title=_("Is the trunk behind NAT?"),
				type="bool"),
				
			VarType("insecure",
				title=_("Bypass auth for incoming calls?"),
				type="bool"),
	
			VarType("panelLab",
				title=_("Operator Panel"),
				type="label",
				hide=True),
				
			VarType("panel",
				title=_("Show this trunk in the panel"),
				type="bool",
				hide=True),

	    		VarType("fromdomain",
                               title=_("Sip domain:"),
                               len=40,
                               optional=True),
	
			VarType("Inbound",
				title=_("Calls from SIP trunk"),
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

 			VarType("Outbound",
 				title=_("Outgoing calls to IAX trunk"),
 				type="label"),
 
 			VarType("clidnameout",
 				title=_("Change Caller*Id Name to:"),
 				len=40,
 				optional=True),
 
 			VarType("clidnumout",
 				title=_("Change Caller*Id Number to:"),
 				len=40,
 				optional=True),

			VarType("dial",
				hide=True,
				len=80),
				]

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
		if self.register:
			self.dial = "SIP/${ARG1}@%s" % (self.name)
		else:
			self.dial = "SIP/${ARG1}@%s" % (self.host)
			if self.forward:
				self.dial += "/${ARG1}" 
		
		#What to do with incoming calls
		self.createIncomingContext()
		
		c = AstConf("sip.conf")
		c.setSection("general")
		if self.register:
			if not self.port:
				registerstr = "register => %s:%s@%s" % (self.id, self.pw, self.host)
			else:
				registerstr = "register => %s:%s@%s:%s" % (self.id, self.pw, self.host, self.port)
			if self.forward: 
				registerstr += "/%s" % self.id
			c.append(registerstr)

		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("username=%s" % self.id)
			c.append("fromuser=%s" % self.id)
			c.append("secret=%s" % self.pw)
			c.append("host=%s" % self.host)
			if self.port:
				c.append("port=%s" % self.port)
			c.append("context=in-%s" % self.name)
			c.append("canreinvite=no")
			if self.fromdomain:
				c.append("fromdomain=%s" % self.fromdomain)
			if self.nat:
				c.append("nat=yes")
			if self.insecure:
				c.append("insecure=very")

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
