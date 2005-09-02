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


class CfgPhoneIax(CfgPhone):

	shortName = _("Normal IAX phone")
	variables = [
		VarType("name",            title=_("Name"), len=15),
		VarType("secret",       title=_("Password"), optional=True, len=6),
		VarType("host",         title=_("IP address of phone"), optional=True, len=15),
		VarType("ext",	        title=_("Extension"), optional=True, len=6),
		VarType("did",	        title=_("Allow direct dialling from outside?"), type="bool", hide=True, default=False),

		VarType("Call Group",   title=_("Call group"), type="label"),
		VarType("enablecallgroup", title=_("Enable call group"), type="bool", optional=False, default=False), 
		VarType("callgroup",  title=_("Call group number"), optional=True),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this extension in the panel"), type="bool", hide=True),

		VarType("Voicemail",    title=_("Voicemail settings"), type="label"),
		VarType("usevm",        title=_("Use voicemail"), type="bool", optional=True),
		VarType("usemwi",       title=_("Signal waiting mail"), type="bool", optional=True),
		VarType("pin",	        title=_("Voicemail PIN"), optional=True, len=6),
		VarType("notransfer",   title=_("Disable IAX transfer"), type="bool"),

		VarType("Outbound",     title=_("Calls from the phone"), type="label"),
		VarType("calleridnum",  title=_("Caller-Id Number"), optional=True),
		VarType("calleridname", title=_("Caller-Id Name"), optional=True),
		VarType("Dialout"  ,   title=_("Allowed dialout-entries"), type="label",hide=True),
		VarType("timeout",     title=_("Enable time restriction?"), type="bool", optional=True,hide=True),
	]
	technology = "IAX2"

	def fixup(self):
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False

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
		needModule("res_crypto")
		needModule("chan_iax2")
														    
		iax = AstConf("iax.conf")
		iax.setSection(self.name)
		iax.append("type=friend")
		iax.appendValue(self, "secret")
		iax.append("host=dynamic")
		iax.appendValue(self, "host", "defaultip")
		iax.append("context=out-%s" % self.name)
		if self.calleridname and self.calleridnum:
			iax.append('callerid="%s" <%s>' % (self.calleridname, self.calleridnum))
		elif self.calleridname:
			iax.append('callerid="%s"' % self.calleridname)
		elif self.calleridnum:
			iax.append('callerid=<%s>' % self.calleridnum)
		
		if self.enablecallgroup:
			iax.append('callgroup=%s' % self.callgroup)
			iax.append('pickupgroup=%s' % self.callgroup)

		iax.append("notransfer=%s" % self.notransfer)

		self.createExtensionConfig()
		self.createVoicemailConfig(iax)

		c = AstConf("extensions.conf")
		c.setSection("out-%s" % self.name)
		c.append("include=>phones")

		try:
			timeoutvalue = not self.timeout and "0" or "1"
		except AttributeError:
			timeoutvalue=0
		import configlets
		for obj in configlets.config_entries:
			if obj.__class__.__name__ == 'CfgDialoutNormal':
				try:
					if self.__getitem__("dialout_"+obj.name):
						secret = self.__getitem__("dialout_%s_secret" % obj.name)
						if secret:
							c.append("exten=>%s,1,Macro(%s,{EXTEN},%s,%s)" % (obj.pattern,obj.name,secret,timeoutvalue))	
						else:
							c.append("exten=>%s,1,Macro(%s,{EXTEN},-,%s)" % (obj.pattern,obj.name,timeoutvalue))	
				except KeyError:
					pass

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createExtButton(self)

