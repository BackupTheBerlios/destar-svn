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


class CfgOptDAHDITrunk(CfgOptSingle):

	shortName = _("DAHDItel Trunk Options")
	newObjectTitle = _("DAHDItel Trunk Options")
	
	def createVariables(self):
		self.variables = [
			VarType("busydetect", title=_("Try to detect busy signal to detect if remote site hung up"), type="bool"),
			VarType("busycount",  title=_("Wait how many busy signals before hanging up"), type="int", default=5),
			#VarType("callprogress", title=_("?"), type="bool"),
		]


	def isAddable(self):
		"""We can only add this configlet if we have at least one
		ZAP trunk defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__.startswith('CfgTrunkDAHDI'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("chan_dahdi.conf")
		c.setSection("channels")

		c.append("")
		c.append("; %s" % self.shortName)
		c.appendValue(self, "busydetect")
		c.appendValue(self, "busycount")
