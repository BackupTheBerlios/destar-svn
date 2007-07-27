# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2005 by Alejandro Rios P.
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


class CfgiTrunkZapDynamic(CfgTrunk):

	shortName = _("Zaptel dynamic span configuration")
	newObjectTitle = _("Zaptel dynamic span configuration")
	technology = "ZAP"

	def createVariables(self):
		self.variables = [
			VarType("name",       
				title=_("Name"), 
				len=35),

			VarType("channels",    
				title=_("Channels"), 
				hint=_("i.e. 1-15,17-31"), 
				default="1-15,17-31",
				type="string", 
				len=20),

			VarType("dchannel",    
				title=_("Signailing channel"), 
				hint=_("i.e. 16"), 
				default="16",
				type="string", 
				len=4),

			VarType("signalling",
				title=_("Signalling type"),
				type="choice",
				options=[('pri_cpe',_('PRI signalling, CPE side')),
					('pri_net', _('PRI signalling, Network side'))]),

			VarType("group",
				title=_("Callout group"),
				type="int",
				optional=True),
	
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
				options=[('phone',_("Phone")),
					('ivr',_("IVR")),
					('pbx',_("Virtual PBX"))]),

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

			VarType("labeldynamic",
				title=_("Dynamic span configuration"),
				type="label"),

			VarType("localdriver",    
				title=_("Local driver"), 
				hint=_("i.e. eth0"), 
				type="string", 
				len=5),

			VarType("address",    
				title=_("Remote driver address"), 
				hint=_("MAC address. Use span number if needed"), 
				type="string", 
				len=20),

			VarType("numchannels",    
				title=_("Number of channels"), 
				hint=_("i.e. 31 for E1, 24 for T1"), 
				type="int", 
				default=31),

			VarType("timing",    
				title=_("Zaptel timing parameter"), 
				hint=_("Read zaptel documentation"), 
				type="int", 
				len=2),

			VarType("dial",
				hide=True,
				len=50),
			]

	def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res

	def createAsteriskConfig(self):
		needModule("chan_zap")

		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("# %s" % self.name)
		c.append("dynamic=eth,%s/%s,%d,%d" % (self.localdriver, self.address, self.numchannels, self.timing))
		c.append("bchan=%s" % self.channels)
		c.append("dchan=%s" % self.dchannel)
		c.append("")

		# Create config for chan_zap:
		c = AstConf("zapata.conf")
		c.append("")
		c.append("; Zaptel Trunk %s" % self.name)
		c.appendValue(self, "signalling")
		c.append("context=in-%s" % self.name)
		c.append("transfer=yes")
		c.append("callerid=asreceived")
		if self.group:
			c.appendValue(self, "group")
		c.append("channel=%s" % self.channels)
		c.append("")

		#Dial part to use on dialout macro
		self.dial = ""
		if self.group:
			self.dial = "Zap/g%d/${ARG1}" % (self.group)
		else:
			self.dial = "Zap/%s/${ARG1}" % (self.channels)
		
		#What to do with incoming calls
		self.createIncomingContext()

		#if panelutils.isConfigured() == 1 and self.panel:
		#	panelutils.createTrunkButton(self)

