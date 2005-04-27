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


class CfgPhoneIax(CfgPhone):

	shortName = _("Normal IAX phone")
	variables = [VarType("name",            title=_("Name"), len=15),
			VarType("secret",       title=_("Password"), optional=True, len=6),
			VarType("host",         title=_("IP address of phone"), optional=True, len=15),

			VarType("Inbound",      title=_("Calls to the phone"), type="label"),
			VarType("ext",	        title=_("Extension"), optional=True, len=6),
			VarType("did",	        title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),

			VarType("Outbound",     title=_("Calls from the phone"), type="label"),
			VarType("calleridnum",  title=_("Caller-Id Number"), optional=True),
			VarType("calleridname", title=_("Caller-Id Name"), optional=True),

			VarType("Voicemail",    title=_("Voicemail settings"), type="label"),
			VarType("usevm",        title=_("Use voicemail"), type="bool", optional=True),
			VarType("usemwi",       title=_("Signal waiting mail"), type="bool", optional=True),
			VarType("pin",	        title=_("Voicemail PIN"), optional=True, len=6),
			VarType("notransfer",   title=_("can this peer transfer natively or not ?"), type="bool")
			]
	technology = "IAX2"
														    
	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_iax2")
														    
		iax = AstConf("iax.conf")
		iax.setSection(self.name)
		iax.append("type=friend")
		iax.appendValue(self, "secret")
		iax.append("host=dynamic")
		iax.appendValue(self, "host", "defaultip")
		if self.calleridname and self.calleridnum:
			iax.append('callerid="%s" <%s>' % (self.calleridname, self.calleridnum))
		elif self.calleridname:
			iax.append('callerid="%s"' % self.calleridname)
		elif self.calleridnum:
			iax.append('callerid=%s' % self.calleridnum)
		iax.appendValue("notransfer=%s", self.notransfer)
														    
		self.createExtensionConfig()
		self.createVoicemailConfig(iax)
