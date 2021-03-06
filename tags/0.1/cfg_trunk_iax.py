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
		VarType("name",      title=_("Name"), len=25, default="iaxtrunk"),
		VarType("host",      title=_("IAX host"), len=80),
		VarType("bandwidth",  title=_("Bandwith"), type="choice", len=25,
				options=[('low',_("Low")),('high', _("High"))]
			),
		
		VarType("authLabel",   title=_("Authentication"), type="label"),
		VarType("auth",      title=_("Authentication Method"), type="radio", default="plain",
		                               options=[('plain',_("Plain text")),('rsa',_("RSA")),('md5',_("MD5"))]),
		VarType("pw",    title=_("Password"), hint=_("For 'Plain' or 'MD5' only"), len=80, optional=True),
		VarType("inkeys",    title=_("Public key from remote server"), hint=_("For 'RSA' only"), len=80, optional=True),
		VarType("outkey",    title=_("Private local key"), hint=_("For 'RSA' only"), len=80, optional=True),

                VarType("trunk",      title=_("Enable trunking?"), type="bool", hide=True),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True, optional=True),

		VarType("Inbound",    title=_("Calls from IAX trunk"), type="label"),
		VarType("contextin",      title=_("Go to"), type="radio", default='phone',
		                               options=[('phone',_("Phone")),('ivr',_("IVR"))]),
		VarType("phone",      title=_("Extension to ring"), type="choice", optional=True,
		                               options=getChoice("CfgPhone")),
		VarType("ivr",      title=_("IVR to jump to"), type="choice", optional=True,
		                               options=getChoice("CfgIVR")),
		VarType("dial", hide=True, len=50),
		]

	technology = "IAX2"
	
	def fixup(self):
		CfgTrunk.fixup(self)
		
        def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res

       	def createAsteriskConfig(self):
		#Dial part to use on dialout macro
		self.dial = "IAX2/%s/${ARG1}" % self.name
		#What to do with incoming calls
		self.createIncomingContext()
		
		c = AstConf("iax.conf")
		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("host=%s" % self.host)
			c.append("username=%s" % self.name)
			c.append("context=in-%s" % self.name)
			c.append("bandwidth=%s" % self.bandwidth)
			c.append("qualify=yes")
			if self.trunk:
				c.append("trunk=yes")
			if self.auth == "rsa" and self.inkeys and self.outkey:		
				c.append("auth=rsa")
				c.append("inkeys=%s" % self.inkeys)
				c.append("outkey=%s" % self.outkey)
			elif self.auth == "md5":
				c.append("auth=md5")
				c.append("secret= %s" % self.pw)
			elif self.auth == "plain":
				c.append("secret= %s" % self.pw)

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
