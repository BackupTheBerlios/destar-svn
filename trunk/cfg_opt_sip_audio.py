# -*- coding: iso-latin-1 -*-
#
# This module is Copyright (C) 2005 by Alejandro Rios,
# Destar is Copyright (C) 2005 by Holger Schurig,
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


class CfgOptSipAudio(CfgOptSingle):

	shortName = _("SIP Audio Options")
	variables = [
		VarType("Codecs"  ,   title=_("Codecs to use"), optional=True, type="label"),
		VarType("alaw", title=_("Allow alaw codec"), optional=True, type="bool"),
		VarType("ulaw", title=_("Allow ulaw codec"), optional=True, type="bool"),
		VarType("ilbc", title=_("Allow ilbc codec"), optional=True, type="bool"),
	]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
                if res:
                        return res
		if (self.alaw == False ) and (self.ulaw == False) and (self.ilbc == False):
                        return ("alaw", _("You should choose at least one codec"))


	def isAddable(self):
		"""We can only add this configlet if we have at least one
		SIP phone/trunk defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.__class__.__name__ in ('CfgPhoneSip','CfgTrunkSip'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("sip.conf")
		if self.alaw:
			c.append("allow=alaw")
		if self.ulaw:
			c.append("allow=ulaw")
		if self.ilbc:
			c.append("allow=ilbc")

