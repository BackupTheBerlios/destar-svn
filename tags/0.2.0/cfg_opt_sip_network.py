# -*- coding: iso-latin-1 -*-
#
# This module is Copyright (C) 2005 by Francesco Crescioli,
# Heavly based on module cfg_opt_sip_audio Copyright (C) 2005 by Alejandro Rios,
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


class CfgOptSipNetwork(CfgOptSingle):

	shortName = _("SIP Network Options")
	newObjectTitle = _("SIP Network Options")
	
	def createVariables(self):
		self.variables = [
			VarType("doBind",	title=_("Bind specific address?"), type="bool"),
			VarType("bindaddr",	title=_("Bind address"), len=25),
			VarType("extintnet",	title=_("External/Internal IP"), type="label"),
			VarType("setExt",	title=_("Force external ip/internel network?"),	type="bool"),
			VarType("extip",	title=_("External ip"), len=25),
			VarType("intnet",	title=_("Internal network"), len=25),
			VarType("intnetmask",	title=_("Netmask"), len=25),
		]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
                if res:
                        return res

	def isAddable(self):
		"""We can only add this configlet if we have at least one
		SIP phone/trunk defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ in ('CfgPhoneSip','CfgTrunkSip'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("sip.conf")
		if self.doBind:
			c.append("bindaddr=%s" % self.bindaddr)
		if self.setExt:
			c.append("externip=%s" % self.extip)
			c.append("localnet=%s/%s" % (self.intnet,self.intnetmask))
