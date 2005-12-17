# -*- coding: iso-latin-1 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2005 by Alejandro Rios
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

import panelutils
from configlets import *


class CfgOptOPPanel(CfgOptSingle):

	shortName = _("Operator Panel")
	newObjectTitle= _("Operator Panel")
	description = _("Configure Asternic Flash Operator Panel")
	groupName = 'Options'
	
	variables = [
		VarType("name", title=_("Name"), len=15, default="oppanel"),
		VarType("web_hostname", title=_("FQDN/IP to access the panel via web"), len=15, optional=True),
		VarType("security_code", title=_("Security Code"), len=15, default=generatePassword(8)),
		VarType("manager", title=_("Manager agent"), type="choice",
		                  options=getChoice("CfgOptManager")),
		VarType("poll_interval", title=_("Frequency in seconds to poll for sip and iax status"), len=10, default="60"),
		     ]

	def createAsteriskConfig(self):
		c = AstConf("op_server.cfg")
                c.setSection("general")
		if self.web_hostname:
			c.appendValue(self, "web_hostname")	
		c.appendValue(self, "security_code")	
		c.appendValue(self, "poll_interval")	
		panelutils.createManagerConfig(self)
		panelutils.createDefaultConfig(c)	

	def row(self):
		return (self.shortName, self.name)
