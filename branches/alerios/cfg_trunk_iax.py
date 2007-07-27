# -*- coding: utf-8 -*-
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
	newObjectTitle  = _("New standard IAX trunk")
	description = _("""Used to setup an IAX trunk to another Asterisk server or an IAX termination.""")
	technology = "IAX2"
	
	def createVariables(self):
		self.variables	= [
			VarType("name",
				title=_("Name"),
				len=30,
				default="iaxtrunk"),

			VarType("id",
				title=_("IAX username"),
				len=15),

			VarType("host",
				title=_("IAX host"),
				len=80),

			VarType("port",
				title=_("IAX2 remote port"),
				type="int",
				default=4569,
				len=5),				

			VarType("bandwidth",
				title=_("Bandwith"),
				type="choice",
				len=25,
				options=[('low',_("Low")),('high', _("High"))]),

			VarType("register",
				title=_("Register with remote host?"),
				type="bool"),
		
			VarType("authLabel",
				title=_("Authentication"),
				type="label"),

			VarType("auth",
				title=_("Authentication Method"),
				type="radio",
				default="plain",
				options=[('plain',_("Plain text")),('rsa',_("RSA")),('md5',_("MD5"))]),

			VarType("pw",
				title=_("Password"),
				hint=_("For 'Plain' or 'MD5' only"),
				len=80,
				optional=True),
				
			VarType("inkeys",
				title=_("Public key from remote server"),
				hint=_("For 'RSA' only"),
				len=80,
				optional=True),

			VarType("outkey",
				title=_("Private local key"),
				hint=_("For 'RSA' only"),
				len=80,
				optional=True),

			VarType("trunk",
				title=_("Enable trunking?"),
				type="bool",
				hide=True),

			VarType("panelLab",
				title=_("Operator Panel"),
				type="label",
				hide=True),

			VarType("panel",
				title=_("Show this trunk in the panel"),
				type="bool",
				hide=True,
				optional=True),

			VarType("Inbound",
				title=_("For incoming calls through this trunk:"),
				type="label"),

			VarType("clid",
				title=_("Change Caller*Id to:"),
				len=40,
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

			VarType("Outbound",
				title=_("For outgoing calls through this trunk:"),
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
				len=50),
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
		needModule("chan_iax2")

		#Dial part to use on dialout macro
		self.dial = "IAX2/%s/${ARG1}" % self.name
		#What to do with incoming calls
		self.createIncomingContext()
		
		c = AstConf("iax.conf")

		if self.register:
			c.setSection("general")
			registerstr = "register => %s" % self.id
			if self.auth == "plain":
				registerstr += ":%s" % self.pw
			# TODO: registration using rsa keys 
			#elif self.auth = "rsa":
			registerstr += "@%s" % self.host
			if self.port:
				registerstr += ":%s" % self.port
			c.append(registerstr)

		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("host=%s" % self.host)
			c.append("username=%s" % self.id)
			c.append("context=in-%s" % self.name)
			c.append("bandwidth=%s" % self.bandwidth)
			c.append("qualify=yes")
			if self.trunk:
				c.append("trunk=yes")
			if self.auth == "rsa" and self.inkeys and self.outkey:		
				c.append("auth=rsa")
				c.append("inkeys=%s" % self.inkeys)
				c.append("outkey=%s" % self.outkey)
			elif self.auth == "md5":
				c.append("auth=md5")
				c.append("secret= %s" % self.pw)
			elif self.auth == "plain":
				c.append("secret= %s" % self.pw)

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
