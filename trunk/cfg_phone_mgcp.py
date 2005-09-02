# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Michael Bielicki, TAAN Softworks Corp.
# Based on work by Holger Schurig
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


class CfgPhoneMGCP(CfgPhone):

	shortName = _("Normal MGCP phone")
	variables = [VarType("name",            title=_("Name"), len=15, hint=_("""If you haven't configured a name for your phone please use the IP address here.""")),
			VarType("secret",       title=_("Password"), optional=True, len=6),
			VarType("host",         title=_("IP address of phone"), len=15),
			VarType("ext",          title=_("Extension"), optional=True, len=6
	
			),
			VarType("nat",          title=_("NAT"), type="bool", optional=True),
			VarType("threeway",     title=_("Three way calling"), type="bool", optional=True),
			VarType("transfer",     title=_("Enable Call transfer"), type="bool", optional=True),
			VarType("forward",	title=_("Enable Call forward"), type="bool", optional=True),
			VarType("did",          title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),

			VarType("Call Group",   title=_("Call group"), type="label"),
			VarType("enablecallgroup", title=_("Enable call group"), type="bool", optional=False, default=False), 
			VarType("callgroup",  title=_("Call group number"), optional=True),

			VarType("Voicemail",    title=_("Voicemail settings"), type="label", len=6),
			VarType("usevm",        title=_("Use voicemail"), type="bool", optional=True),
			VarType("usemwi",       title=_("Signal waiting mail"), type="bool", optional=True),
			VarType("pin",          title=_("Voicemail PIN"), optional=True, len=6),

			VarType("Outbound",     title=_("Calls from the phone"), type="label"),
			VarType("calleridnum",  title=_("Caller-Id-Number"), optional=True),
			VarType("calleridname",	title=_("Caller-Id-Name"), optional=True),
			VarType("Dialout"  ,   title=_("Allowed dialout-entries"), type="label",hide=True),
			VarType("timeout",     title=_("Enable time restriction?"), type="bool", optional=True,hide=True),
		]

	technology = "MGCP"

	def fixup(self):
		import configlets
		dialouts=False
		for obj in configlets.config_entries:
			if obj.groupName == 'Dialout':
				dialouts=True
				alreadyappended = False
				for v in self.variables:	
					if v.name == "dialout_"+obj.name:
						alreadyappended = True
				if not alreadyappended:
					self.variables.append(VarType("dialout_%s" % obj.name, title=_("%s") % obj.name, type="bool", optional=True,render_br=False))
					self.variables.append(VarType("dialout_%s_secret" % obj.name, title=_("Password:"), len=50, optional=True))
		if dialouts:
			for v in self.variables:
				if v.name == "Dialout" or v.name=="timeout":
					v.hide = False

	def createAsteriskConfig(self):
		needModule("chan_mgcp")

		mgcp = AstConf("mgcp.conf")
		mgcp.setSection(self.host)
		mgcp.append("host=%s" % self.host)
		mgcp.append("transfer=%s" % self.transfer)
		mgcp.append("threewaycalling=%s" % self.threeway)
		mgcp.append("callwaiting=no")
		mgcp.append("nat=%s" % self.nat)
		mgcp.append("context=out-%s" % self.name)
		mgcp.append("cancallforward=%s" % self.forward)
		if self.calleridname and self.calleridnum:
			mgcp.append('callerid="%s" <%s>' % (self.calleridname, self.calleridnum))
		elif self.calleridname:
			mgcp.append('callerid="%s"' % self.calleridname)
		elif self.calleridnum:
			mgcp.append('callerid=<%s>' % self.calleridnum)

		if self.enablecallgroup:
			mgcp.append('callgroup=%s' % self.callgroup)
			mgcp.append('pickupgroup=%s' % self.callgroup)

		self.createExtensionConfig()
		self.createVoicemailConfig(mgcp)
		self.createOutgoingContext()
