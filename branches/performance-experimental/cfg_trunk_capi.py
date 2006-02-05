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


# fcpci: http://www.avm.de/ftp/cardware/fritzcrd.pci/linux/suse.82/index.html
# chan_capi: http://www.junghanns.net

class CfgTrunkCapi(CfgTrunk):

	shortName = _("ISDN using CAPI, outgoing")
	newObjectTitle = _("New outgoing ISDN using CAPI")
	variables = [
		VarType("name",      title=_("Name"), len=15),

		VarType("Outbound",  title=_("Calls to the ISDN network"), type="label"),
		VarType("msn",       title=_("Subscriber number"), len=15),
		VarType("ext",       title=_("Outgoing prefix"), optional=True, len=6),
		]

	technology = "CAPI"


	def channel(self):
		return "%s[contr1/%s]" % (self.technology, self.msn)


	# def fixup(self):
		# CfgTrunk.fixup(self)
		# useContext("in-capi")


	def createAsteriskConfig(self):
		needModule("chan_capi")

		# Create config for chan_capi:
		c = AstConf("capi.conf")
		if not c.hasSection("general"):
			c.append("nationalprefix=0")
			c.append("internationalprefix=00")
			c.append("rxgain=0.8")
			c.append("txgain=0.8")
		c.setSection("interfaces")
		c.appendValue(self, "msn")
		c.append("context=in-capi")

		msn_arr = []
		# BUG: it does somehow not work to simply write 'for msn in config_entries',
                # despite the "from configlets import *" above
		import configlets
		for msn in configlets.configlet_tree:
			if msn.__class__.__name__ != "CfgTrunkCapiMSN": continue
			msn_arr.append(msn.msn)
		if msn_arr:
			c.append("incomingmsn=%s" % ",".join(msn_arr) )
		c.append("controller=1")
		c.append("softdtmf=1")
		c.append("devices=2")

		# Write dialout entry:
		if self.ext:
			c = AstConf("extensions.conf")
			c.setSection("default")
			c.appendExten("_%s." % self.ext, "Dial(CAPI/%s:b${EXTEN:%d},90,T)" % (self.msn, len(self.ext)))
