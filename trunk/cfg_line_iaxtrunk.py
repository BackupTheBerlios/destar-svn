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


class CfgLineIaxtrunk(CfgLine):

	shortName   = _("IAX Trunk")

	description = _("""Used to setup an IAX trunk to another Asterisk server or an IAX termination.""")

	variables	= [
		VarType("name",       title=_("Name"), len=15, default="iaxtrunk"),
		VarType("id",         title=_("IAX username"),   len=6),
		VarType("pw",         title=_("IAX password"), len=15),
		VarType("host",       title=_("IAX host"), len=25),

		VarType("Outbound",   title=_("Calls to IAX trunk"), type="label"),
		VarType("ext",        title=_("Extension"), optional=True, len=6),
		VarType("context",    title=_("Context"), default="out-pstn", optional=True, hide=True),
		VarType("callerid",   title=_("Caller-Id Name"), optional=True),

		VarType("Inbound",    title=_("Calls from IAX trunk"), type="label"),
		VarType("extin",      title=_("Extension to ring"), optional=True, len=4),
		VarType("contextin",  title=_("Context"), optional=True, hide=True, default="in-pstn")
		]

	technology = "IAX2"


	def fixup(self):
		CfgLine.fixup(self)
		useContext(self.context)
		useContext("in-iaxtrunk")


	def createAsteriskConfiglet(self):
		needModule("res_crypto")
		needModule("chan_iax2")

		c = AstConf("extensions.conf")
		if self.ext:
			needModule("app_setcidname")
			needModule("app_setcidnum")
			ext = "_%s." % self.ext
			c.setSection(self.context)
			if self.callerid:
				c.appendExten(ext, "SetCIDName(%s)" % self.callerid)
			c.appendExten(ext, "SetCIDNum(%s)" % self.id)
			c.appendExten(ext, "Dial(IAX2/%s:%s@%s/${EXTEN:%d},60,r)" % (self.id, self.pw, self.host, len(self.ext)))
			#c.appendExten(ext, "Busy")
		if self.extin and self.contextin:
			c.setSection(self.contextin)
			c.appendExten("s", "Goto(default,%s,1)" % self.extin)

		c = AstConf("iax.conf")
		c.setSection("general")
		c.append("register=%s:%s@%s" % (self.id, self.pw, self.host))

		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("context=in-iaxtrunk")
			c.append("auth=md5")
			c.append("host=%s" % self.host)
			c.append("secret= %s" % self.pw)
