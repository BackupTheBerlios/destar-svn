# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig,
# This file has Copyright (C) 2005 by Alejandro Rios P.
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


class CfgPhoneQueue(CfgPhone):

	shortName = _("Normal Call Queue")
	newObjectTitle = _("New Call Queue")
	technology = "QUEUE"
	groupName = "Queues"
	
	def createVariables(self):
		self.variables = [
			VarType("pbx",    
				title=_("Virtual PBX"), 
				type="choice", 
				options=getChoice("CfgOptPBX")),

			VarType("name",
					title=_("Name"),
					len=15),

			VarType("ext",
					title=_("Extension"),
					optional=True,
					len=6),

                        VarType("clid",
                                        title = _("Change Caller ID name to:"),
                                        len = 25,
                                        optional = True),

			VarType("timeout",
					title=_("Agent calling timeout"),
					optional=True,
					len=6),

			VarType("retry",
					title=_("How long to wait before trying all the members again?"),
					optional=True,
					len=6),

	                VarType("queuetimeout",
        	            		title=_("Queue timeout"),
                                	optional=True,
                                	len=6),

                	VarType("queuetimeoutext",
                        		title=_("On queue timeout forward to extension"),
                        		type="choice",
                        		optional=True,
                        		options=getChoice("CfgPhone")),

			VarType("moh",
					title=_("Music-on-hold class"),
					type="choice",
					optional=True,
					options=getChoice("CfgOptMusic")),

			VarType("ring",
					title=_("Ring instead of playing Music-on-Hold?"),
					type="bool"),

			VarType("strategy",
					title=_("Strategy:"),
					type="choice",
					options=(("ringall",_("Ring all - ring all available channels until one answers")),
						("roundrobin",_("Round robin - take turns ringing each available interface")),
						("leastrecent",_("Least recent - ring interface which was least recently called by this queue")), 
						("fewestcalls",_("Fewest calls - ring the one with fewest completed calls from this queue")), 
						("random",_("Random - ring random interface")), 
						("rrmemory",_("Round robin with memory - remember where we left off last ring pass"))), 
					default="ringall"),

			VarType("Announces",
					title=_("Announces"),
					type="label",
					len=6),

			VarType("announce",
					title=_("Announce queue position to caller?"),
					type="bool"),

			VarType("announcefrequency",
					title=_("How often to announce queue position and/or estimated holdtime to caller"),
					optional=True,
					len=6),

			VarType("announceholdtime",
					title=_("Include estimated hold time in position announcements?"),
					type="choice",
					options=( 	("yes",_("Yes")),
							("no",_("No")),
							("once",_("Only Once"))),
					default="no"),
	
			VarType("Monitoring",
					title=_("Monitoring"),
					type="label",
					len=6),

			VarType("monitor",
					title=_("Monitor answered calls?"),
					type="bool"),

			VarType("monitorfilename",
					title=_("Monitor file name"),
					hint=_("Otherwise it will use Date-CallerIdName(CallerIdNum)-Exten"),
					len=25,
					optional=True),

			VarType("monitorfileformat",
					title=_("Monitor file format"),
					type="choice",
					options=(	("gsm",_("GSM")),
							("wav",_("WAV")),
							("wav49",_("WAV49"))), 
					default="wav49"),

			VarType("monitorappend",
					title=_("Append to existing file instead of overwriting it?"),
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
					
			VarType("panelLab",
					title=_("Operator Panel"),
					type="label",
					hide=True),

			VarType("panel",
					title=_("Show this queue in the panel"),
					type="bool",
					hide=True,
					optional=True),]

		self.dependencies = [
			DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("moh", 
					type="hard",
					message = _("This is a Dependency")),

		]
	
	def checkConfig(self):
                res = CfgPhone.checkConfig(self)
                if res:
                        return res
		if self.announce and not self.announcefrequency:
			return ('announcefrequency',_("You should select a frequency"))

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
		needModule("app_queue")
		needModule("res_monitor")

		c = AstConf("queues.conf")
		c.setSection(self.name)
		if self.moh:
			c.append("musiconhold=%s" % self.moh)
		c.appendValue(self, "strategy")
		if self.retry:
			c.appendValue(self, "retry")
		if self.timeout:
			c.appendValue(self, "timeout")
		if self.announce:
			c.append("announce-frequency=%s" % self.announcefrequency)
			c.append("announce-holdtime=%s" % self.announceholdtime)
		c.append("autofill=yes")

		extensions = AstConf("extensions.conf")
		extensions.setSection(self.pbx)
		
		mon_line=""

		if self.monitor:
			needModule("app_mixmonitor")
			options = ""
			if self.monitorappend:
				options = 'a' 
			if self.heardvol == self.spokenvol:
				options = options+'W(%s)' % (self.heardvol)
			else:          
				options = options+'v(%s)V(%s)' % (self.heardvol, self.spokenvol)        
			if self.monitorfilename:
				mon_line = "MixMonitor(%s.%s,%s)" % (self.monitorfilename,self.monitorfileformat,options)
			else:
				mon_line = "MixMonitor(${STRFTIME(${EPOCH},,%%Y%%m%%d%%H%%M%%S)}-${CALLERID(num)}-${EXTEN}-${UNIQUEID}.%s,%s)" % (self.monitorfileformat,options)

		qnames = []
		if self.ext:
		    qnames.append(self.ext)
		if self.name:
		    qnames.append(self.name)

		for qname in qnames:
			opt = "Tt"
			if mon_line:
				extensions.appendExten(qname, mon_line, self.pbx)
				extensions.appendExten(qname, "Set(CDR(record)=${MIXMONITOR_FILENAME})", self.pbx)

			if self.ring:
				opt = opt + "r"

                        if self.clid:
                                needModule("func_callerid")
                                extensions.appendExten(qname,"Set(CALLERID(name)=${CALLERID(num)}-%s)" %  self.clid, self.pbx)
				
			if self.moh and not self.ring:
                                needModule("func_channel")
				extensions.appendExten(qname, "Answer", self.pbx)
				extensions.appendExten(qname, "Set(CHANNEL(musicclass)=%s)" % self.moh, self.pbx)

			if self.queuetimeout:
			#	opt = opt + "n"
				extensions.appendExten(qname, "Queue(%s,%s,,,%s)" % (self.name, opt, self.queuetimeout), self.pbx)
				if self.queuetimeoutext:
					import configlets
					obj = configlets.configlet_tree.getConfigletByName(self.queuetimeoutext)
					try:
						extensions.appendExten(qname, "Goto(%s,%s,1)" %  (obj.pbx, self.queuetimeoutext), self.pbx)
					except AttributeError:
						pass
			else:
				extensions.appendExten(qname, "Queue(%s,%s)" % (self.name, opt), self.pbx)
		self.createPanelConfig()

        def createPanelConfig(self):
                try:
                        if panelutils.isConfigured() == 1 and self.panel:
                                panelutils.createQueueButton(self)
                except AttributeError:
                        pass
