# -*- coding: utf-8 -*-
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
	
	def createVariables(self):
		self.variables = [
			VarType("name",
					title=_("Name"),
					len=25),

			VarType("waittime",
					title=_("Time to wait before answer the line"),
					hint=_("(in seconds)"),
					len=10,
					type="int",
					default=2),

			VarType("digittimeout",
					title=_("How many time has the user to dial an extension?"),
					hint=_("(in seconds)"),
					len=10,
					type="int",
					default=3),

			VarType("timeout",
					title=_("Max. time for incoming calls in seconds"),
					hint=_("(0 or empty means no time restriction)"),
					optional=True,
					len=10,
					type="int",
					default=0),

			VarType("moh",
					title=_("Music-on-hold class"),
					type="choice",
					optional=True,
					options=getChoice("CfgOptMusic")),

			VarType("backgroundfile",
					title=_("File to play in the background"),
					default="beep"),

			VarType("repeat",
					title=_("How many times should it be played?"),
					default=1,
					len=2,
					type="int"),

			VarType("pause",
					title=_("Pause between each playback"),
					optional=True,len=2),

			VarType("exten",
					title=_("Extension to ring after file playing"),
					type="choice",
					options=getChoice("CfgPhone")),

			VarType("operator",
					title=_("Digit to jump that extension directly"),
					optional=True,
					len=1),

			VarType("ivrtime",
					title=_("IVR to jump on special dates"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),

			VarType("times",
					title=_("Times string"),
					hint=_("i.e. hours,weekdays,monthdays,months (comma separated)"),
					default="",
					optional=True,
					len=300),

			VarType("pbx", 
					title=_("Allow calling to all extensions of PBX"),
					type="choice", 
					options=getChoice("CfgOptPBX"),
					optional=True)
				]

		self.dependencies = [
			DepType("moh", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("exten", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("ivrtime", 
					type="hard",
					message = _("This is a Dependency"))]



	def isAddable(self):
		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		return len(configlets.configlet_tree['Phones']) > 0
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
		if self.pbx:
			pbx = self.pbx
		else:	
			pbx = "phones"
		s.append("include=%s" % pbx)
		s.appendExten("s","Wait(%d)" % self.waittime, context=self.name)
		s.appendExten("s","Set(TIMEOUT(digit)=%d)" % self.digittimeout, context=self.name)
		if self.moh:
			s.appendExten("s","Setmusiconhold(%s)" % self.moh, context=self.name)
			s.appendExten("s","Set(DIAL_OPTIONS=m)", context=self.name)
		else:
			s.appendExten("s","Set(DIAL_OPTIONS=r)", context=self.name)
		if self.ivrtime:
			if self.times:
				times=self.times.split(',')
				for t in times:
					s.appendExten("s","GotoIfTime(%s?%s,s,1)" % (t,self.ivrtime), context=self.name)
		if self.timeout:
			s.appendExten("s","Set(TIMEOUT(absolute)=%s)" % self.timeout, context=self.name)
		for i in range(self.repeat):
			s.appendExten("s","Background(ivr/%s)" % self.backgroundfile, context=self.name)	
			if self.pause:
				s.appendExten("s","WaitExten(%s)" % self.pause, context=self.name)
		s.appendExten("s","Goto(%s,%s,1)" % (pbx,self.exten), context=self.name)	
		if self.operator:
			s.appendExten("%s" % self.operator, "Goto(%s,%s,1)" % (pbx,self.exten), context=self.name)	
		s.appendExten("i","Playback(invalid)", context=self.name)	
		s.appendExten("i","Goto(%s,%s,1)" % (pbx,self.exten), context=self.name)	
		s.appendExten("t","ResetCDR(w)", context=self.name)
		s.appendExten("t","NoCDR", context=self.name)
		s.appendExten("t","Hangup", context=self.name)
		s.appendExten("T","ResetCDR(w)", context=self.name)
		s.appendExten("T","NoCDR", context=self.name)
		s.appendExten("T","Hangup", context=self.name)
	

	def row(self):
		return (self.shortName,self.name)
