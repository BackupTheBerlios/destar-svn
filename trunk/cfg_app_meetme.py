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
	description= _("Application that allows the creation of dynamic conferencing rooms")
	
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
		c.setSection("%s-apps" % self.pbx)
		c.appendExten(self.ext, "Answer", self.pbx)
		c.appendExten(self.ext, "Set(TIMEOUT(absolute)=%d)" % self.timeout, self.pbx)
		# 'd' -- dynamically add conference
		# 'P' -- always prompt pin
		args=""
		if self.confno:
			args += "%d" % self.confno
		args += ",d"
		if self.pin:
			args += "P,%d" % self.pin
		c.appendExten(self.ext, "MeetMe(%s)" % args, self.pbx)

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
