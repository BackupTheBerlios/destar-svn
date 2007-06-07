# -*- coding: iso-latin-1 -*-
#
# This module is Copyright (C) 2005 by Alejandro Rios
# Destar is Copyright (C) 2005 by Holger Schurig
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


class CfgDialoutNormal(CfgDialout):

	shortName = _("Normal dialout entry")
	newObjectTitle= _("New normal dialout entry")
	description = _("""Used to route calls through trunks""")
	groupName = 'Dialout'
					
	def createVariables(self):
		self.variables = [
		VarType("name",   
			title=_("Name"), 
			len=15),

		VarType("pattern", 
			title=_("Pattern"), 
			len=55),

		VarType("rmprefix", 
			title=_("Remove Prefix of length"), 
			len=10, 
			default="0"),

		VarType("addprefix", 
			title=_("Add Prefix"), 
			len=10, 
			optional=True, 
			default=""),

		VarType("maxtime", 
			title=_("Maximum call time in seconds"), 
			type="int", 
			len=15, 
			default=6000),

		VarType("ringtime", 
			title=_("Ringing time in seconds"), 
			type="int", 
			len=15, 
			default=30),

		VarType("qlookup", 
			title=_("Search on quick dial list?"), 
			type="bool"),

		VarType("dis_transfer", 
			title=_("Disable transfer to the calling party?"), 
			type="bool", 
			default=False),

		VarType("Trunks", 
			title=_("Trunks to use for routing this dialout entry"), 
			type="label", 
			len=15, 
			hide=True)
		]

		Cfg.fixup(self)
		if varlist_manager.hasTrunks() > 0:
			self.variables += varlist_manager.getTrunks()
			for v in self.variables:	
				if v.name == "Trunks" or v.name=="defaulttrunk":
					v.hide = False
					
					
		self.dependencies = []
		for var in self.__dict__.keys():
			if var.startswith('trunk_'):
				self.dependencies.append(
					DepType(var,
							type="hard",
							message = _("This is a Dependency")))
							
	def createDependencies(self):
		for dep in self.dependencies:
			if self.__dict__.has_key(dep.name):
				obj_name = dep.name[6:] # get the name after "trunk_"
				import configlets
				obj = configlets.configlet_tree.getConfigletByName(obj_name)
				if obj is None:
					return
				dependent_obj = DependentObject(self, dep)
				obj.dependent_objs.append(dependent_obj)

	def isAddable(self):
		"We can only add this object if we have at least one trunk defined."
		import configlets
		return (len(configlets.configlet_tree['Trunks']) > 0)

	isAddable = classmethod(isAddable)


	def createAsteriskConfig(self):
		c = AstConf("macros.inc")
		c.setSection("macro-%s" % self.name)
		c.append("; params: exten,secret,timeout")
		needModule("app_authenticate")
		if self.dis_transfer:
		       opts="tW"
		else:
		       opts="TtW"
		if self.qlookup:
			c.appendExten("s",'Set(options=%sr)' % opts)
			c.appendExten("s","Set(dest=${DB(QUICKDIALLIST/GLOBAL/${ARG1})})",e="Goto(3)")
			c.appendExten("s",'Set(ARG1=${dest})')
			c.appendExten("s","GotoIf($[${ARG2} = n]?6:5)")
			c.appendExten("s","Authenticate(${ARG2})")
			c.appendExten("s","GotoIf($[${ARG3} = 0]?7:10)")
			c.appendExten("s",'Set(timeout=0)')
			c.appendExten("s",'Set(options=%s)' % opts)
			c.appendExten("s",'Goto(11)')
		else:
			c.appendExten("s",'Set(options=%sr)' % opts)
			c.appendExten("s","GotoIf($[${ARG2} = n]?4:3)")
			c.appendExten("s","Authenticate(${ARG2})")
			c.appendExten("s","GotoIf($[${ARG3} = 0]?5:8)")
			c.appendExten("s",'Set(timeout=0)')
			c.appendExten("s",'Set(options=%s)' % opts)
			c.appendExten("s",'Goto(10)')
		c.appendExten("s",'Set(timeout=%d)' % self.maxtime)
		c.appendExten("s",'Set(options=%sL(%d000:10000))' % (opts,self.maxtime))
		#TODO: add this trunks sorted by price and with a default one.
		import configlets
		tapisupport = False
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ == 'CfgOptSettings':
				if obj.tapi:
				    tapisupport = True
		for obj in configlets.configlet_tree['Trunks']:
			try:
				if self.__getitem__("trunk_"+obj.name):
					c.appendExten("s","Set(TIMEOUT(absolute)=${timeout})")
					c.appendExten("s","Set(CDR(outtrunk)=%s)" % obj.name)
					if self.__getitem__("trunk_%s_price" % obj.name):
						c.appendExten("s","Set(CDR(accountcode)=%s)" % self.__getitem__("trunk_%s_price" % obj.name))
					else:
						c.appendExten("s","Set(CDR(accountcode)=0)")
					if obj.clidnameout:
						c.appendExten("s","Set(CALLERID(name)=%s)" % obj.clidnameout)
					if obj.clidnumout:
						c.appendExten("s","Set(CALLERID(number)=%s)" % obj.clidnumout)
				        if tapisupport:
					        c.appendExten("s","Set(chan=${CUT(CHANNEL,,1)})")
					        c.appendExten("s","UserEvent(TAPI|TAPIEVENT: LINE_NEWCALL ${chan})")
	    				        c.appendExten("s","UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_DIALTONE)")
					        c.appendExten("s","UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_DIALING)")
					        c.appendExten("s","UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_PROCEEDING)")
					c.appendExten("s","Dial(%s,%d|${options})" % (obj.dial,self.ringtime))
			except KeyError:
				pass
		c.appendExten("s","Congestion(5)")
		c.appendExten("s","Goto(9)")
		c.appendExten("T","ResetCDR(w)")
		c.appendExten("T","NoCDR")
		c.appendExten("T","Hangup")
		c.appendExten("t","ResetCDR(w)")
		c.appendExten("t","NoCDR")
		c.appendExten("t","Hangup")
		if tapisupport:
		        c.appendExten("h","UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_IDLE)")

