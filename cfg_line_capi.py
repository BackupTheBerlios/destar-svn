# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig
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
from language import _

# fcpci: http://www.avm.de/ftp/cardware/fritzcrd.pci/linux/suse.82/index.html
# chan_capi: http://www.junghanns.net

class CfgLineCapi(CfgLine):

	shortName = _("ISDN using CAPI")
	variables = [VarType("name",  title=_("Name"), len=15),
		     VarType("msn",   title=_("Subscriber number"), len=15),

		     VarType("Inbound",	  title=_("Calls from the ISDN network"), type="label"),
		     VarType("extin",     title=_("Extension to ring"), optional=True, len=6),
		     VarType("contextin", title=_("Context"), optional=True, hide=True, default="in-pstn"),

		     VarType("Outbound",  title=_("Calls to the ISDN network"), type="label"),
		     VarType("ext",       title=_("Extension"), optional=True, len=6),
		     VarType("context",   title=_("Context"),   optional=True, hide=True, default="out-pstn")]

	technology = "CAPI"


	def channel(self):
		return "%s[contr1/%s]" % (self.technology, self.msn)


	def fixup(self):
		CfgLine.fixup(self)
		useContext(self.contextin)
		useContext(self.context)


	def createAsteriskConfiglet(self):
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
		c.append("context=%s" % self.contextin)
		c.append("incomingmsn=*")
		c.append("controller=1")
		c.append("softdtmf=1")
		c.append("devices=2")

		# Write dialin entry:
		if self.extin:
			c = AstConf("extensions.conf")
			c.setSection("in-pstn")
			c.appendExten("s", "Goto(default,%s,1)" % self.extin)

		# Write dialout entry:
		if self.ext and self.context:
			ext = self.ext
			if ext.endswith("*"):
				ext = "_%s." % ext[:-1]
			c.setSection(self.context)
			c.appendExten(ext, "Dial(CAPI/%s:${EXTEN:%d},60,TR)" % (self.msn, len(ext)-2))
