# -*- coding: utf-8 -*-
#
# This modules is Copyright (C) 2007 by Alejandro Rios,
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

class CfgIVRTreeNode(CfgIVR):

	shortName = _("IVR Tree node")
	newObjectTitle= _("New IVR tree node")
	description = _("""Basic IVR which connects to other IVRs.""")
	groupName = 'IVRs'
	
	def createVariables(self):
		self.variables = [
			VarType("name",
					title=_("Name"),
					len=25),

			VarType("digittimeout",
					title=_("How much time has the user to dial an extension?"),
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

			VarType("operator",
					title=_("Extension to ring after file playing or by pressing '0'"),
					type="choice",
					options=getChoice("CfgPhone")),

			VarType("waittime",
					title=_("Time to wait before jumping to extension"),
					hint=_("(in seconds)"),
					len=10,
					type="int",
					default=2),

			VarType("pbx", 
					title=_("Allow calling to all extensions of PBX"),
					type="choice", 
					options=getChoice("CfgOptPBX"),
					optional=True),

			VarType("ivrtime",
					title=_("IVR to jump on special dates"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),

			VarType("times",
					title=_("Times string"),
					hint=_("i.e. *|*|25|dec,*|*|20|jul (comma separated)"),
					default="",
					optional=True,
					len=300),

			VarType("ivr_1",
					title=_("IVR to jump when pressing '1'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_1",
					title=_("Phone to jump when pressing '1'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),
			VarType("ivr_2",
					title=_("IVR to jump when pressing '2'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_2",
					title=_("Phone to jump when pressing '2'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_3",
					title=_("IVR to jump when pressing '3'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_3",
					title=_("Phone to jump when pressing '3'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_4",
					title=_("IVR to jump when pressing '4'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_4",
					title=_("Phone to jump when pressing '4'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_5",
					title=_("IVR to jump when pressing '5'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_5",
					title=_("Phone to jump when pressing '5'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_6",
					title=_("IVR to jump when pressing '6'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_6",
					title=_("Phone to jump when pressing '6'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_7",
					title=_("IVR to jump when pressing '7'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_7",
					title=_("Phone to jump when pressing '7'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_8",
					title=_("IVR to jump when pressing '8'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_8",
					title=_("Phone to jump when pressing '8'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_9",
					title=_("IVR to jump when pressing '9'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_9",
					title=_("Phone to jump when pressing '9'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True),

			VarType("ivr_ast",
					title=_("IVR to jump when pressing '*'"),
					type="choice",
					options=getChoice("CfgIVR"),
					render_br=False,
					optional=True),
			VarType("phone_ast",
					title=_("Phone to jump when pressing '*'"),
					type="choice",
					options=getChoice("CfgPhone"),
					optional=True)

				]

		self.dependencies = [
			DepType("moh", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("operator", 
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
		context = self.name
		s.setSection(context)
		if self.pbx:
			pbx = self.pbx
		else:	
			pbx = "phones"
		s.append("include=%s" % pbx)
		s.appendExten("s","Ringing()", context)
		s.appendExten("s","Set(TIMEOUT(digit)=%d)" % self.digittimeout, context)
		dopt=""
		if self.moh:
			# Use Music as ringback tone
			s.appendExten("s","Setmusiconhold(%s)" % self.moh, context)
			dopt+=("m")
		else:
			# Ringback
			dopt+=("r")
		if VICIDIAL_INTEGRATION:
			dopt+=("o")
		s.appendExten("s","Set(DIAL_OPTIONS=%s)" % dopt, context)
		if self.ivrtime:
			if self.times:
				times=self.times.split(',')
				for t in times:
					s.appendExten("s","GotoIfTime(%s?%s,s,1)" % (t,self.ivrtime), context)
		if self.timeout:
			s.appendExten("s","Set(TIMEOUT(absolute)=%s)" % self.timeout, context)
		for i in range(self.repeat):
			s.appendExten("s","Background(%s)" % self.backgroundfile, context)	
			if self.pause:
				s.appendExten("s","WaitExten(%s)" % self.pause, context)
		s.appendExten("s","WaitExten(%d)" % self.waittime, context)
		s.appendExten("s","Goto(%s,%s,1)" % (pbx,self.operator), context)	
		if self.ivr_1:
			s.appendExten("1","Goto(%s,s,1)" % self.ivr_1, context)	
		if self.ivr_2:
			s.appendExten("2","Goto(%s,s,1)" % self.ivr_2, context)	
		if self.ivr_3:
			s.appendExten("3","Goto(%s,s,1)" % self.ivr_3, context)	
		if self.ivr_4:
			s.appendExten("4","Goto(%s,s,1)" % self.ivr_4, context)	
		if self.ivr_5:
			s.appendExten("5","Goto(%s,s,1)" % self.ivr_5, context)	
		if self.ivr_6:
			s.appendExten("6","Goto(%s,s,1)" % self.ivr_6, context)	
		if self.ivr_7:
			s.appendExten("7","Goto(%s,s,1)" % self.ivr_7, context)	
		if self.ivr_8:
			s.appendExten("8","Goto(%s,s,1)" % self.ivr_8, context)	
		if self.ivr_9:
			s.appendExten("9","Goto(%s,s,1)" % self.ivr_9, context)	
		if self.ivr_ast:
			s.appendExten("*","Goto(%s,s,1)" % self.ivr_ast, context)	
		if self.phone_1:
			s.appendExten("1","Goto(%s,%s,1)" % (pbx,self.phone_1), context)	
		if self.phone_2:
			s.appendExten("2","Goto(%s,%s,1)" % (pbx,self.phone_2), context)	
		if self.phone_3:
			s.appendExten("3","Goto(%s,%s,1)" % (pbx,self.phone_3), context)	
		if self.phone_4:
			s.appendExten("4","Goto(%s,%s,1)" % (pbx,self.phone_4), context)	
		if self.phone_5:
			s.appendExten("5","Goto(%s,%s,1)" % (pbx,self.phone_5), context)	
		if self.phone_6:
			s.appendExten("6","Goto(%s,%s,1)" % (pbx,self.phone_6), context)	
		if self.phone_7:
			s.appendExten("7","Goto(%s,%s,1)" % (pbx,self.phone_7), context)	
		if self.phone_8:
			s.appendExten("8","Goto(%s,%s,1)" % (pbx,self.phone_8), context)	
		if self.phone_9:
			s.appendExten("9","Goto(%s,%s,1)" % (pbx,self.phone_9), context)	
		if self.phone_ast:
			s.appendExten("*","Goto(%s,%s,1)" % (pbx,self.phone_ast), context)	
		s.appendExten("0", "Goto(%s,%s,1)" % (pbx,self.operator), context)	
		s.appendExten("i","Playback(invalida)", context)	
		#s.appendExten("i","Goto(%s,%s,1)" % (pbx,self.operator), context)	
		s.appendExten("i","Goto(s,1)", context)	
		s.appendExten("t","ResetCDR(w)", context)
		s.appendExten("t","NoCDR", context)
		s.appendExten("t","Hangup", context)
		s.appendExten("T","ResetCDR(w)", context)
		s.appendExten("T","NoCDR", context)
		s.appendExten("T","Hangup", context)
		s.appendExten("#","ResetCDR(w)", context)
		s.appendExten("#","NoCDR", context)
		s.appendExten("#","Hangup", context)
	

	def row(self):
		return (self.shortName,self.name)
