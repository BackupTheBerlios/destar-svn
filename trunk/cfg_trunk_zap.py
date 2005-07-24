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

		VarType("Outbound",   title=_("Calls to the PSTN network"), type="label"),
		VarType("group",      title=_("Callout group"), type="int", default=1),
		VarType("ext",        title=_("Outgoing prefix"), optional=True, len=6),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this extension in the panel"), type="bool", hide=True),

		VarType("Inbound",    title=_("Incoming calls"), type="label"),
		VarType("phone",      title=_("Phone to ring"), type="choice",
		                               options=getChoice("CfgPhone")),
		
		VarType("Gains",      title=_("Reception and Transmission Gains"), type="label"),
		VarType("rxgain",     title=_("Reception gain (in dB)"), optional=True, default="0.0"),
		VarType("txgain",     title=_("Transmission gain (in dB)"), optional=True, default="0.0"),
		]

	def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res



	def fixup(self):
		CfgTrunk.fixup(self)
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False


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
		c.appendValue(self, "signalling")
		c.appendValue(self, "group")
		c.appendValue(self, "channel")
		c.appendValue(self, "rxgain")
		c.appendValue(self, "txgain")
		c.append("")

		# Write special dialout entry
		# TODO: we should not have ONE dialout entry, but several of them,
		# e.g. for local calls, national calls, foreign calls etc
		c = AstConf("extensions.conf")
		if self.ext:
			ext = "_%s." % self.ext
			context = "out-%s" % self.name
			c.setSection(context)
			c.appendExten("%s" % ext, "Dial(Zap/%s/${EXTEN:%d},60,T)" % (self.channel,len(self.ext)))
		if self.phone:
			contextin = "in-%s" % self.name
			c.setSection(contextin)
			c.appendExten("s", "Goto(phones,%s,1)" % self.phone)

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)

