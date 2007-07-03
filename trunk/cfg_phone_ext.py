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


from configlets import *


class CfgPhoneExtension(CfgPhone):

	shortName = _("Extension")
	newObjectTitle = _("New extension")
	description = _("Set an 'alias' extension to a phone")
	technology = "virtual"
	
	def createVariables(self):
		self.variables = [
			VarType("pbx",    
				title=_("Virtual PBX"), 
				type="choice", 
				options=getChoice("CfgOptPBX")),

			VarType("name",
					title=_("Name"),
					len=15),
	
			VarType("ext",
					title=_("Extension"),
					hint=_("This can be used to set operator(o) or fax(fax) extensions."),
					len=6),
	
			VarType("Outbound",
					title=_("Calls to the extension"),
					type="label"),

			VarType("phone",
					title=_("Real phone to ring"),
					type="choice",
					options=getChoice("CfgPhone")),

			VarType("Voicemail",
					title=_("Voicemail settings"),
					type="label",
					len=6),
					
			VarType("pin",
					title=_("Voicemail PIN"),
					type="int",
					optional=True,
					len=6),
			
			VarType("email",
					title=_("Voicemail email"),
					optional=True,
					len=60)
			]	

		self.dependencies = [
			DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
		]


	def isAddable(self):
		"We can only add this object if we have at least one other phone defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		if len(configlets.configlet_tree.getConfigletsByName('CfgOptPBX')) > 0:
			for obj in configlets.configlet_tree:
				if obj.groupName == 'Phones':
					return True
		return False
	isAddable = classmethod(isAddable)


	def row(self):
		return (self.shortName, self.ext, "%s -> %s" % (self.name, self.phone))


	def createAsteriskConfig(self):
		extensions = AstConf("extensions.conf")
		extensions.setSection(self.pbx)
		extensions.appendExten(self.ext,"Set(CDR(pbx)=%s,CDR(userfield)=%s,CALLERID(num)=${CALLERIDNUM}-%s)" % (self.pbx,self.name,self.ext))
		self.createDialEntry(extensions, self.ext, self.pbx, self.ext)
		extensions.appendExten(self.name,"Set(CDR(pbx)=%s,CDR(userfield)=%s,CALLERID(num)=${CALLERIDNUM}-%s)" % (self.pbx,self.name,self.ext))
		self.createDialEntry(extensions, self.name, self.pbx, self.ext)
		self.usemwi = False
		self.createVoicemailConfig(extensions)

	def createDialEntry(self, extensions, exten, pbx, ext):
		import configlets
		obj = configlets.configlet_tree.getConfigletByName(self.phone)
		ret = extensions.appendExten(exten, "Macro(dial-std-exten,%s/%s,out-%s,%s,%s)" % (
			obj.technology,
			self.phone,
			self.phone,
			ext,
			pbx
			))


