# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig,
# add ons by Michael Bielicki, TAAN Softworks Corp.
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


class CfgPhoneSip(CfgPhone):

	shortName = _("Standard SIP phone")
	variables = [
		VarType("name",       title=_("Name"), len=15),
		VarType("secret",     title=_("Password"), optional=True, len=6),
		VarType("host",       title=_("IP address of phone"), len=15),
		VarType("nat",        title=_("Is the trunk behind NAT ?"), type="bool", optional=True),
		VarType("ext",        title=_("Extension"), optional=True, len=6),
		VarType("did",        title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),

		VarType("Outbound",   title=_("Calls from the phone"), type="label"),
		VarType("callerid",   title=_("Caller-Id"), optional=True),

		VarType("Voicemail",  title=_("Voicemail settings"), type="label", len=6),
		VarType("usevm",      title=_("Use voicemail"), type="bool", optional=True),
		VarType("usemwi",     title=_("Signal waiting mail"), type="bool", optional=True),
		VarType("pin",        title=_("Voicemail PIN"), optional=True, len=6),
	]
	technology = "SIP"

	def createAsteriskConfiglet(self):
		needModule("chan_sip")

		sip = AstConf("sip.conf")
		sip.setSection(self.name)
		sip.append("type=friend")
		sip.append("qualify=yes")
		sip.appendValue(self, "secret")
		sip.append("host=dynamic")
		sip.appendValue(self, "host", "defaultip")
		sip.append("dtmfmode=info")
		sip.append("canreinvite=no")
		if self.callerid:
			sip.appendValue(self, "callerid")
		if self.nat:
			sip.append("nat=yes")
		self.createExtensionConfig()
		self.createVoicemailConfig(sip)
