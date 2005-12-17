# -*- coding: iso-latin-1 -*-
#
# This modules is Copyright (C) 2005 by Alejandro Rios,
# Destar is Copyright (C) 2005 by Holger Schurig,
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
import os

class CfgIVRAutoatt(CfgIVR):

	shortName = _("Auto attendant")
	newObjectTitle= _("New auto attendant")
	description = _("""Basic auto-attendant.""")
	groupName = 'IVRs'
		
	variables = [
		VarType("name",	  title=_("Name"), len=25),
		VarType("timeout",   title=_("Max. time for incoming calls in seconds"), hint=_("(0 or empty means no time restriction)"), optional=True, len=10,default=0),
		VarType("moh",	  title=_("Music-on-hold class"), type="choice", optional=True,
			options=getChoice("CfgOptMusic")),
		VarType("backgroundfile",   title=_("File to play in the background"),default="beep"),
		VarType("repeat", title=_("How many times should it be played?"), default=1, len=2, type="int"),
		VarType("pause", title=_("Pause between each playback"), optional=True, len=2),
		VarType("ext",	  title=_("Extension to ring after file playing"), type="choice",
			options=getChoice("CfgPhone")),
		VarType("operator",  title=_("Digit to jump that extension directly"), optional=True, len=1),
		VarType("ivrtime",	  title=_("IVR to jump on special dates"), type="choice",
			options=getChoice("CfgIVR"), render_br=False, optional=True),
		VarType("times",   title=_("Times string"),hint=_("i.e. <hours>|<weekdays>|<monthdays>|<months> (comma separated)"),default="", optional=True, len=300),
		VarType("phones", title=_("Allow calling to all extensions?"), type="bool"),
		
	]

	def isAddable(self):
		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.groupName == 'Phones':
				return True
		return False
	isAddable = classmethod(isAddable)

	def checkConfig(self):
		return CfgIVR.checkConfig(self)
		if self.repeat < 1:
			return ("repeat",_("File should be played at least one time"))
		if self.ivrtime and not self.times:
			return ("times",_("Please specify dates"))
		
	def createAsteriskConfig(self):
		s = AstConf("extensions.conf")
		s.setSection(self.name)
		if self.phones:
			s.append("include=phones")
		s.appendExten("s","Wait(1)")
		s.appendExten("s","DigitTimeout,2.3")
		if self.ivrtime:
			if self.times:
				times=self.times.split(',')
				for t in times:
					s.appendExten("s","GotoIf(%s?%s,s,1)" % (t,self.ivrtime))
		if self.timeout:
			s.appendExten("s","Absolutetimeout(%s)" % self.timeout)
		if self.moh:
			s.appendExten("s","Setmusiconhold(%s)" % self.moh)
		for i in range(self.repeat):
			s.appendExten("s","Background(%s)" % self.backgroundfile)	
			if self.pause:
				s.appendExten("s","WaitExten(%s)" % self.pause)
		s.appendExten("s","Goto(phones,%s,1)" % self.ext)	
		if self.operator:
			s.appendExten("%s" % self.operator, "Goto(phones,%s,1)" % self.ext)	
		s.appendExten("i","Playback(privacy-invalid)")	
		s.appendExten("i","Goto(phones,%s,1)" % self.ext)	
		s.appendExten("t","ResetCDR(w)")
		s.appendExten("t","NoCDR")
		s.appendExten("t","Hungup")
		s.appendExten("T","ResetCDR(w)")
		s.appendExten("T","NoCDR")
		s.appendExten("T","Hungup")
	

	def row(self):
		return (self.shortName,self.name)
