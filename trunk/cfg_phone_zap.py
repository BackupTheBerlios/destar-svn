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


class CfgPhoneZap(CfgPhone):

	shortName = _("Normal ZAP phone")
	variables = [
		VarType("name",       title=_("Name"), len=35),
		VarType("channel",    title=_("Zaptel channel number"), type="string", len=5),
		VarType("sigtype",    title=_("Signalling type"), type="choice",
	                              options=[('ls','loopstart'),('ks', 'kewlstart')]),
		VarType("ext",        title=_("Extension"), optional=True, len=6),
		VarType("did",        title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),

		VarType("Outbound",   title=_("Calls from the phone"), type="label"),
		VarType("callerid",   title=_("Caller-Id"), optional=True),

		VarType("Voicemail",  title=_("Voicemail settings"), type="label", len=6),
		VarType("usevm",      title=_("Use voicemail"), type="bool", optional=True),
		VarType("usemwi",     title=_("Signal waiting mail"), type="bool", optional=True),
		VarType("pin",        title=_("Voicemail PIN"), optional=True, len=6),
	]
	technology = "ZAP"


	def createAsteriskConfig(self):
		needModule("chan_zap")

		# Create config for chan_zap:
		c = AstConf("zapata.conf")
		c.append("signalling=fxo_%s" % self.sigtype)
		if self.callerid:
			c.appendValue(self, "callerid")
		else: # must add an empty value, because it may be set elsewhere
			c.append("callerid=")
		c.append("group=1")
		# TODO?
		c.append("context=default")
		c.append("channel=%s" % self.channel)
		c.append("")

		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("fxo%s=%s" % (self.sigtype, self.channel))
		c.append("")

		self.createExtensionConfig()
		self.createVoicemailConfig(c)
	

	def channelString(self):
		return "%s/%s" % (self.technology, self.channel)


	def createDialEntry(self, extensions, ext):
		ret = extensions.appendExten(ext, "Macro(dial-std-exten,%s/%s,%s,%d)" % (
			self.technology,
			self.channel,
			"phones",
			int(self.usevm))
		      )
