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
import panelutils


class CfgTrunkZap(CfgTrunk):

	shortName = _("Standard ZAP trunk")
	variables = [
		VarType("name",       title=_("Name"), len=35),
		VarType("channel",    title=_("Zaptel channel number"), type="string", len=5),
		VarType("signalling", title=_("Signalling type"), type="choice",
		                      options=[('fxs_ls','loopstart'),('fxs_ks', 'kewlstart')]),
		VarType("group",      title=_("Callout group"), type="int", default=1, optional=True),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True),

		VarType("Gains",      title=_("Reception and Transmission Gains"), type="label"),
		VarType("rxgain",     title=_("Reception gain"), hint=_("in dB"), optional=True, default="0.0"),
		VarType("txgain",     title=_("Transmission gain"), hint=_("in dB"), optional=True, default="0.0"),
	
		VarType("Inbound",    title=_("Calls from SIP trunk"), type="label"),
		VarType("contextin",      title=_("Go to"), type="radio", hide=True, default='phone',
		                               options=[('phone',_("Phone")),('autoatt',_("Auto_Attendant"))]),
		VarType("phone",      title=_("Extension to ring"), type="choice", optional=False,
		                               options=getChoice("CfgPhone")),
		VarType("dial", hide=True, len=50),
		]
	technology = "ZAP"

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
		needModule("chan_zap")

		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("fxs%s=%s" % (self.signalling[4:], self.channel))
		c.append("")

		# Create config for chan_zap:
		c = AstConf("zapata.conf")
		c.append("")
		c.append("; Zaptel Trunk %s" % self.name)
		contextin = "in-%s" % self.name
		c.append("context=%s" % contextin)
		c.append("callerid=asreceived")
		c.appendValue(self, "signalling")
		c.appendValue(self, "rxgain")
		c.appendValue(self, "txgain")
		if self.group:
			c.appendValue(self, "group")
		c.appendValue(self, "channel")
		c.append("")

		#Dial part to use on dialout macro
		if self.group:
			self.dial = "Zap/g%d%/${ARG1}" % (self.group)
		else:
			self.dial = "Zap/%s/${ARG1}" % (self.channel)
		
		#What to do with incoming calls
		c = AstConf("extensions.conf")
		c.setSection(contextin)
		if self.contextin == 'phone' and self.phone:
			c.appendExten("s", "Goto(phones,%s,1)" % self.phone)
		elif self.contextin == 'autoatt':
			import configlets
			for obj in configlets.config_entries:
				if obj.__class__.__name__ == 'CfgOptAutoatt':
					try:
						autoatt = self.__getitem__("autoatt_%s" % obj.name)
						if autoatt:
							time = self.__getitem__("autoatt_%s_time" % obj.name)
							if time:
								c.append("include=>%s|%s" % (obj.name,time))
							else:
								c.append("include=>%s" % obj.name)
					except KeyError:
						pass


		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)

