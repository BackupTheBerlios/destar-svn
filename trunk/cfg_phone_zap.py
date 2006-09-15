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
	newObjectTitle = _("New ZAP phone")
	technology = "ZAP"
	
	def createVariables(self):
		self.variables = [
			VarType("pbx",    
				title=_("Virtual PBX"), 
				type="choice", 
				options=getChoice("CfgOptPBX")),

			VarType("name",
				title=_("Name"),
				len=35),

			VarType("channels",
				title=_("Zaptel channel number"),
				type="string",
				len=5),

			VarType("sigtype",
				title=_("Signalling type"),
				type="choice",
				options=[('ls','loopstart'),
					('ks', 'kewlstart')]),
				
			VarType("group",
				title=_("Group"),
				type="int",
				optional=True),
				
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
				title=_("Show this phone in the panel"),
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
		c.append("context=out-%s" % self.name)

		if self.group:
			c.appendValue(self, "group")
		c.append("txgain=0.0")
		c.append("rxgain=0.0")
		c.append("channel=%s" % self.channels)
		c.append("")

		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("fxo%s=%s" % (self.sigtype, self.channels))
		c.append("")

		if self.enablecallgroup:
			c.append('callgroup=%s' % self.callgroup)
			c.append('pickupgroup=%s' % self.callgroup)

		self.createExtensionConfig()
		self.createVoicemailConfig(c)
		self.createOutgoingContext()
		self.createPanelConfig()

	def channelString(self):
		return "%s/%s" % (self.technology, self.channels)


	def createDialEntry(self, extensions, exten, pbx, ext):
		ret = extensions.appendExten(exten, "Macro(dial-std-exten,%s/%s,out-%s,%d,%s,%s)" % (
			self.technology,
			self.channels,
			self.name,
			int(self.usevm),
			pbx,
			ext)
		      )
