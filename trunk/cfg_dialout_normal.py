# -*- coding: utf-8 -*-
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

		VarType("otheropts", 
			title=_("Other Options for Dial Application"), 
			len=10, 
			optional=True, 
			default=""),

		VarType("maxtime", 
			title=_("Maximum call time in seconds"), 
			type="int", 
			len=15, 
			default=7200),

		VarType("ringtime", 
			title=_("Ringing time in seconds"), 
			type="int", 
			len=15, 
			default=600),

		VarType("qlookup", 
			title=_("Search on quick dial list?"), 
			type="bool"),

		VarType("dis_transfer", 
			title=_("Disable transfer to the calling party?"), 
			type="bool", 
			default=False),

		VarType("Outbound",
			title=_("Caller ID for calls established through this dialout"),
			type="label"),

		VarType("clidnameout",
			title=_("Change Caller*Id Name to:"),
			len=40,
			optional=True),

		VarType("clidnumout",
			title=_("Change Caller*Id Number to:"),
			len=40,
			optional=True),

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
		context="macro-%s" % self.name
		c.setSection(context)
		c.append("; params: exten,secret,timeout")
		needModule("app_authenticate")
		if self.dis_transfer:
			opts="tW"
		else:
			opts="TtW"
		c.append("exten=>s,1,Set(options=%s)" % opts)
		if self.otheropts:
			opts += self.otheropts
			#c.append("exten=>s,n,Playback(llamadasiendotransferida)")
		if self.qlookup:
			c.append("exten=>s,n(quickd),Set(dest=${DB(QUICKDIALLIST/GLOBAL/${ARG1})})")
			c.append("exten=>s,quickd+1,Goto(ifAuth)")
			c.append("exten=>s,n,Set(ARG1=${dest})")
		c.append("exten=>s,n(ifAuth),GotoIf($[${ARG2} = n]?ifTimeOut:auth)")
		c.append("exten=>s,n(auth),Authenticate(${ARG2})")
		c.append("exten=>s,n,Set(options=%s)" % opts.strip('r'))
		c.append("exten=>s,n(ifTimeOut),GotoIf($[${ARG3} = 0]?noTimeOut:setTimeOut)")
		c.append("exten=>s,n(noTimeOut),Set(timeout=0)")
		c.append("exten=>s,n,Goto(CallLimit)")
		c.append("exten=>s,n(setTimeOut),Set(timeout=%d)" % self.maxtime)
		c.append("exten=>s,n(CallLimit),Set(options=%sL(%d000:10000))" % (opts,self.maxtime))
		#TODO: add this trunks sorted by price and with a default one.

		import configlets
		unavail=1
		c.append("exten=>s,n,Set(TIMEOUT(absolute)=${timeout})")
		tapisupport = False
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ == 'CfgOptSettings':
				if obj.tapi:
				    tapisupport = True
		for obj in configlets.configlet_tree['Trunks']:
			try:
				if self.__getitem__("trunk_"+obj.name):
					c.append("exten=>s,n(unavail%s),Set(CDR(outtrunk)=%s)" % (unavail, obj.name) )
					if self.__getitem__("trunk_%s_price" % obj.name):
						c.append("exten=>s,n,Set(CDR(accountcode)=%s)" % self.__getitem__("trunk_%s_price" % obj.name))
					else:
						c.append("exten=>s,n,Set(CDR(accountcode)=0)")
					if self.clidnameout:
						c.append("exten=>s,n,Set(CALLERID(name)=%s)" % self.clidnameout)
					if self.clidnumout:
						c.append("exten=>s,n,Set(CALLERID(number)=%s)" % self.clidnumout)
				        if tapisupport:
						needModule("app_cut")
					        c.append("exten=>s,n,Set(chan=${CUT(CHANNEL,,1)})")
					        c.append("exten=>s,n,UserEvent(TAPI|TAPIEVENT: LINE_NEWCALL ${chan})")
	    				        c.append("exten=>s,n,UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_DIALTONE)")
					        c.append("exten=>s,n,UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_DIALING)")
					        c.append("exten=>s,n,UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_PROCEEDING)")
					c.append("exten=>s,n,Dial(%s,%d|${options})" % (obj.dial,self.ringtime))
					unavail+=1
					c.append('exten=>s,n,GotoIf($["${DIALSTATUS}" = "CHANUNAVAIL"]?unavail%s)' % unavail)
			except KeyError:
				pass
		c.append("exten=>s,n,Goto(busy)")
		c.append("exten=>s,n(unavail%s),Playback(all-circuits-busy-now)" % unavail)
		c.append("exten=>s,n(busy),Busy(5)")
		c.append("exten=>s,n,Hangup()")
		c.appendExten("T","ResetCDR(w)", context=context)
		c.appendExten("T","NoCDR", context=context)
		c.appendExten("T","Hangup", context=context)
		c.appendExten("t","ResetCDR(w)", context=context)
		c.appendExten("t","NoCDR", context=context)
		c.appendExten("t","Hangup", context=context)
		if tapisupport:
		        c.appendExten("h","UserEvent(TAPI|TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_IDLE)", context=context)

