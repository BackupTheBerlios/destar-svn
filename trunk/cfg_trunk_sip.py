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


class CfgTrunkSiptrunk(CfgTrunk):

	shortName   = _("Standard SIP Trunk")

	description = _("""Used to setup a SIP trunk to a SIP provider or a different SIP server.""")

	variables   = [
		VarType("name",       title=_("Name"), len=15, default="siptrunk"),
		VarType("id",         title=_("SIP username"),   len=15),
		VarType("pw",         title=_("SIP password"), len=15),
		VarType("host",       title=_("SIP host"), len=25),
		VarType("forward",      title=_("Enable forward address type?"), type="bool"),
		VarType("nat",      title=_("Is the trunk behind NAT?"), type="bool"),

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True),

		VarType("Inbound",    title=_("Calls from SIP trunk"), type="label"),
		VarType("contextin",      title=_("Go to"), type="radio", hide=True, default='phone',
		                               options=[('phone',_("Phone")),('autoatt',_("Auto_Attendant"))]),
		VarType("phone",      title=_("Extension to ring"), type="choice", optional=False,
		                               options=getChoice("CfgPhone")),
		VarType("dial", hide=True, len=50),
		]

	technology = "SIP"


	def fixup(self):
		CfgTrunk.fixup(self)
		
        def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res
                
	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_sip")

		#Dial part to use on dialout macro
		self.dial = "SIP/${ARG1}@%s" % (self.host)
		if self.forward:
			self.dial += "/{$ARG1}" 
		
		#What to do with incoming calls
		c = AstConf("extensions.conf")
		contextin = "in-%s" % self.name
		c.setSection(contextin)
		if self.contextin == 'phone' and self.phone:
			c.appendExten("s", "Goto(phones,%s,1)" % self.phone)
		elif self.contextin == 'autoatt':
			import configlets
			for obj in configlets.config_entries:
				if obj.__class__.__name__ == 'CfgOptAutoatt':
					try:
						autoatt = self.__getitem__("autoatt_%s" % obj.name)
						if autoatt:
							time = self.__getitem__("autoatt_%s_time" % obj.name)
							if time:
								c.append("include=>%s|%s" % (obj.name,time))
							else:
								c.append("include=>%s" % obj.name)
					except KeyError:
						pass

		c = AstConf("sip.conf")
		c.setSection("general")
		c.append("register=%s:%s@%s" % (self.id, self.pw, self.host))

		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("username=%s" % self.id)
			c.append("secret=%s" % self.pw)
			c.append("host=%s" % self.host)
			c.append("context=%s" % contextin)
			c.append("auth=md5")
			c.append("canreinvite=no")
			if self.nat:
				c.append("nat=yes")

		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
