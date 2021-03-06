# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Michael Bielicki
# Copyright (C) 2006 Manuel Cerón <ceronman@gmail.com>
# based on Free World Dialup Module by Hoger Schurig
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA	02111-1307	USA


from configlets import *


class CfgOptDID(CfgOpt):

	shortName	= _("Direct inward dialing (DID) number")
	newObjectTitle	= _("New direct inward dialing (DID) number")
	description = _(""" Used to route a DID to an extension 
						or Auto-Attendant.""")
	groupName = 'DIDs'


	def createVariables(self):
		self.variables	= [
			VarType("did", 
					title = _("DID"),
					len = 15),

			VarType("trunk",
					title = _("From Trunk:"),
					type = "choice",
					options = getChoice("CfgTrunk")),

			VarType("contextin",
					title = _("Go to"),
					type = "radio",
					default = 'phone',
					options = [('phone', _("Phone")), ('ivr', _("IVR")), ("custommap", _("Custom map"))]),

			VarType("phone",
					title = _("Phone to ring"),
					optional = True,
					type ="choice",
					options = getChoice("CfgPhone")),

			VarType("ivr",
					title = _("IVR to jump to"),
					optional = True,
					type = "choice", 
					options = getChoice("CfgIVR")),

			VarType("custommappbx",
                                        title=_("Custom map, PBX"),
                                        type="choice",
                                        optional = True,
                                        options=getChoice("CfgOptPBX")),

    			VarType("custommapdest",
                                        title = _("Custom map, destination"),
                                        len = 30,
                                        optional = True),

			VarType("callerid",
					title=_("CallerID:"),
					type="label"),

			VarType("clid",
					title = _("Change Caller*Id Name to:"),
					len = 25,
					optional = True),

			VarType("clidnum",
					title = _("Change Caller*Id Number to:"),
					len = 25,
					optional = True),
					]
					
		self.dependencies = [
			DepType("trunk", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("phone", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("ivr", 
					type="hard",
					message = _("This is a Dependency"))]

	def isAddable(self):
		import configlets
		return len(configlets.configlet_tree['Trunks']) > 0
	isAddable = classmethod(isAddable)

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
		if res:
			return res
		import configlets
		for obj in configlets.configlet_tree:
			if obj==self: 
				continue
			try:
				if obj.did == self.did and obj.trunk == self.trunk:
					return ("did", _("DID already in use for that trunk."))
			except AttributeError:
				pass

	def row(self):
		return (self.shortName, "%s -> %s" % (self.trunk, self.did))

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection("in-%s" % self.trunk)
		c.appendExten(self.did,"Set(CDR(intrunk)=%s)" %  self.trunk)
		if self.clid:
			needModule("func_callerid")
			c.appendExten(self.did,"Set(CALLERID(name)=%s)" %  self.clid)
		if self.clidnum:
			needModule("func_callerid")
			c.appendExten(self.did,"Set(CALLERID(number)=%s)" %  self.clidnum)
		if self.contextin == 'phone' and self.phone:
			import configlets
			obj = configlets.configlet_tree.getConfigletByName(self.phone)
			try:
				c.appendExten(self.did,"Goto(%s,%s,1)" %  (obj.pbx,self.phone))
			except AttributeError:
				pass
		elif self.contextin == 'ivr' and self.ivr:
			c.appendExten(self.did,"Goto(%s,s,1)" % self.ivr)
        	elif self.contextin == 'custommap' and self.custommapdest:
        		c.appendExten(self.did,"Goto(%s,%s,1)" % (self.custommappbx, self.custommapdest))
