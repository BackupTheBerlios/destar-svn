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
from language import _


class CfgAppPhraseRecordingMenu(CfgApp):
	#http://www.voip-info.org/tiki-index.php?page=Asterisk+tips+phrase+recording+menu

	shortName   = _("Phrase recording menu")
	description = _("""NOT YET WORKING""")
		
	def createVariables(self):
		self.variables   = [VarType("ext",    title=_("Extension"), len=6)]

	def createAsteriskConfiglet(self):
		c = AstConf("extensions.conf")
		c.setSection("default")
		c.appendExten(self.ext, "Goto(phrase-menu,s,1)")

		if c.hasSection("phrase-menu"):
			return
		
		c.setSection("phrase-menu")
		c.appendExten("s", "Answer")
		c.appendExten("s", "DigitTimeout,5")
		c.appendExten("s", "ResponseTimeout,10")
		c.appendExten("s", "BackGround(custom/phrase-menu)")
		
		c.appendExten(1, "Wait(1)")
		c.appendExten(1, "Read(PHRASEID|custom/enter-phrase-num)")
		c.appendExten(1, "Record(custom/${PHRASEID}:gsm)")
		c.appendExten(1, "Wait(1)")
		c.appendExten(1, "Playback(custom/${PHRASEID},skip)")
		c.appendExten(1, "Wait(1)")
		c.appendExten(1, "Goto(s,2)")

		c.appendExten(2, "Wait(1)")
		c.appendExten(2, "Read(PHRASEID|custom/enter-phrase-num)")
		c.appendExten(2, "Playback(custom/${PHRASEID},skip)")
		c.appendExten(2, "Wait(1)")
		c.appendExten(2, "Goto(s,2)")

		c.appendExten("t", "Hangup")

		c.appendExten("i", "Playback(custom/invalid-option,skip)")
		c.appendExten("i", "Goto(s,2)")
