# -*- coding: utf-8 -*-
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


class CfgOptMusic(CfgOpt):

	shortName = _("Background music directory")
	newObjectTitle= _("New background music directory")
	
	def createVariables(self):
		self.variables = [VarType("name", title=_("Name"), len=15),
		     VarType("type", 
		     		title=_("Type"), 
				type="choice", 
				options=(("mp3", "mp3"), 
					("quietmp3", _("Quiet mp3")) ,
					("mp3nb", _("mp3 nbuffered")),
					("quietmp3nb", _("Quiet mp3 unbuffered")),
					("custom", _("Custom")),
					("files", _("Files"))),
					default="quietmp3",
					),

		     VarType("dir",  
		     		title=_("Directory"), 
				len=255),

		     VarType("app",  
		     		title=_("Application"), 
				len=255, 
				optional=True),
				]

	def checkConfig(self):
		return CfgOpt.checkConfig(self)
		if self.type == "custom" and not self.app:
			return ("app",_("Please specify an application"))

	def createAsteriskConfig(self):
		c = AstConf("musiconhold.conf")
		c.setSection(self.name)
		c.append("mode=%s" % self.type)
		c.append("directory=%s" % self.dir)
		if self.type == "custom" and self.app:
			c.append("application=%s" % self.app)

	def row(self):
		return (self.shortName, self.name)
