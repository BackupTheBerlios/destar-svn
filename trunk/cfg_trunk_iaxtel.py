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


class CfgTrunkIaxtel(CfgTrunk):

	shortName   = _("VOIP-Provider Iaxtel")
	newObjectTitle  = _("New VOIP-Provider Iaxtel trunk")

	description = _("""You can register free of charge at
			http://www.iaxtel.com and get an IAXtel number  where
			people can call you. These calls are free of charge, too.'.""")

	

	technology = "IAX2"
	
	def createVariables(self):
		self.variables   = [
		VarType("name",     title=_("Name"), len=15),
		VarType("iaxtelid", title=_("IAXTEL number"),   len=6),
		VarType("iaxtelpw", title=_("IAXTEL password"), len=15),

		VarType("Outbound", title=_("Calls to IAXTEL"), type="label"),
		VarType("ext",      title=_("Extension"), optional=True, len=6),
		VarType("context",  title=_("Context"), default="out-pstn", optional=True, hide=True),
		VarType("callerid", title=_("Caller-Id Name"), optional=True),

		VarType("Inbound",  title=_("Calls from IAXTEL"), type="label"),
		VarType("phone",    title=_("Phone to ring"), optional=True, type="choice",
		                    options=getChoice("CfgPhone"))
		]
		
	def fixup(self):
		CfgTrunk.fixup(self)
		useContext(self.context)
		useContext("in-iaxtel")

	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_iax2")

		c = AstConf("extensions.conf")
		if self.ext:
			needModule("app_setcidname")
			needModule("app_setcidnum")

			ext = "_%s." % self.ext
			c.setSection(self.context)
			if self.callerid:
				c.appendExten(ext, "CALLERID(%s)" % self.callerid)
			c.appendExten(ext, "CALLERID(%s)" % self.iaxtelid)
			c.appendExten(ext, "Dial(IAX2/%s:%s@iaxtel.com/${EXTEN:%d@iaxtel},60,r)" % (self.iaxtelid, self.iaxtelpw, len(self.ext)))
			#c.appendExten(ext, "Busy")

		c = AstConf("iax.conf")
		c.setSection("general")
		c.append("register=%s:%s@iaxtel.com" % (self.iaxtelid, self.iaxtelpw))

		if not c.hasSection("iaxtel"):
			c.setSection("iaxtel")
			c.setSection("iaxtel")
			c.append("type=user")
			# TODO?
			c.append("context=in-iaxtel")
			c.append("auth=rsa")
			c.append("inkeys=iaxtel")

		if self.phone:
			c = AstConf("extensions.conf")
			c.setSection("in-iaxtel")
			# TODO: don't hardcode the "SIP/" here:
			c.appendExten(self.iaxtelid, "Macro(exten-std,SIP/%s)" % self.phone)
