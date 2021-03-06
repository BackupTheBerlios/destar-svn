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


class CfgOptRtp(CfgOptSingle):

	shortName = _("RTP options")
	newObjectTitle= _("RTP options")

	def createVariables(self):
		self.variables = [
			VarType("rtpstart", type="int", title=_("Start of RTP port area"), default=16384),
			VarType("rtpend",   type="int", title=_("End of RTP port area"),   default=16482),
			VarType("rtpchecksums", type="bool", title=_("Check UDP checksums of RTP packets"), default=True),
		]

	def row(self):
		return (self.shortName, "%d - %d" % (self.rtpstart, self.rtpend))


	def checkConfig(self):
		ret = CfgOpt.checkConfig(self)
		if ret:
			return ret

		if self.rtpstart > self.rtpend:
			return ("rtpend", _("must be higher than start value"))


	def createAsteriskConfig(self):
		c = AstConf("rtp.conf")
		c.appendValue(self, "rtpstart")
		c.appendValue(self, "rtpend")
		c.appendValue(self, "rtpchecksums")
