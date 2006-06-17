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


class CfgTrunkFwdIax(CfgTrunk):

	shortName   = _("VOIP-Provider FreeworldDialup (IAX)")
	newObjectTitle   = _("New VOIP-Provider FreeworldDialup (IAX) trunk")

	description = _("""You can register free of charge at
			http://freeworlddialup.com and get an FWD Id where
			people can call you. These calls are is free of charge, too.

			When you've an account, you must enable FWD's IAX support at
			http://www.freeworlddialup.com/advanced/iax to use this
			this 'phone line'.""")
	technology = "IAX2"
	
	def createVariables(self):
		self.variables   = [
			VarType("name",     title=_("Name"), len=15, default="fwdiax"),
			VarType("fwdid",    title=_("FWD number"),   len=6),
			VarType("fwdpw",    title=_("FWD password"), len=15),
	
			VarType("Outbound", title=_("Calls to FWD"), type="label"),
			VarType("ext",      title=_("Extension"), optional=True, len=6),
			VarType("context",  title=_("Context"), default="default", optional=True, hide=True),
			VarType("callerid", title=_("Caller-Id Name"), optional=True),
	
			VarType("Inbound",  title=_("Calls from FWD"), type="label"),
			VarType("phone",    title=_("Phone to ring"), optional=True, type="choice",
								options=getChoice("CfgPhone"))
		]
		
	def fixup(self):
		CfgTrunk.fixup(self)
		useContext(self.context)
		useContext("in-iaxfwd")

	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_iax2")

		c = AstConf("extensions.conf")
		if self.ext:
			needModule("func_callerid")

			ext = "_%s." % self.ext
			c.setSection(self.context)
			if self.callerid:
				c.appendExten(ext, "CALLERID(%s)" % self.callerid)
			else: 
				c.appendExten(ext, "CALLERID(%s)" % self.fwdid)
			c.appendExten(ext, "Dial(IAX2/%s:%s@iax2.fwdnet.net/${EXTEN:%d},60,r)" % (self.fwdid, self.fwdpw, len(self.ext)))
			#c.appendExten(ext, "Busy")

		c = AstConf("iax.conf")
		c.setSection("general")
		c.append("register=%s:%s@iax.fwdnet.net" % (self.fwdid, self.fwdpw))

		if not c.hasSection("iaxfwd"):
			c.setSection("iaxfwd")
			c.append("type=user")
			# TODO?
			c.append("context=in-iaxfwd")
			c.append("auth=rsa")
			c.append("inkeys=freeworlddialup")

		if self.phone:
			c = AstConf("extensions.conf")
			c.setSection("in-iaxfwd")
			c.appendExten(self.fwdid, "Goto(phones,%s,1)" % self.phone)
