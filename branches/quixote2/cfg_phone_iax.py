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
	newObjectTitle = _("New IAX phone")
	technology = "IAX2"
	def createVariables(self):
		self.variables = [
			VarType("pbx",    
				title=_("Virtual PBX"), 
				type="choice", 
				options=getChoice("CfgOptPBX")),

			VarType("name",
					title=_("Name"),
					len=15),

			VarType("secret",
					title=_("Password"),
					optional=True,
					len=15),

			VarType("host",
					title=_("IP address of phone"),
					optional=True,
					len=15),

			VarType("ext",
					title=_("Extension"),
					len=6),

			VarType("did",
					title=_("Allow direct dialling from outside?"),
					type="bool",
					hide=True,
					default=False),
	
			VarType("Call Group",
					title=_("Call group"),
					type="label"),

			VarType("enablecallgroup",
					title=_("Enable call group"),
					type="bool",
					optional=False,
					default=False), 

			VarType("callgroup",
					title=_("Call group number"),
					optional=True),
	
			VarType("panelLab",
					title=_("Operator Panel"),
					type="label",
					hide=True),

			VarType("panel",
					title=_("Show this extension in the panel"),
					type="bool",
					hide=True,
					optional=True),
	
			VarType("Voicemail",
					title=_("Voicemail settings"),
					type="label"),

			VarType("usevm",
					title=_("Use voicemail"),
					type="bool",
					optional=True),

			VarType("usemwi",
					title=_("Signal waiting mail"),
					type="bool",
					optional=True),

			VarType("pin",
					title=_("Voicemail PIN"),
					optional=True,
					len=6),

			VarType("notransfer",
					title=_("Skip asterisk media path?"),
					type="bool"),
	
			VarType("Outbound",
					title=_("Calls from the phone"),
					type="label"),

			VarType("calleridnum",
					title=_("Caller-Id Number"),
					optional=True),

			VarType("calleridname",
					title=_("Caller-Id Name"),
					optional=True),

			VarType("Monitoring",
					title=_("Monitoring"),
					type="label",
					len=6),

			VarType("monitor",
					title=_("Monitor calls made from this extension?"),
					optional=True,
					type="bool"),

			VarType("monitorfilename",
					title=_("Monitor file name"),
					hint=_("Otherwise it will use Date-CallerIdName(CallerIdNum)-Exten"),
					len=25,
					optional=True),

			VarType("monitorfileformat",
					title=_("Monitor file format"),
					type="choice",
					options=(       ("gsm",_("GSM")),
							("wav",_("WAV")),
							("wav49",_("WAV49"))),
					default="gsm"),

			VarType("monitorappend",
					title=_("Append to existing file instead of overwriting it?"),
					optional=True,
					type="bool"),

			VarType("monitorwhenbridged",
					title=_("Save audio only while the channel is bridged?"),
					hint=_("Does not include conferences"),
					optional=True,
					type="bool"),

			VarType("heardvol",
					title=_("Heard volume factor"),
					type="choice",
					options=(       ("+4",_("+4")),
					("+3",_("+3")),
					("+2",_("+2")),
					("+1",_("+1")),
					("0",_("0")),
					("-1",_("-1")),
					("-2",_("-2")),
					("-3",_("-3")),                   
					("-4",_("-4"))),	
					default="0"),

			VarType("spokenvol",
					title=_("Spoken volume factor"),
					type="choice",
					options=(       ("+4",_("+4")),
					("+3",_("+3")),
					("+2",_("+2")),
					("+1",_("+1")),
					("0",_("0")),
					("-1",_("-1")),
					("-2",_("-2")),
					("-3",_("-3")),                   
					("-4",_("-4"))),
					default="0"),
					
			VarType("Dialout",
					title=_("Allowed dialout-entries"),
					type="label",
					hide=True),

			VarType("timeout",
					title=_("Enable time restriction?"),
					type="bool",
					optional=True,
					hide=True),]

		if varlist_manager.hasDialouts():
			self.variables += varlist_manager.getDialouts()
			for v in self.variables:
				if v.name == "Dialout" or v.name=="timeout":
					v.hide = False
					
		queues = len(configlet_tree.getConfigletsByName('CfgPhoneQueue'))
		if queues > 0:
			for v in self.variables:
				if v.name == "QueueLab" or v.name == "queues":
					v.hide = False
		self.dependencies = [
			DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
			]
		for var in self.__dict__.keys():
			if var.startswith('dialout_'):
				self.dependencies.append(
					DepType(var,
							type="hard",
							message = _("This is a Dependency")))

	def createDependencies(self):
		for dep in self.dependencies:
			if self.__dict__.has_key(dep.name):
				obj_name = dep.name[8:] # get the name after "dialout_"
				import configlets
				obj = configlets.configlet_tree.getConfigletByName(obj_name)
				if obj is None:
					return
				dependent_obj = DependentObject(self, dep)
				obj.dependent_objs.append(dependent_obj)

	def isAddable(self):
		"We can only add this object if we have at least one pbx defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		if len(configlets.configlet_tree.getConfigletsByName('CfgOptPBX')) > 0:
			return True
		return False
	isAddable = classmethod(isAddable)

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

		if not self.notransfer:
			iax.append("notransfer=yes")

		self.createExtensionConfig()
		self.createVoicemailConfig(iax)
		self.createOutgoingContext()
		self.createPanelConfig()
