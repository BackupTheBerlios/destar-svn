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
import panelutils


class CfgTrunkIaxtrunk(CfgTrunk):

	shortName   = _("Standard IAX Trunk")

	description = _("""Used to setup an IAX trunk to another Asterisk server or an IAX termination.""")

	variables	= [
		VarType("name",       title=_("Name"), len=15, default="iaxtrunk"),
		VarType("id",         title=_("IAX username"),   len=6),
		VarType("pw",         title=_("IAX password"), len=15),
		VarType("host",       title=_("IAX host"), len=25),

		VarType("Outbound",   title=_("Calls to IAX trunk"), type="label"),
		VarType("ext",        title=_("Outgoing Prefix"), optional=True, len=6),
		VarType("callerid",   title=_("Caller-Id Name"), optional=True),

		VarType("Inbound",    title=_("Calls from IAX trunk"), type="label"),
		VarType("phone",      title=_("Extension to ring"), type="choice",
		                               options=getChoice("CfgPhone")),
		
		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True),
		]

	technology = "IAX2"

        def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res

	def fixup(self):
		CfgTrunk.fixup(self)
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False


	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_iax2")

		c = AstConf("extensions.conf")
		if self.ext:
			needModule("app_setcidname")
			needModule("app_setcidnum")
			ext = "_%s." % self.ext
			context = "out-%s" % self.name
			c.setSection(context)
			if self.callerid:
				c.appendExten(ext, "SetCIDName(%s)" % self.callerid)
			c.appendExten(ext, "SetCIDNum(%s)" % self.id)
			c.appendExten(ext, "Dial(IAX2/%s:%s@%s/${EXTEN:%d},60,r)" % (self.id, self.pw, self.host, len(self.ext)))
			#c.appendExten(ext, "Busy")
		if self.phone:
			contextin = "in-%s" % self.name
			c.setSection(contextin)
			c.appendExten("s", "Goto(phones,%s,1)" % self.phone)
		c = AstConf("iax.conf")
		c.setSection("general")
		c.append("register=%s:%s@%s" % (self.id, self.pw, self.host))

		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			contextin = "in-%s" % self.name
			c.append("context=%s" % contextin)
			c.append("auth=md5")
			c.append("host=%s" % self.host)
			c.append("secret= %s" % self.pw)
		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
