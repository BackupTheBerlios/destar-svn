# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2007 by Ian Sper 
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

class CfgAppDisa(CfgApp):

	shortName   = _("Disa extension")
	description = _("Direct Inward System Access")
	newObjectTitle = _("New Disa extension") 
	def createVariables(self):	
		self.variables   = [
			VarType("pbx",
				title=_("Virtual PBX"),
				type="choice",
				options=getChoice("CfgOptPBX")),

			VarType("name",
				title=_("Name"),
				len=20),

			VarType("pin",
				title=_("Password"),
				len=20),

			VarType("ext",
				title=_("Extension"),
				len=6,
				default="*171"),

			VarType("Dialout",
				title=_("Allowed dialout-entries"),
				type="label",
				hide=True),

			VarType("timeout",
				title=_("Enable time restriction?"),
				type="bool",
				optional=True,
				hide=True),]
		if varlist_manager.hasDialouts():
                        self.variables += varlist_manager.getDialouts()
                        for v in self.variables:
                                if v.name == "Dialout" or v.name=="timeout":
                                        v.hide = False
	
	
	def row(self):
		return ("%s" % (self.ext),self.shortName)

	def checkConfig(self):
                import configlets
                for o in configlets.configlet_tree:
                        if o==self: continue
                        try:
                                if o.ext == self.ext:
                                        return ("ext", _("Extension already in use"))
                        except AttributeError:
                                pass
	

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection("%s" % self.pbx)
		needModule("app_disa")	
		c.appendExten("%s" % self.ext ,"Set(TIMEOUT(digit)=5)")
		c.appendExten("%s" % self.ext ,"Set(TIMEOUT(response)=10)")
		c.appendExten("%s" % self.ext ,"Authenticate(%s)" % self.pin)
		c.appendExten("%s" % self.ext ,"DISA(no-password|out-%s)" % self.name)
