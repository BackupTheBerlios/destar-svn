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


class CfgLineZapTDM(CfgLine):

	shortName = _("PSTN using zaptel-tdm")
	variables = [
		VarType("name",  title=_("Name"), len=35),
		VarType("channel", title=_("Zaptel channel number"), type="rostring", default=1, len=2),
		VarType("lang", title=_("Channel Language"), default="en", len=2),
		VarType("sigtype", title=_("Signalling type"), type="choice", options=[('ks', 'kewlstart'),('ls','loopstart')]),

		VarType("Outbound",  title=_("Calls to the PSTN network"), type="label"),
		VarType("ext",   title=_("Outgoing prefix"), optional=True, len=6),
		]


	def isAddable(self):
		return False
	isAddable = classmethod(isAddable)


	def fixup(self):
		CfgLine.fixup(self)
		useContext("in-pstn")


	def createAsteriskConfiglet(self):
		needModule("chan_zap")

		# Create config for chan_zap:
		c = AstConf("zapata.conf")
		if not c.hasSection("channels"):
			c.setSection("channels")
			c.append("language=%s" %self.lang)
		c.append("signalling=fxs_%s" % self.sigtype)
		c.append("callerid=")
		#prefix = ""
		#c.append("dialplan=local")
		#c.append("pridialplan=local")
		#immediate must be no according to http://www.voip-info.org/wiki-Asterisk+tips+DID
		#c.append("immediate=yes")
		c.append("group=1")
		# TODO?
		c.append("context=in-pstn")
		c.append("channel=%d" % self.channel)
		#c.append("echocancel=yes")

		# Write dialout entry:
		if self.ext:
			c = AstConf("extensions.conf")
			c.setSection("default")
			c.appendExten("_%s." % self.ext, "Dial(Zap/%d/${EXTEN:%d},60)" % (self.channel,len(self.ext)))

	
	def zapType(self):
		return 'fxo'
