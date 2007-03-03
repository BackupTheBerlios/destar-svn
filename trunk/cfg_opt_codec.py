# -*- coding: utf-8 -*-
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

################################################
# This configlet depricates cfg_opt_sip_audio.py

class CfgOptCodec(CfgOpt):

	shortName = _("Audio Codec")
	newObjectTitle = _("New audio codec to be used")
	groupName = 'Codecs'
	
	def createVariables(self):
		self.variables = [
			VarType("name", title=_("Allow codec"), type="choice",
				options=(
					("all",_("Use all codecs")),
					("speex",_("Speex")),
					("alaw",_("A Law (g711a)")),
					("ulaw",_("U Law (g711u)")),
					("gsm",_("GSM")),
					("ilbc",_("ILBC")),
					("g726",_("g726")),
					("g723",_("g723.1")),
					("g729",_("g729")),
					)
				),
		]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)

	def row(self):
		return (self.shortName, self.name)

	def createAsteriskConfig(self):
		for cf in ["sip.conf", "iax.conf"]:
			c = AstConf(cf)
			if self.name == "g723":
				c.append("allow=%s.1" % self.name)
				needModule("codec_%s_1" % self.name)
			else:	
				c.append("allow=%s" % self.name)
				needModule("codec_%s" % self.name)
