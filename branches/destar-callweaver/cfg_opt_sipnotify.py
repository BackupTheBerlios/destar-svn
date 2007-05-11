# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 by Harald Holzer
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


class CfgOptEnum(CfgOpt):

	shortName = _("Sip notify")
	newObjectTitle= _("Sip notify")
	
	def createVariables(self):
		self.variables = [
			VarType("info",
			    title=_("Enables the sip notify command to reboot or sync phones on callweaver commanline."),
			    type="label",
			    )]

	def createAsteriskConfig(self):
		c = AstConf("sip_notify.conf")
		c.setSection("snom-reboot")
		c.append("Event=>reboot")
		c.append("Content-Length=>0")
		c.append("")
		c.setSection("snom-check-cfg")
		c.append("Event=>check-sync;reboot=false")
		c.append("Content-Length=>0")
		c.append("")
		c.setSection("polycom-check-cfg")
		c.append("Event=>check-sync")
		c.append("Content-Length=>0")
		c.append("")
		c.setSection("sipura-check-cfg")
		c.append("Event=>resync")
		c.append("Content-Length=>0")
		c.append("")
		c.setSection("grandstream-check-cfg")
		c.append("Event=>sys-control")
		c.append("")
		c.setSection("cisco-check-cfg")
		c.append("Event=>check-sync")
		c.append("Content-Length=>0")

	def row(self):
		return (self.shortName, "")
