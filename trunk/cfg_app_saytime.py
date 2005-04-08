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


class CfgAppSayTime(CfgApp):

	shortName   = _("Say time")
	variables   = [VarType("ext", title=_("Extension"), len=6),
		       VarType("what", title=("Say what"), type="choice", options=[
				("kM"   , _("Time")),
				("dbY"  , _("Date")),
				("dbYkM", _("Date and Time"))] )]

	def createAsteriskConfig(self):
		needModule("app_sayunixtime")

		c = AstConf("extensions.conf")
		c.setSection("default")
		c.appendExten(self.ext, "Answer")
		c.appendExten(self.ext, "Wait(1)")
		c.appendExten(self.ext, "SayUnixTime(,,%s)" % self.what)
		c.appendExten(self.ext, "Hangup")
