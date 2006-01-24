# -*- coding: iso-latin-1 -*-
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
import panelutils


class CfgPhoneQueue(CfgPhone):

	shortName = _("Normal Call Queue")
	variables = [
		VarType("name",       title=_("Name"), len=15),
		VarType("ext",        title=_("Extension"), optional=True, len=6),
		VarType("timeout",    title=_("Timeout"), optional=True, len=6),
		VarType("moh",	  title=_("Music-on-hold class"), type="choice", optional=True,
			options=getChoice("CfgOptMusic")),
		VarType("strategy",    title=_("Strategy:"), type="choice",
                	options=( ("ringall",_("Ring all - ring all available channels until one answers")),
                        	  ("roundrobin",_("Round robin - take turns ringing each available interface")),
                                  ("leastrecent",_("Least recent - ring interface which was least recently called by this queue")), 
                                  ("fewestcalls",_("Fewest calls - ring the one with fewest completed calls from this queue")), 
                                  ("random",_("Random - ring random interface")), 
                                  ("rrmemory",_("Round robin with memory - remember where we left off last ring pass")) 
				), 
			default="ringall"),
		VarType("retry",        title=_("How long to wait before trying all the members again?"), optional=True, len=6),

		VarType("Announces",  title=_("Announces"), type="label", len=6),
		VarType("announce",  title=_("Announce queue position to caller?"), type="bool"),
		VarType("announcefrequency", title=_("How often to announce queue position and/or estimated holdtime to caller"), optional=True, len=6),
		VarType("announceholdtime",    title=_("Include estimated hold time in position announcements?"), type="choice",
                	options=( ("yes",_("Yes")),
                        	  ("no",_("No")),
                                  ("once",_("Only Once"))
				), 
			default="no"),

		VarType("Monitoring",  title=_("Monitoring"), type="label", len=6),
		VarType("monitor",        title=_("Monitor answered calls?"), type="bool"),
		VarType("monitorfileformat",    title=_("Monitor file format"), type="choice",
                	options=( ("gsm",_("GSM")),
                        	  ("wav",_("WAV")),
                                  ("wav49",_("WAV49"))
				), 
			default="gsm"),
		VarType("monitorfilename",  title=_("Monitor file name"), hint=_("Otherwise it will use ${UNIQUEID}"), len=25, optional=True),
		VarType("monitorjoin",        title=_("Split file on inbound and outbound channels?"), type="bool"),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this queue in the panel"), type="bool", hide=True, optional=True),
	]
	technology = "Virtual"

	def fixup(self):
		Cfg.fixup(self)
		useContext("phones")

		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False
	def checkConfig(self):
                res = CfgPhone.checkConfig(self)
                if res:
                        return res
		if self.announce and not self.announcefrequency:
			return ('announcefrequency',_("You should select a frequency"))

		
	def createAsteriskConfig(self):
		needModule("res_monitor")
		needModule("app_queue")

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
		if self.monitor:
			c.append("monitor-format=%s" % self.monitorfileformat)
			if not self.monitorjoin:
				c.append("monitor-join=yes")
		
		extensions = AstConf("extensions.conf")
		extensions.setSection("phones")
		if self.ext:
			if self.monitor and self.monitorfilename:
				extensions.appendExten(self.ext, "SetVar(MONITOR_FILENAME=%s)" % self.monitorfilename)
			extensions.appendExten(self.ext, "SetMusicOnHold(%s)" % self.moh)
			extensions.appendExten(self.ext, "Queue(%s|Tth)" % self.name)
		if self.monitor and self.monitorfilename:
			extensions.appendExten(self.name, "SetVar(MONITOR_FILENAME=%s)" % self.monitorfilename)
		extensions.appendExten(self.name, "SetMusicOnHold(%s)" % self.moh)
		extensions.appendExten(self.name, "Queue(%s|Tth)" % self.name)
		
		try:
			if panelutils.isConfigured() == 1 and self.panel:
				panelutils.createQueueButton(self)
		except AttributeError:
			pass
