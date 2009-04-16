# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2007 by Holger Schurig
# This file has Copyright (C) 2007 by Santiago Ruano Rincón
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


class CfgOptOQueuesAgents(CfgOptSingle):

	shortName = _("Queues and Agents")
	newObjectTitle= _("Queues and Agents")
	description = _("General settings for Queues and Agents")
	groupName = 'Options'
	 
	def createVariables(self):
		self.variables = [
			VarType("labelqueues",
				title=_("Queues settings"),
				type="label"),

			VarType("persistentmembers",
				title=_("Queues persistent members:"),
				type="bool",
				default=True,
				optional=True),

			VarType("labelagents",
				title=_("Agents settings"),
				type="label"),

			VarType("persistentagents",
				title=_("Persistent agents:"),
				type="bool",
				default=True,
				optional=True),

			]

	def createAsteriskConfig(self):
		c = AstConf("queues.conf")
                c.setSection("general")
		if self.persistentmembers:
			c.append("persistentmembers = yes")	
		else:
			c.append("persistentmembers = no")	

		c = AstConf("agents.conf")
                c.setSection("general")
		if self.persistentagents:
			c.append("persistentagents = yes")	
		else:
			c.append("persistentagents = no")	

