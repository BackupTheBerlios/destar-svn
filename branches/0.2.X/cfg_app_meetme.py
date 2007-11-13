# -*- coding: utf-8 -*-
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

class CfgAppMeetme(CfgApp):

	shortName   = _("Meeting room")
	newObjectTitle  = _("New meeting room")
	description= _("Application that let create dynamic conferencing rooms")
	
	def createVariables(self):
		self.variables   = [
			VarType("pbx",
				title=_("Virtual PBX"),
				type="choice",
				options=getChoice("CfgOptPBX")),

			VarType("ext",
				title=_("Extension"),
				len=6),

			VarType("timeout",
				title=_("Maximun duration in seconds?"),
				type="int",
				default=1200,
				len=6),

		       	VarType("confno",
				title=_("Conference number"),
				optional=True,
				type="int",
				len=6),

		       	VarType("pin",
				title=_("PIN"),
				optional=True,
				type="int",
				len=6),
			
			VarType("recordLab",
				title=_("Recording"),
				type="label"),

	                VarType("record",
				title=_("Record conferences?"),
				type="bool",
				optional=True),
			
			VarType("recordfilename",
					title=_("Monitor file name"),
					hint=_("Otherwise it will use Date-CallerIdName(CallerIdNum)-Exten"),
					len=25,
					optional=True),

			VarType("recordfileformat",
					title=_("Monitor file format"),
					type="choice",
					options=(	("gsm",_("GSM")),
							("wav",_("WAV")),
							("wav49",_("WAV49"))), 
					default="gsm"),

			VarType("recordappend",
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
				title=_("Show this trunk in the panel"),
				type="bool",
				hide=True,
				optional=True)]
			
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]
	
	def fixup(self):
		Cfg.fixup(self)
		self.lookPanel()

	def createAsteriskConfig(self):
		needModule("chan_zap")
		needModule("app_meetme")

		c = AstConf("extensions.conf")
		c.setSection(self.pbx)

		mon_line=""
		if self.record:
			needModule("app_mixmonitor")
			options = ""
			if self.recordappend:
				options = 'a' 
			if self.heardvol == self.spokenvol:
				options = options+'W(%s)' % (self.heardvol)
			else:          
				options = options+'v(%s)V(%s)' % (self.heardvol, self.spokenvol)        
			if self.recordfilename:
				mon_line = "MixMonitor(%s.%s|%s)" % (self.recordfilename,self.recordfileformat,options)
			else:
				mon_line = "MixMonitor(${TIMESTAMP}-${CALLERIDNAME}(${CALLERIDNUM})-${EXTEN}.%s|%s)" % (self.recordfileformat,options)

		c.appendExten(self.ext, "Answer")
		if mon_line:
			c.appendExten(self.ext, mon_line)
		c.appendExten(self.ext, "Set(TIMEOUT(absolute)=%d)" % self.timeout)
		# 'd' -- dynamically add conference
		# 'P' -- always prompt pin
		args=""
		if self.confno:
			args += "%d" % self.confno
		args += "|d"
		if self.pin:
			args += "P|%d" % self.pin
		c.appendExten(self.ext, "MeetMe(%s)" % args)

		if self.confno:
			c = AstConf("meetme.conf")
			c.setSection("rooms")
			room = str(self.confno)
			if self.pin:
				room += ",%d" % self.pin
			c.append("conf=%s" % room)
		try:
			if panelutils.isConfigured() == 1 and self.panel:
				panelutils.createMeetmeButton(self)
		except AttributeError:
			pass
