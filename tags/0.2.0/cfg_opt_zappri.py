# -*- coding: iso-latin-1 -*-
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


class CfgOptZapPRI(CfgOpt):

	shortName = _("Zaptel configuration for PRI")
	newObjectTitle = _("Zaptel configuration for PRI")
	def createVariables(self):
		self.variables = [
			VarType("name",       title=_("Name"), len=35),
			VarType("span",    title=_("Zaptel span"), hint=_("i.e. 1 if 1st card"), type="string", len=5),
			VarType("timing",    title=_("Zaptel timing parameter"), hint=_("Read zaptel documentation"), type="string", len=5),
			VarType("distance",    title=_("Line Build Out (dB)"), hint=_("Power level based on distance from the card to the service provider's gateway."), type="choice", 
					options=[
						('0',_("0: 0 db (CSU) / 0-133 feet (DSX-1)")),
						('1',_("1: 133-266 feet (DSX-1)")),
						('2',_("2: 266-399 feet (DSX-1)")),
						('3',_("3: 399-533 feet (DSX-1)")),
						('4',_("4: 533-655 feet (DSX-1)")),
						('5',_("5: -7.5db (CSU)")),
						('6',_("6: -15db (CSU)")),
						('7',_("7: -22.5db (CSU)"))
						]),
			VarType("framing", title=_("Framing"), type="choice",
								  options=[('d4',_('D4 (T1)')),('esf', _('ESF (T1)')),('ccs',_('CSS (E1)')),('cas',_('CAS (E1)'))]),
			VarType("coding", title=_("Coding"), type="choice",
								  options=[('ami',_('AMI (T1/E1)')),('b8zs', _('B8ZF (T1)')),('hdb3',_('HDB3 (E1)'))]),
	
			VarType("channels",    title=_("Channels"), hint=_("i.e. 1-15,17-31"), type="string", len=20),
			VarType("dchannel",    title=_("Signaling channel"), hint=_("i.e. 16"), type="string", len=5),
			]


	def row(self):
		return (self.shortName, self.name)

	def createAsteriskConfig(self):
		needModule("chan_zap")

		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("# %s" % self.name)
		c.append("span=%s,%s,%s,%s,%s,crc4" % (self.span,self.timing,self.distance,self.framing,self.coding))
		c.append("bchan=%s" % self.channels)
		c.append("dchan=%s" % self.dchannel)
		c.append("")

