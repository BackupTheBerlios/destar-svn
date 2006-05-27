# -*- coding: iso-latin-1 -*-
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
					options=getChoice("CfgPhone")),]

		if varlist_manager.hasDialouts():
			self.variables += varlist_manager.getDialouts()
			for v in self.variables:
				if v.name == "Dialout" or v.name=="timeout":
					v.hide = False
					
		queues = len(configlet_tree.getConfigletsByName('CfgPhoneQueue'))
		if queues > 0:
			for v in self.variables:
				if v.name == "QueueLab" or v.name == "queues":
					v.hide = False

	def createDependencies(self):
		for dep in self.dependencies:
			if self.__dict__.has_key(dep.name):
				obj_name = dep.name[8:] # get the name after "dialout_"
				import configlets
				obj = configlets.configlet_tree.getConfigletByName(obj_name)
				if obj is None:
					return
				dependent_obj = DependentObject(self, dep)
				obj.dependent_objs.append(dependent_obj)


	def isAddable(self):
		"We can only add this object if we have at least one other phone defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.groupName == 'Phones':
				return True
		return False
	isAddable = classmethod(isAddable)


	def row(self):
		return (self.shortName, self.ext, "%s -> %s" % (self.name, self.phone))


	def createAsteriskConfig(self):
		ext = AstConf("extensions.conf")
		ext.setSection("phones")
		ext.appendExten(self.ext, "Goto(%s)" % self.phone)
