# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2005 by Holger Schurig,
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


class CfgPhoneZap(CfgPhone):

	shortName = _("Normal ZAP phone")
	variables = [
		VarType("name",       title=_("Name"), len=35),
		VarType("channel",    title=_("Zaptel channel number"), type="string", len=5),
		VarType("sigtype",    title=_("Signalling type"), type="choice",
	                              options=[('ls','loopstart'),('ks', 'kewlstart')]),
		VarType("ext",        title=_("Extension"), optional=True, len=6),
		VarType("did",        title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),
		
		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this phone in the panel"), type="bool", hide=True),

		VarType("Outbound",     title=_("Calls from the phone"), type="label"),
		VarType("calleridnum",  title=_("Caller-Id Number"), optional=True),
		VarType("calleridname", title=_("Caller-Id Name"), optional=True),

		VarType("Call Group",   title=_("Call group"), type="label"),
		VarType("enablecallgroup", title=_("Enable call group"), type="bool", optional=False, default=False), 
		VarType("callgroup",  title=_("Call group number"), optional=True),
		
		VarType("Voicemail",  title=_("Voicemail settings"), type="label", len=6),
		VarType("usevm",      title=_("Use voicemail"), type="bool", optional=True),
		VarType("usemwi",     title=_("Signal waiting mail"), type="bool", optional=True),
		VarType("pin",        title=_("Voicemail PIN"), optional=True, len=6),
	]
	technology = "ZAP"


	def fixup(self):
		CfgPhone.fixup(self)
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False


	def createAsteriskConfig(self):
		needModule("chan_zap")

		# Create config for chan_zap:
		c = AstConf("zapata.conf")
		c.append("signalling=fxo_%s" % self.sigtype)

		if self.calleridname and self.calleridnum:
			c.append('callerid="%s" <%s>' % (self.calleridname, self.calleridnum))
		elif self.calleridname:
			c.append('callerid="%s"' % self.calleridname)
		elif self.calleridnum:
			c.append('callerid=%s' % self.calleridnum)

		c.append("group=1")
		# TODO?
		c.append("context=default")
		c.append("txgain=0.0")
		c.append("rxgain=0.0")
		c.append("channel=%s" % self.channel)
		c.append("")

		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("fxo%s=%s" % (self.sigtype, self.channel))
		c.append("")

		if self.enablecallgroup:
			sip.append('callgroup=%s' % self.callgroup)
			sip.append('pickupgroup=%s' % self.callgroup)

		self.createExtensionConfig()
		self.createVoicemailConfig(c)
	
		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)

	def channelString(self):
		return "%s/%s" % (self.technology, self.channel)


	def createDialEntry(self, extensions, ext):
		ret = extensions.appendExten(ext, "Macro(dial-std-exten,%s/%s,%s,%d)" % (
			self.technology,
			self.channel,
			"phones",
			int(self.usevm))
		      )
