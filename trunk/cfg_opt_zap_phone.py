# -*- coding: iso-latin-1 -*-
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


class CfgOptZapPhone(CfgOptSingle):

	shortName = _("Zaptel Phone Options")
	variables = [
		VarType("adsi", title=_("Use ADSI for menu phones"), type="bool"),
		VarType("callwaiting", title=_("Signal a waiting call"), type="bool"),
		VarType("callwaitingcallerid", title=_("Send callerid during call waiting indication"), type="bool"),
		VarType("threewaycalling", title=_("Suspend a call temporarily via a hook flash"), type="bool"),
		VarType("transfer", title=_("Allow call transfer"), type="bool", default=True),
		VarType("cancallforward", title=_("Allow call forwards"), type="bool", default=True),
		VarType("callreturn", title=_("Read caller number with *69"), type="bool", default=True),
	]


	def isAddable(self):
		"""We can only add this configlet if we have at least one
		ZAP phone defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.__class__.__name__ == 'CfgPhoneZap':
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("zapata.conf")
		c.setSection("channels")

		c.append("")
		c.append("; %s" % self.shortName)
		c.appendValue(self, "adsi")
		c.appendValue(self, "callwaiting")
		c.appendValue(self, "callwaitingcallerid")
		c.appendValue(self, "threewaycalling")
		c.appendValue(self, "transfer")
		c.appendValue(self, "cancallforward")
		c.appendValue(self, "callreturn")
