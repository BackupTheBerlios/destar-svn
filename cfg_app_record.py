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
from language import _


class CfgAppRecord(CfgApp):

	shortName   = _("Record sound")
	description = _("""Allows you to record a sound file. You can hang up, be silent for
			a second or dial '#' to stop the recording.""")
	variables   = [VarType("ext",      title=_("Extension"), len=6),
		       VarType("filename", title=_("File name"))]

	def createAsteriskConfiglet(self):
		needModule("app_record")

		c = AstConf("extensions.conf")
		c.setSection("default")
		c.appendExten(self.ext, "AbsoluteTimeout(20)")
		c.appendExten(self.ext, "Answer")
		c.appendExten(self.ext, "Wait(1)")
		# TODO: don't hardcode ":gsm" here
		# TODO strip any extension or display an error if the user enters an extension
		c.appendExten(self.ext, "Record(%s:gsm)" % self.filename)
		c.appendExten(self.ext, "Hangup")
