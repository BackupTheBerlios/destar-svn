# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Holger Schurig
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

import language
from configlets import *

class CfgOptUser(CfgOpt):

	shortName = _("DeStar user")
	newObjectTitle = _("New DeStar user")
	groupName = 'Users'
	
	def createVariables(self):
		self.variables = [
		VarType("name",   title=_("Name"), len=15),
		VarType("secret", title=_("Password"), len=15),
		VarType("pc",     title=_("Associated IP address of PC"), hint=_("Trusted for auto-login"), len=15, optional=True),
		VarType("phone",  title=_("Associated phone"), type="choice", optional=True,
		                  options=getChoice("CfgPhone")),
		VarType("pbx",	  title=_("Associated Virtual PBX"), type="choice", optional=True, options=getChoice("CfgOptPBX")),
		VarType("level",  title=_("Type"), type="choice",
		                  options=( ("0",_("disabled")),
		                            ("1",_("User")),
		                            ("2",_("Virtual PBX Administrator")),
		                            ("3",_("Configurator")) )),
		VarType("language", title=_("Language"), type="choice",
				    options=( ("en","en"),
				    	      ("es","es"),
					      ("fr","fr") )),
		     ]
		self.dependencies = [
			DepType("pbx", 
					type="soft",
					message = _("This is a Dependency")),
			DepType("phone", 
					type="soft",
					message = _("This is a Dependency"))]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
		if res:
			return res
		import configlets
		for obj in configlets.configlet_tree:
			if obj==self: 
				continue
			try:
				if self.level == "2" and not self.pbx:
					return ("pbx", _("Please choose a Virtual PBX for this user."))
			except AttributeError:
				pass

	def createAsteriskConfig(self):
		pass

	def row(self):
		return (self.shortName, self.name)
