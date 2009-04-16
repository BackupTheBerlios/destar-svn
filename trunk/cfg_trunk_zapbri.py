# -*- coding: utf-8 -*-
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
import panelutils


class CfgTrunkDAHDIBRI(CfgTrunk):

	shortName = _("Standard ZAP BRI trunk")
	newObjectTitle = _("New standard ZAP BRI trunk")
	technology = "ZAP"
	
	def createVariables(self):
		self.variables = [
			VarType("name",
				title=_("Name"),
				len=35),

			VarType("channels",
				title=_("DAHDItel channel number"),
				type="int",
				len=2,
				default = 1),

			VarType("cards", title=_("Number of lines"), type="int", default=1, len=2),

			VarType("signalling",
				title=_("Signalling type"),
				type="choice",
				options=[('bri_cpe',_('BRI signalling PTP, CPE side')),
					('bri_net', _('BRI signalling PTP, Network side')),
					('bri_cpe_ptmp',_('BRI signalling PTMP, CPE side')),
					('bri_net_ptmp',_('BRI signalling PTMP, Network side'))],
				default="bri_cpe_ptmp"),

			VarType("group",
				title=_("Callout group"),
				type="int",
				default = 1),
	
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
				title=_("Calls from BRI trunk"),
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
 				title=_("Outgoing calls to BRI trunk"),
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
		needModule("chan_dahdi")

		c = AstConf("system.conf")
		c.setSection("")
		c.destar_comment = False
		for n in range(self.cards):
			c.append("span=%d,1,3,ccs,ami" % (self.channels + n))
		for n in range(self.cards):
			c.append("bchan=%d-%d" % (self.channels + n * 3, self.channels + n * 3 + 1))
			c.append("dchan=%d" % (self.channels + n * 3 + 2))
		c.append("alaw=%d-%d" % (self.channels + n * 3, self.channels + n * 3 + 2))
		c.append("")

		# Create config for chan_dahdi:
		c = AstConf("chan_dahdi.conf")
		c.append("")
		c.append("nationalprefix = 0")
		c.append("internationalprefix = 00")
		c.append("pridialplan = dynamic")
		c.append("prilocaldialplan = local")
		c.append("echocancel=no")
		c.append("echotraining = 300")
		c.append("echocancelwhenbridged=no")
		
		c.append("switchtype=euroisdn")
		c.append("signalling=%s" % self.signalling)

		c.append("; ISDN Trunk %s" % self.name)
		c.append("context=in-%s" % self.name)
		if self.group:
			c.appendValue(self, "group")

		chanstr = ""
		for n in range(self.cards):
		    if chanstr:
			chanstr = chanstr + ","
		    chanstr = chanstr + "%d-%d" % (self.channels + n * 3 , self.channels + 1 + n * 3 )
		c.append("channel=%s" % chanstr)
		c.append("")

		#Dial part to use on dialout macro
		if self.group:
			self.dial = "DAHDI/g%d/${ARG1}" % (self.group)
		
		#What to do with incoming calls
		self.createIncomingContext()

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)

