# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig
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
	description = _("""Allows you to record a sound file. You can hang up, be silent for
			a second or dial '#' to stop the recording.""")
	variables   = [
		VarType("ext",      title=_("Extension"), len=6),
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


	def checkConfig(self):
		res = CfgApp.checkConfig(self)
		if res:
			return res
		if self.filename.find(".") != -1:
			return ("filename", _("Please don't specify an extension"))


	def createAsteriskConfiglet(self):
		needModule("app_record")

		c = AstConf("extensions.conf")
		c.setSection("default")
		c.appendExten(self.ext, "AbsoluteTimeout(20)")
		c.appendExten(self.ext, "Answer")
		c.appendExten(self.ext, "Wait(1)")
		# TODO: don't hardcode ":gsm" here
		c.appendExten(self.ext, "Record(%s:%s)" % (self.filename, self.format) )
		c.appendExten(self.ext, "Hangup")
