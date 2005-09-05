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
import panelutils

class CfgAppMeetme(CfgApp):

	shortName   = _("Meeting room")
	variables   = [	VarType("ext",      title=_("Extension"), len=6),
		       	VarType("confno",   title=_("Conference number"), hint=_("If empty, will be the same as the extension"), optional=True, len=6),
		       	VarType("pin",      title=_("PIN"), optional=True, len=6),
			
			VarType("panelLab",   title=_("Operator Panel"), type="label", hide=True),
                	VarType("panel",      title=_("Show this trunk in the panel"), type="bool", hide=True)
			]

	def fixup(self):
		Cfg.fixup(self)
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False

	def createAsteriskConfig(self):
		needModule("app_meetme")

		c = AstConf("extensions.conf")
		c.setSection("apps")
		c.appendExten(self.ext, "Answer")
		c.appendExten(self.ext, "Wait(1)")
		# 'd' -- dynamically add conference
		# 'p' -- allow user to exit the conference by pressing '#'
		if not self.confno:
			self.confno = self.ext
		c.appendExten(self.ext, "MeetMe(%s,dp)" % self.confno)

		c = AstConf("meetme.conf")
		c.setSection("rooms")
		if self.pin:
			c.append("conf=%s,%s" % (self.confno, self.pin))
		else:
			c.append("conf=%s" % self.confno)
		
		try:
			if panelutils.isConfigured() == 1 and self.panel:
				panelutils.createMeetmeButton(self)
		except AttributeError:
			pass
