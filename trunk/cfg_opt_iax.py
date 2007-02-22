# -*- coding: iso-latin-1 -*-
#
# This module is Copyright (C) 2007 by dasenjo,
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


class CfgOptIAX(CfgOptSingle):

	shortName = _("IAX Options")
	newObjectTitle = _("IAX Options")
	
	def createVariables(self):
		self.variables = [
			VarType("bindaddr",	
					title=_("Bind address"), 
					len=25,
					optional=True),

			VarType("bindport",	
					title=_("Bind port"), 
					type="int",
					len=25,
					optional=True),

			VarType("jitterbuffer",	
					title=_("Use jitterbuffer?"), 
					type="bool",
					optional=True),

			VarType("forcejitterbuffer",	
					title=_("Force jitterbuffer?"), 
					type="bool",
					optional=True),

			VarType("tos",
					title=_("TOS Field"),
					len=14,
					optional=True,
					default="lowdelay"),]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
                if res:
                        return res

	def isAddable(self):
		"""We can only add this configlet if we have at least one
		IAX phone/trunk defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ in ('CfgPhoneIax','CfgTrunkIaxtrunk'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("iax.conf")
		c.setSection("general")
		if self.bindaddr:
			c.append("bindaddr=%s" % self.bindaddr)
		if self.bindport:
			c.append("bindport=%s" % self.bindport)
		if self.jitterbuffer:
			c.append("jitterbuffer=yes")
		if self.forcejitterbuffer:
			c.append("forcejitterbuffer=yes")
		if self.tos:
			c.append("tos=%s" % self.tos)
