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


class CfgAppAA(CfgApp):

	shortName   = _("Auto-Attendant")
	description = _("""Create a greeting that listens for IVR""")
	variables   = [VarType("name",      title=_("Auto Attendant Name")),
                       VarType("greeting",  title=_("Greeting File name")),
                       VarType("context",   title=_("Context")),
		      ]

	def createAsteriskConfiglet(self):
		c = AstConf("extensions.conf")
		c.setSection(self.context)
		c.append("exten => s,1,Answer")
		c.append("exten => s,2,Wait(0.5)")
		c.append("exten => s,3,Background(%s)" % self.greeting)
		c.append("exten => s,4,Background(silence/4)")
		c.append("exten => s,5,Goto(s,3)")
