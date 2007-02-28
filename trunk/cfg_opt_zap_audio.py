# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Holger Schurig,
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


class CfgOptZapAudio(CfgOptSingle):

	shortName = _("Zaptel Audio Options")
	newObjectTitle = _("Zaptel Audio Options")
	
	def createVariables(self):
		self.variables = [
			VarType("relaxdtmf", title=_("Be sloppy when detecting DTMF"), type="bool"),
			VarType("echocancel", title=_("Echo cancel samples"), type="choice",
									  options=["0 (no echo cancel)", "16", "32", "64", "128", "256"], default="128"),
			VarType("echocancelwhenbridged", title=_("Cancel echo even on bridged calls"), type="bool"),
			VarType("echotraining", title=_("Do early echo training"), type="bool"),
		]


	def isAddable(self):
		"""We can only add this configlet if we have at least one
		ZAP phone/trunk defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ in ('CfgPhoneZap','CfgTrunkZap'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("zapata.conf")
		c.setSection("channels")

		c.append("")
		c.append("; %s" % self.shortName)
                c.append("usecallingpres=yes")
                c.append("threewaycalling=yes")
                c.append("transfer=yes")
                c.append("cancallforward=yes")
                c.append("callreturn=no")
                c.appendValue(self, "relaxdtmf")
                c.appendValue(self, "echocancel")
                c.appendValue(self, "echocancelwhenbridged")
                c.append("echotraining=yes")

