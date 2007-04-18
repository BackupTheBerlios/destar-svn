# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Holger Schurig,
# this module was written by Diego Andrés Asenjo.
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

class CfgAgent(CfgPhone):

	shortName = _("Agent")
	newObjectTitle = _("New agent")
	description = _("This is a queue agent")
	technology = "AGENT"
	groupName = "Agents"
	
	def createVariables(self):
		self.variables = [
			VarType("pbx",    
				title=_("Virtual PBX"), 
				type="choice", 
				options=getChoice("CfgOptPBX")),

			VarType("name",
				title=_("Name"),
				len=15),

			VarType("number",
					title=_("Agent number"),
					type="int",
					len=15),

			VarType("secret",
					title=_("Password"),
					type="int",
					len=15),
					
			VarType("QueueLab",
					title=_("Call Queues"),
					type="label",
					hide=True),
			
			VarType("queues",
					title=_("Agent of queues:"),
					type="mchoice",
					optional=True,
					options=getChoice("CfgPhoneQueue"),
					hide=True)]
					
		queues = len(configlet_tree.getConfigletsByName('CfgPhoneQueue'))
		if queues > 0:
			for v in self.variables:
				if v.name == "QueueLab" or v.name == "queues":
					v.hide = False

		self.dependencies = [
			DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
		]

	def createAsteriskConfig(self):

		ag = AstConf("agents.conf")
		ag.setSection("agents")
		ag.append("agent=%d,%d,%s" % (self.number, self.secret, self.name))

		self.createQueuesConfig()
