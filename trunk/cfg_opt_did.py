# -*- coding: iso-latin-1 -*-
# Copyright (C) 2004 Michael Bielicki
# based on Free World Dialup Module by Hoger Schurig
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


class CfgOptDID(CfgOpt):

	shortName   = _("Direct inward dialing (DID) number")
	newObjectTitle  = _("New direct inward dialing (DID) number")

	description = _("""Used to route a DID to an extension or Auto-Attendant.""")

	variables	= [
		VarType("did",       title=_("DID"), len=15),
		VarType("trunk",     title=_("From Trunk:"), type="choice",
		                     options=getChoice("CfgTrunk")),
		VarType("contextin",      title=_("Go to"), type="radio", default='phone',
		                               options=[('phone',_("Phone")),('ivr',_("IVR"))]),
		VarType("phone",     title=_("Phone to ring"), optional=True, type="choice",
		                     options=getChoice("CfgPhone")),
		VarType("ivr",     title=_("IVR to jump to"), optional=True, type="choice",
		                     options=getChoice("CfgIVR")),
		VarType("clid",       title=_("Change Caller*Id to:"), len=25, optional=True),
		]
	
	def isAddable(self):
		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.groupName == 'Trunks':
				return True
		return False
	isAddable = classmethod(isAddable)

        def checkConfig(self):
                res = CfgOpt.checkConfig(self)
                if res:
                        return res
		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
				if obj==self: continue
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
		if self.clid:
			needModule("app_setcidname")
			c.appendExten(self.did,"SetCIDName(%s)" %  self.clid)
		if self.contextin == 'phone' and self.phone:
			c.appendExten(self.did,"Goto(phones,%s,1)" %  self.phone)
		elif self.contextin == 'ivr' and self.ivr:
			c.appendExten(self.did,"Goto(%s,s,1)" % self.ivr)
