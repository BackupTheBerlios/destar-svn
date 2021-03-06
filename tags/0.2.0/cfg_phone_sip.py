# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2005 by Holger Schurig,
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
import md5


class CfgPhoneSip(CfgPhone):

	shortName = _("Normal SIP phone")
	newObjectTitle = _("New SIP phone")
	description = _("This is a SIP phone account, to be used by hard-phones, soft-phones, ATAs, etc.")
	technology = "SIP"
	
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
					len=15),

			VarType("host",
					title=_("IP address of phone"),
					optional=True,
					len=15),
					
			VarType("nat",
					title=_("Is the trunk behind NAT ?"),
					type="bool",
					optional=True),

			VarType("ext",
					title=_("Extension"),
					len=13),
					
			VarType("dtmfmode",
					title=_("DTMF mode:"),
					type="choice",
					options=(
						("rfc2833",_("RFC 2833 (RTP)")),
						("inband",_("In Band (only with ulaw/alaw)")),
						("info",_("SIP INFO")) ), default="info"),
	
			VarType("Call Group",
					title=_("Call group"),
					type="label"),
			
			VarType("enablecallgroup",
					title=_("Enable call group"),
					type="bool",
					optional=True,
					default=False), 
					
			VarType("callgroup",
					title=_("Call group number"),
					optional=True),
	
			VarType("QueueLab",
					title=_("Call Queues"),
					type="label",
					hide=True),
			
			VarType("queues",
					title=_("Agent of queues:"),
					type="mchoice",
					optional=True,
					options=getChoice("CfgPhoneQueue"),
					hide=True),
	
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
					type="label",
					len=6),
					
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
			
			VarType("email",
					title=_("Voicemail email"),
					optional=True,
					len=60),
			
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
				if dep.name.startswith('dialout_'):
					obj_name = dep.name[8:] # get the name after "dialout_"
				else:
					obj_name = self.__dict__[dep.name]
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
		needModule("chan_sip")
		needModule("app_authenticate")

		sip = AstConf("sip.conf")
		sip.setSection(self.name)
		sip.append("type=friend")
		sip.append("qualify=yes")
		m = md5.new()
		m.update('%s:asterisk:%s' % (self.name,self.secret))
		sip.append("md5secret=%s" % m.hexdigest())
		sip.append("host=dynamic")
		if self.host:
			sip.appendValue(self, "host", "defaultip")
		sip.append("dtmfmode=%s" % self.dtmfmode)
		sip.append("context=out-%s" % self.name)
		sip.append("canreinvite=no")

		if self.calleridname:
			sip.append('callerid="%s" <%s>' % (self.calleridname, self.ext))
		else:
			sip.append('callerid="%s" <%s>' % (self.name,self.ext))

		if self.enablecallgroup:
			sip.append('callgroup=%s' % self.callgroup)
			sip.append('pickupgroup=%s' % self.callgroup)

		if self.nat:
			sip.append("nat=yes")

        	try:
            		pbx = self.pbx
        	except AttributeError:
            		pbx = "phones"
		sip.append("subscribecontext=%s" % pbx)

		self.createExtensionConfig()
		self.createHintConfig()
		self.createVoicemailConfig(sip)
		self.createOutgoingContext()
		self.createPanelConfig()
		self.createQueuesConfig()
