# -*- coding: utf-8 -*-
#
# This module is Copyright (C) 2005 by Francesco Crescioli,
# Heavly based on module cfg_opt_sip_audio Copyright (C) 2005 by Alejandro Rios,
# Destar is Copyright (C) 2005 by Holger Schurig,
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


class CfgOptSipNetwork(CfgOptSingle):

	shortName = _("SIP Options")
	newObjectTitle = _("SIP Options")
	
	def createVariables(self):
		self.variables = [
			VarType("doBind",	
					title=_("Bind specific address?"), 
					type="bool"),

			VarType("bindaddr",	
					title=_("Bind address"), 
					len=25,
					optional=True),

			VarType("globalnat",
					title=_("Global NAT"),
					type="choice",
					options=( ("no",_("No")),
						  ("yes",_("Yes")),
						  ("always",_("Always")), 
						  ("route",_("Route")) ), 
					default="no"),

			# Hell, what a mess in Asterisk and Snom FW >6.2.2, pedantic is needed to get "#" working
			VarType("pedantic",	
					title=_("SIP Pedantic checking of Call-ID"),	
					type="bool",
					optional=True),

			VarType("extintnet",	
					title=_("External/Internal IP"), 
					type="label"),

			VarType("setExt",	
					title=_("Force external ip/internel network?"),	
					type="bool"),

			VarType("extip",	
					title=_("External ip"), 
					len=25,
					optional=True),

			VarType("intnet",	
					title=_("Internal network"), 
					len=25,
					optional=True),

			VarType("intnetmask",	
					title=_("Netmask"), 
					len=25,
					optional=True),

			VarType("tos",
					title=_("TOS Field"),
					len=10,
					optional=True,
					default="184"),

			VarType("srvlookup",
					title=_("Enable DNS SRV lookups on outbound calls"),
					type="bool",
					default=True,
					optional=True),

			VarType("other",
					title=_("Other options"), 
					type="label"),

			VarType("moh",
                                        title=_("Music on hold"),
                                        type="choice",
                                        optional = True,
                                        options=getChoice("CfgOptMusic")),
		]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
                if res:
                        return res

	def isAddable(self):
		"""We can only add this configlet if we have at least one
		SIP phone/trunk defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ in ('CfgPhoneSip','CfgTrunkSip'):
				return CfgOptSingle.isAddable(self)
		return False
	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("sip.conf")
		c.setSection("general")
		if self.doBind:
			c.append("bindaddr=%s" % self.bindaddr)
		if self.setExt:
			if self.extip:
				c.append("externip=%s" % self.extip)
			if self.intnet:
				c.append("localnet=%s/%s" % (self.intnet,self.intnetmask))
		if self.tos:
			c.append("tos=%s" % self.tos)
		if self.moh:
			c.append("musiconhold=%s" % self.moh)
     		if self.pedantic:
             		c.append("pedantic=yes")
		c.append("nat=%s" % self.globalnat)
		if self.srvlookup:
			c.append("srvlookup=yes")
