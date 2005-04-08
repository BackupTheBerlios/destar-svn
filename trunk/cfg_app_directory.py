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


class CfgAppDirectory(CfgApp):

	shortName   = _("Directory")
	description = _("""The application allows you to dial by name.""")
	variables   = [VarType("ext", title=_("Extension"), len=6),
		       VarType("vmcontext", title=_("Voicemail Context"), default="default", len=15),
		       VarType("context", title=_("Context"), len=15)]

	def createAsteriskConfig(self):
		c = AstConf("extensions.conf")
		c.setSection(self.context)
		c.appendExten(self.ext, "Directory(%s)" % self.vmcontext)
		c.appendExten(self.ext, "Hangup")

