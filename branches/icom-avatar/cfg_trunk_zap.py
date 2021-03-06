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


class CfgTrunkDAHDI(CfgTrunk):

	shortName = _("Standard ZAP trunk")
	newObjectTitle = _("New standard ZAP trunk")
	technology = "ZAP"
	def createVariables(self):
		self.variables = [
			VarType("name",
				title=_("Name"),
				len=35),

			VarType("channels",
				title=_("DAHDItel channel number"),
				type="string",
				len=5),

			VarType("signalling",
				title=_("Signalling type"),
				type="choice",
				options=[('fxs_ls',_('loopstart')),
					('fxs_ks',_('kewlstart'))]),

			VarType("group",
				title=_("Callout group"),
				type="int",
				optional=True),

			VarType("panelLab",
				title=_("Operator Panel"),
				type="label",
				hide=True),

			VarType("panel",
				title=_("Show this trunk in the panel"),
				type="bool",
				hide=True,
				optional=True),

			VarType("Gains",
				title=_("Reception and Transmission Gains"),
				type="label"),

			VarType("rxgain",
				title=_("Reception gain"),
				hint=_("in dB"),
				optional=True,
				default="0.0"),

			VarType("txgain",
				title=_("Transmission gain"),
				hint=_("in dB"),
				optional=True,
				default="0.0"),

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
				optional=False,
				options=getChoice("CfgPhone")),

			VarType("ivr",
				title=_("IVR to jump to"),
				type="choice",
				optional=True,
				options=getChoice("CfgIVR")),

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
				len=50),]

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

	def fixup(self):
		CfgTrunk.fixup(self)
		if not self.rxgain:
			self.rxgain = "0.0"
		if not self.txgain: 
			self.txgain = "0.0"


	def createAsteriskConfig(self):
		needModule("chan_dahdi")

		c = AstConf("system.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("fxs%s=%s" % (self.signalling[4:], self.channels))
		c.append("")

		# Create config for chan_dahdi:
		c = AstConf("chan_dahdi.conf")
		c.append("")
		c.append("; DAHDItel Trunk %s" % self.name)
		c.append("context=in-%s" % self.name)
		c.append("callerid=asreceived")
                c.append("busydetect=yes")
                c.append("busycount=8")
		c.appendValue(self, "signalling")
		c.appendValue(self, "rxgain")
		c.appendValue(self, "txgain")
		if self.group:
			c.appendValue(self, "group")
		c.append("channel=%s" % self.channels)
		c.append("")

		#Dial part to use on dialout macro
		if self.group:
			self.dial = "DAHDI/g%d/${ARG1}" % (self.group)
		else:
			self.dial = "DAHDI/%s/${ARG1}" % (self.channels)
		
		#What to do with incoming calls
		self.createIncomingContext()

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)

