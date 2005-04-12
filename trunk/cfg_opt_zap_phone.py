# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2005 by Holger Schurig,
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


class CfgOptZap(CfgOptSingle):

	shortName = _("Global Zaptel Phone Options")
	variables = [
		VarType("AnalogOptions", title=_("Analog phone options"), type="label"),
		VarType("adsi", title=_("Use ADSI for menu phones"), type="bool"),
		VarType("callwaiting", title=_("Signal a waiting call"), type="bool"),
		VarType("callwaitingcallerid", title=_("Send callerid during call waiting indication"), type="bool"),
		VarType("threewaycalling", title=_("Suspend a call temporarily via a hook flash"), type="bool"),
		VarType("transfer", title=_("Allow call transfer"), type="bool", default=True),
		VarType("cancallforward", title=_("Allow call forwards"), type="bool", default=True),
		VarType("callreturn", title=_("Read caller number with *69"), type="bool", default=True),

		VarType("AudioOptions", title=_("Audio Quality Tuning"), type="label"),
		VarType("relaxdtmf", title=_("Be sloppy when detecting DTMF"), type="bool"),
		VarType("echocancel", title=_("Echo cancel samples"), type="choice", options=["0 (no echo cancel)", "16", "32", "64", "128", "256"], default="128"),
		VarType("echocancelwhenbridged", title=_("Cancel echo even on bridged calls"), type="bool"),
		VarType("echotraining", title=_("Do early echo training"), type="bool"),
	]


	def createAsteriskConfig(self):
		c = AstConf("zapata.conf")
		c.setSection("channels")

		# Analog trunk features
		#c.appendValue(self, "busydetect")
		#c.appendValue(self, "busycount")
		#c.appendValue(self, "callprogrss")
		#c.appendValue(self, "pulsedial")
		

		c.append("immediate=no")
		c.append("overlapdial=yes")
		c.append("cancallforward=no")

		c.appendValue(self, "adsi")
		c.appendValue(self, "callwaiting")
		c.appendValue(self, "callwaitingcallerid")
		c.appendValue(self, "threewaycalling")
		c.appendValue(self, "transfer")
		c.appendValue(self, "cancallforward")
		c.appendValue(self, "callreturn")

		c.appendValue(self, "relaxdtmf")
		c.appendValue(self, "echocancel")
		c.appendValue(self, "echocancelwhenbridged")
		c.appendValue(self, "echotraining")
		#c.appendValue(self, "rxgain=")
		#c.appendValue(self, "txgain=")

		c.append("")
