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


class CfgOptRtp(CfgOptSingle):

	shortName = _("RTP options")
	variables = [VarType("rtpstart",
			     type="int",
			     title=_("Start of RTP port area"),
			     hint="hint",
			     default=16384),
		     VarType("rtpend",
			     type="int",
			     title=_("End of RTP port area"),
			     default=16482)]

	def row(self):
		return (self.shortName, "%d - %d" % (self.rtpstart, self.rtpend))


	def checkConfig(self):
		ret = CfgOpt.checkConfig(self)
		if ret:
			return ret

		if self.rtpstart < self.rtpend:
			return ("rtpend", _("must be higher as start value"))


	def createAsteriskConfiglet(self):
		c = AstConf("rtp.conf")
		c.appendValue(self, "rtpstart")
		c.appendValue(self, "rtpend")
