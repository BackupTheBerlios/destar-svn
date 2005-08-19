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

		VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True),

		VarType("Inbound",    title=_("Calls from IAX trunk"), type="label"),
		VarType("contextin",      title=_("Go to"), type="radio", hide=True, default='phone',
		                               options=[('phone',_("Phone")),('autoatt',_("Auto_Attendant"))]),
		VarType("phone",      title=_("Extension to ring"), type="choice", optional=False,
		                               options=getChoice("CfgPhone")),
		VarType("dial", hide=True, len=50),
		]

	technology = "IAX2"

        def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res
		if self.contextin == 'phone' and not self.phone:
			return ('phone',_("You should select a phone to ring to"))

	def fixup(self):
		CfgTrunk.fixup(self)
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False
		import configlets
		autoatts=False
		for obj in configlets.config_entries:
			if obj.__class__.__name__ == 'CfgOptAutoatt':
				autoatts=True
				alreadyappended = False
				for v in self.variables:	
					if v.name == "autoatt_"+obj.name:
						alreadyappended = True
				if not alreadyappended:
					self.variables.append(VarType("autoatt_%s" % obj.name, title=_("%s") % obj.name, type="bool", optional=True,render_br=False))
					self.variables.append(VarType("autoatt_%s_time" % obj.name, title=_("Time"), hint=_("00:00-23:59|mon-sun|1-31|jan-dic"), len=50, optional=True))
		if autoatts:
			for v in self.variables:
				if v.name == "contextin":
					v.hide = False
				if v.name == "phone":
					v.optional = True

	def createAsteriskConfig(self):
		needModule("res_crypto")
		needModule("chan_iax2")
		#Dial part to use on dialout macro
		self.dial = "IAX2/%s:%s@%s/${ARG1}" % (self.id, self.pw, self.host)
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

		c = AstConf("iax.conf")
		c.setSection("general")
		c.append("register=%s:%s@%s" % (self.id, self.pw, self.host))
		if not c.hasSection(self.name):
			c.setSection(self.name)
			c.append("type=friend")
			c.append("context=%s" % contextin)
			c.append("auth=md5")
			c.append("host=%s" % self.host)
			c.append("secret= %s" % self.pw)
		
		if panelutils.isConfigured() == 1 and self.panel:
			panelutils.createTrunkButton(self)
