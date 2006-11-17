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


class CfgTrunkZapHFC(CfgTrunk):

	shortName = _("ISDN using zaphfc")
	newObjectTitle = _("New ISDN using zaphfc trunk")
	
	def createVariables(self):
		self.variables = [
			VarType("name",  title=_("Name"), len=35),
			VarType("mode",  title=_("Mode of NTBA"), type="choice",
							 options=("p2p","p2mp"), default="p2mp"),
			VarType("cards", title=_("Number of cards"), type="int", default=1, len=2),
	
			VarType("Outbound",  title=_("Calls to the ISDN network"), type="label"),
			VarType("msn",   title=_("Subscriber number"), len=15),
			VarType("ext",   title=_("Outgoing prefix"), optional=True, len=6),
			]


	def fixup(self):
		CfgTrunk.fixup(self)


	def createAsteriskConfig(self):
		needModule("chan_zap")

		# Create config for the zaphfc kernel module:
		c = AstConf("zaptel.conf")
		c.destar_comment = False
		c.setSection("")
		c.append("loadzone=nl")
		c.append("defaultzone=nl")
		for n in range(self.cards):
			c.append("span=%d,1,3,ccs,ami" % (n+1))
		for n in range(self.cards):
			c.append("bchan=%d-%d" % (n*3+1,n*3+2))
			c.append("dchan=%d" % (n*3+3))


		# Create config for chan_zap:
		c = AstConf("zapata.conf")
		c.append("switchtype=euroisdn")
		if self.mode=="p2p":
			c.append("signalling=bri_cpe")
			prefix=self.msn
		else:
			c.append("signalling=bri_net_ptmp")
			prefix = ""
		c.append("group=1")
		# TODO?
		c.append("context=in-pstn")
		c.append("channel=1-2")

		# Write DID extensions
		if self.mode=="p2p":
			# For every phone, we need a separate DID config entry, we create them
			# in the [in-pstn] context.
			c = AstConf("extensions.conf")
			c.setSection("in-pstn")
			for p in configlet_tree:
				if not isinstance(p, Phone): continue
				if not p.did: continue
				#c.appendExten("%s%s" % (self.msn,p.ext), "Macro(exten-std,SIP/%s)" % p.name)

		# Write dialout entry:
		if self.ext:
			c = AstConf("extensions.conf")
			c.setSection("default")
			c.appendExten("_%s." % self.ext, "Dial(Zap/g1/${EXTEN:%d},60)" % (len(self.ext)))
