# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig
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
from language import _


class CfgPhoneMGCP(CfgPhone):

	shortName = _("Standard MGCP phone")
	variables = [VarType("name",            title=_("Name"), len=15),
			VarType("secret",       title=_("Password"), optional=True, len=6),
			VarType("host",         title=_("IP address of phone"), len=15),
			VarType("ext",          title=_("Extension"), optional=True, len=6
			# This can wait until we have popup-windows
			#hint=_("""If you define an extension, then you can call the
			#	phone with this number. A phone without an extension can still
			#	be used as a target for direct dialin or calling groups.""")
			),
			VarType("nat",          title=_("NAT"), type="bool", optional=True),
			VarType("threeway",     title=_("Three way calling"), type="bool", optional=True),
			VarType("transfer",     title=_("Enable Call transfer"), type="bool", optional=True),
			VarType("forward",	title=_("Enable Call forward"), type="bool", optional=True),
			VarType("did",          title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),

			VarType("Outbound",     title=_("Calls from the phone"), type="label"),
			VarType("calleridnum",  title=_("Caller-Id-number"), optional=True),
			VarType("calleridname",	title=_("Caller-Id-Name"), optional=True),

			VarType("Voicemail",    title=_("Voicemail settings"), type="label", len=6),
			VarType("usevm",        title=_("Use voicemail"), type="bool", optional=True),
			VarType("usemwi",       title=_("Signal waiting mail"), type="bool", optional=True),
			VarType("pin",          title=_("Voicemail PIN"), optional=True, len=6),
			]

	technology = "MGCP"

	def createAsteriskConfiglet(self):
		needModule("chan_mgcp")

		mgcp = AstConf("mgcp.conf")
		mgcp.setSection(self.host)
		mgcp.append("host=%s" % self.host)
		mgcp.append("transfer=%s" % self.transfer)
		mgcp.append("threewaycalling=%s" % self.threeway)
		mgcp.append("callwaiting=no")
		mgcp.append("nat=%s" % self.nat)
		mgcp.append("cancallforward=%s" % self.forward)
		if self.calleridname and self.calleridnum:
			mgcp.append('callerid="%s" <%s>' % (self.calleridname, self.calleridnum))
		elif self.calleridname:
			mgcp.append('callerid="%s"' % self.calleridname)
		elif self.calleridnum:
			mgcp.append('callerid=%s' % self.calleridnum)

		self.createExtensionConfig()
		self.createVoicemailConfig(mgcp)
