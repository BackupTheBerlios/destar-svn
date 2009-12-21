# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2005 by Alejandro Rios P.
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


class CfgTrunkDAHDIPRI(CfgTrunk):

	shortName = _("Standard ZAP PRI trunk")
	newObjectTitle = _("New standard ZAP PRI trunk")
	technology = "ZAP"
	
	def createVariables(self):
		self.variables = [
			VarType("name",
				title=_("Name"),
				len=35),

			VarType("signalling",
				title=_("Signalling type"),
				type="choice",
				options=[('pri_cpe',_('PRI signalling, CPE side')),
					('pri_net', _('PRI signalling, Network side'))]),
					
			VarType("switchtype",
				title=_("Switch type"),
				type="choice",
			      	options=[('national',_('National ISDN 2')),
					('dms100', _('Nortel DMS100')),
					('4ess', _('AT&T 4ESS')),
					('5ess', _('Lucent 5ESS')),
					('euroisdn', _('Euro ISDN')),
					('ni1', _('Old National ISDN 1'))],
				default="euroisdn"),
				
			VarType("pridialplan",
				title=_("PRI Dialplan"),
				type="choice",
			      	options=[('unknown',_('Unknown')),
					('private', _('Private ISDN')),
					('local', _('Local ISDN')),
					('national', _('National ISDN')),
					('international', _('International ISDN')),
					('dynamic', _('Dynamically selects the appropriate dialplan'))],
				default="unknown"),

			VarType("channels",
				title=_("Channels"),
				hint=_("i.e. 1-15,17-31"),
				type="string",
				len=20),
				
			VarType("group",
				title=_("Callout group"),
				type="string",
				optional=True),

			VarType("dialmethod",
				title=_("Dial Group Method: G/g/R/r"),
				type="choice",
				options=[('g',_('g: Ascending sequential hunt group')),
					('G', _('G: Descending sequential hunt group')),
					('r', _('r: Ascending rotary hunt group')),
					('R', _('R: Descending rotary hunt group'))],
				default="g"),

			VarType("panelLab",
				title=_("Operator Panel"),
				type="label",
				hide=True),

			VarType("panel",
				title=_("Show this trunk in the panel"),
				type="bool",
				hide=True,
				optional=True),

			VarType("Gains",
				title=_("Reception and Transmission Gains"),
				type="label"),

			VarType("rxgain",
				title=_("Reception gain"),
				hint=_("in dB"),
				optional=True,
				default="0.0"),

			VarType("txgain",
				title=_("Transmission gain"),
				hint=_("in dB"),
				optional=True,
				default="0.0"),

			VarType("Inbound",
				title=_("For incoming calls through this trunk:"),
				type="label"),

			VarType("clid",
				title=_("Change Caller*Id to:"),
				len=25,
				optional=True),

 			VarType("clidnumin",
 				title=_("Change Caller*Id Number to:"),
 				len=40,
 				optional=True),
			
			VarType("contextin",
				title=_("Go to"),
				type="radio",
				default='phone',
				options=[('phone',_("Phone")),('ivr',_("IVR")),('pbx',_("Virtual PBX"))]),

			VarType("phone",
				title=_("Extension to ring"),
				type="choice",
				optional=True,
				options=getChoice("CfgPhone")),

			VarType("ivr",
				title=_("IVR to jump to"),
				type="choice",
				optional=True,
				options=getChoice("CfgIVR")),

			VarType("pbx",
				title=_("Allow dial extension from which Virtual PBX"),
				type="choice",
				optional=True,options=getChoice("CfgOptPBX")),

			VarType("Outbound",
				title=_("For outgoing calls through this trunk:"),
				type="label"),

			VarType("clidnameout",
				title=_("Change Caller*Id Name to:"),
				len=40,
				optional=True),

			VarType("clidnumout",
				title=_("Change Caller*Id Number to:"),
				len=40,
				optional=True),

			VarType("dial",
				hide=True,
				len=50),]

		self.dependencies = [
			DepType("phone", 
					type="hard",
					message = _("This is a Dependency")),
			DepType("ivr", 
					type="hard",
					message = _("This is a Dependency"))
		]

#	def isAddable(self):
#		"""We can only add this configlet if we have at least one
#		DAHDIPRI option defined."""
#
#		# BUG: it does somehow not work to simply write for obj in config_entries,
#		# despite the "from configlets import *" above
#		import configlets
#		for obj in configlets.configlet_tree:
#			if obj.__class__.__name__ == 'CfgOptDAHDIPRI':
#				return True
#		return False 
#	isAddable = classmethod(isAddable)

	def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res
		#import configlets
		#for obj in configlets.configlet_tree:
		#	if obj.__class__.__name__ == 'CfgTrunkDAHDIPRI':
		#		if obj==self: continue
		#		try:
		#			if obj.group == self.group and obj.group:
		#				return ("group", _("Group already in use"))
		#		except AttributeError:
		#			pass


	def fixup(self):
		CfgTrunk.fixup(self)
		if not self.rxgain:
			self.rxgain = "0.0"
		if not self.txgain: 
			self.txgain = "0.0"


	def createAsteriskConfig(self):
		needModule("chan_dahdi")

		# Create config for chan_dahdi:
		c = AstConf("chan_dahdi.conf")
		c.append("")
		c.append("; DAHDItel Trunk %s" % self.name)
		if self.group:
			c.appendValue(self, "group")
		c.appendValue(self, "signalling")
		c.appendValue(self, "switchtype")
		c.append("resetinterval=never")
		c.append("prilocaldialplan=local")
		c.appendValue(self, "pridialplan")
		contextin = "in-%s" % self.name
		c.append("context=%s" % contextin)
		c.append("usecallerid=yes")
		c.append("callerid=asreceived")
		c.append("hidecallerid=no")
		c.append("callwaiting=no")
		c.append("usecallingpres=yes")
		c.append("callwaitingcallerid=no")
		c.append("threewaycalling=yes")
		c.append("transfer=yes")
		c.append("cancallforward=yes")
		c.append("callreturn=no")
		c.append("echocancel=yes")
		c.append("echocancelwhenbridged=yes")
		c.append("echotraining=yes")
		c.append("relaxdtmf=yes")
		c.append("immediate=no")
		c.append("busydetect=no")
		c.appendValue(self, "rxgain")
		c.appendValue(self, "txgain")
		c.append("channel=%s" % self.channels)
		c.append("")

		#Dial part to use on dialout macro
		if self.group:
                        self.dial = "DAHDI/%s%s/${ARG1}" % (self.dialmethod, self.group)
		else:
			self.dial = "DAHDI/%s/${ARG1}" % (self.channels)
		
		#What to do with incoming calls
		self.createIncomingContext()

		if panelutils.isConfigured() == 1 and self.panel:
			p = AstConf("op_buttons.cfg")
                        chgrp = self.channels.split(',')
                        for gr in chgrp:
                                gr_start_end = gr.split('-')
                                for ch in range(int(gr_start_end[0]),int(gr_start_end[1])+1):
                                        p.setSection("%s/%d" % (self.technology, ch) )
                                        p.append("Position=n")
                                        p.append("Icon=2")
                                        p.append("Extension=-1")
                                        p.append("Label=%s-%d" % (self.name,ch))
