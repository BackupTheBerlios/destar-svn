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


class CfgAppRecord(CfgApp):

	shortName   = _("Record sound")
	newObjectTitle  = _("New recording extension")
	description = _("""Allows you to record a sound file. You can be silent for
			a second or dial '#' to stop the recording.""")
			
	def createVariables(self):
		self.variables   = [
			VarType("pbx",    title=_("Virtual PBX"), type="choice", options=getChoice("CfgOptPBX")),
			VarType("ext",      title=_("Extension"), len=6),
			VarType("max",      title=_("Max duration"), len=6, default=0),
			VarType("filename", title=_("File name")),
			VarType("format",   title=_("Sound format"), type="choice",
				options=(("gsm", _("GSM compression")),
					 ("ulaw",_("PCM format 'ulaw'")),
					 ("alaw",_("alaw")),
					 ("vox", _("vox")),
					 ("wav", _("WAV-File with Microsoft PCM, 16 bit, mono 8000 Hz")),
					 ("WAV", _("WAV-File with GSM 6.10 compression, mono 8000 Hz")),
					),
				default="WAV")
		]
		self.dependencies = [ DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
					]


	def checkConfig(self):
		res = CfgApp.checkConfig(self)
		if res:
			return res
		if self.filename.find(".") != -1:
			return ("filename", _("Please don't specify an extension"))


	def createAsteriskConfig(self):
		needModule("app_record")

		c = AstConf("extensions.conf")
		c.setSection(self.pbx)
		c.appendExten(self.ext, "Goto(record-%s,s,1)" % self.filename)
		c.appendExten(self.ext, "Hangup")
		c.setSection("record-%s" % self.filename)
		c.append("exten => s,1,Macro(record,%s,%s,%s)" % (self.filename, self.format, self.max))
		c.append("exten => s,n(menu),Background(press-1&to-listen-to-it&or&press-2&to-rerecord-yr-message)")
		c.append("exten => s,n,WaitExten(5)")
		c.append("exten => s,n,Hangup()")
		c.append("exten => 1,1,Playback(%s)" % self.filename)
		c.append("exten => 1,n,Goto(s,menu)")
		c.append("exten => 2,1,Goto(s,1)")
