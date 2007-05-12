# -*- coding: iso-latin-1 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2006 by Alejandro Rios P.
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


class CfgTrunkUnicall(CfgTrunk):

	shortName = _("Standard Unicall MFC/R2 trunk")
	newObjectTitle = _("New standard MFC/R2 trunk")
	technology = "UniCall"
	
	def createVariables(self):
		self.variables = [
			VarType("name",
				title=_("Name"),
				len=35),

			VarType("signalling",
				title=_("Signalling type"),
				type="choice",
				options=[('mcfr2_cpe',_('MFC/R2 signalling, CPE side')),
					('mcfr2_co', _('MFC/R2 signalling, Network side'))]),
					
			VarType("protocolvariant",
				title=_("Protocol variant"),
				hint=_("i.e. cn,20,7"),
				type="string",
				len=20),
				
			VarType("channels",
				title=_("Channels"),
				hint=_("i.e. 1-15,17-31"),
				type="string",
				len=20),
				
			VarType("group",
				title=_("Callout group"),
				type="string",
				optional=True),

			VarType("faxdetect",
				title=_("Fax detection"),
				type="choice",
			      	options=[('incoming','Incoming only'),
					('outgoing', 'Outgoing only'),
					('both', 'Both Incoming/Outgoing'),
					('no', 'Disable')],
				default="no"),

		# TODO: check op-panel support for Unicall.
		#	VarType("panelLab",
		#		title=_("Operator Panel"),
		#		type="label",
		#		hide=True),

		#	VarType("panel",
		#		title=_("Show this trunk in the panel"),
		#		type="bool",
		#		hide=True,
		#		optional=True),

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
				title=_("Calls from PRI channel(s)"),
				type="label"),

			VarType("clid",
				title=_("Change Caller*Id to:"),
				len=25,
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

	def isAddable(self):
		"""We can only add this configlet if we have at least one
		ZapPRI option defined."""

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ == 'CfgOptZapPRI':
				return True
		return False 
	isAddable = classmethod(isAddable)

	def checkConfig(self):
                res = CfgTrunk.checkConfig(self)
                if res:
                        return res
		import configlets
		for obj in configlets.configlet_tree:
			if obj.__class__.__name__ == 'CfgTrunkUnicall':
				if obj==self: continue
				try:
					if obj.group == self.group and obj.group:
						return ("group", _("Group already in use"))
				except AttributeError:
					pass


	def fixup(self):
		CfgTrunk.fixup(self)
		if not self.rxgain:
			self.rxgain = "0.0"
		if not self.txgain: 
			self.txgain = "0.0"


	def createAsteriskConfig(self):
		needModule("chan_unicall")

		# Create config for chan_unicall:
		c = AstConf("unicall.conf")
		c.append("")
		c.append("; Unicall MFC/R2 Trunk %s" % self.name)
		if self.group:
			c.appendValue(self, "group")
		c.append("protocolclass=mfcr2")
		c.appendValue(self, "protocolvariant")
		if self.signalling == 'mfcr2_cpe':
			c.append("protocolend=cpe")
		else:
			c.append("protocolend=co")
		contextin = "in-%s" % self.name
		c.append("context=%s" % contextin)
		c.appendValue(self, "faxdetect")
		c.append("usecallerid=yes")
		c.append("hidecallerid=no")
		c.append("callwaitingcallerid=yes")
		c.append("threewaycalling=yes")
		c.append("transfer=yes")
		c.append("cancallforward=yes")
		c.append("callreturn=yes")
		c.append("echocancel=yes")
		c.append("echocancelwhenbridged=yes")
		c.append("echotraining=yes")
		c.append("relaxdtmf=yes")
		c.append("immediate=yes")
		c.appendValue(self, "rxgain")
		c.appendValue(self, "txgain")
		c.append("channel=%s" % self.channels)
		c.append("")

		#Dial part to use on dialout macro
		if self.group:
			self.dial = "UniCall/g%s/${ARG1}" % (self.group)
		else:
			self.dial = "UniCall/%s/${ARG1}" % (self.channels)
		
		#What to do with incoming calls
		self.createIncomingContext()

	# TODO: check op-panel support for Unicall.
	#	if panelutils.isConfigured() == 1 and self.panel:
	#		p = AstConf("op_buttons.cfg")
        #               chgrp = self.channels.split(',')
        #               for gr in chgrp:
        #                       gr_start_end = gr.split('-')
        #                       for ch in range(int(gr_start_end[0]),int(gr_start_end[1])+1):
        #                               p.setSection("%s/%d" % (self.technology, ch) )
        #                               p.append("Position=n")
        #                               p.append("Icon=2")
        #                               p.append("Extension=-1")
        #                               p.append("Label=%s-%d" % (self.name,ch))
