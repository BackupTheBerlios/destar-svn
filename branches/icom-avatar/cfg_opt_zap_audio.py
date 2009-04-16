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


echo_samples=[0, 16, 32, 64, 128, 256]

class CfgOptDAHDIAudio(CfgOptSingle):

	shortName = _("DAHDItel Audio Options")
	newObjectTitle = _("DAHDItel Audio Options")
	
	def createVariables(self):
		self.variables = [
			VarType("relaxdtmf", title=_("Be sloppy when detecting DTMF"), type="bool"),
			VarType("echocancel", title=_("Echo cancel samples"), type="choice",
						  options=zip(echo_samples, echo_samples),
						  default=128),
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
			if obj.__class__.__name__.startswith('CfgTrunkDAHDI') or obj.__class__.__name__.startswith('CfgPhoneDAHDI'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("chan_dahdi.conf")
		c.setSection("channels")

		c.append("")
		c.append("; %s" % self.shortName)
                c.append("usecallingpres=yes")
                c.append("threewaycalling=yes")
                c.append("transfer=yes")
                c.append("cancallforward=yes")
                c.append("callreturn=no")
                c.appendValue(self, "relaxdtmf")
		c.append("echocancel=%s" % str(self.echocancel))
                c.appendValue(self, "echocancelwhenbridged")
                c.append("echotraining=yes")

