# -*- coding: iso-latin-1 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig
# This file has Copyright (C) 2005 by Alejandro Rios
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

import panelutils
from configlets import *


class CfgOptOPPanel(CfgOptSingle):

	shortName = _("Operator Panel")
	newObjectTitle= _("Operator Panel")
	description = _("Configure Asternic Flash Operator Panel")
	groupName = 'Options'
	 
	def createVariables(self):
		self.variables = [
			VarType("name",
				title=_("Name"),
				len=15,
				default="oppanel"),

			VarType("web_hostname",
				title=_("FQDN/IP to access the panel via web"),
				len=15,
				optional=True),
			
			VarType("security_code",
				title=_("Security Code"),
				len=15,
				default=generatePassword(8)),

			VarType("btnsize",
				title=_("Button Size"),
				type="choice",
				options=(
					("vsmall", _("Very Small"), "vsmall"),
					("small", _("Small"), "small"),
					("normal", _("Normal"), "normal"),
					("large", _("Large"), "large"),
					("vlarge", _("Very Large"), "vlarge"),
					),
				default="normal"
				),

			VarType("manager",
				title=_("Manager agent"),
				type="choice",
				options=getChoice("CfgOptManager")),

			VarType("poll_interval",
				title=_("Frequency in seconds to poll for sip and iax status"),
				len=10,
				default="60"),
		]

	def createAsteriskConfig(self):
		c = AstConf("op_server.cfg")
                c.setSection("general")
		if self.web_hostname:
			c.appendValue(self, "web_hostname")	

		c.appendValue(self, "security_code")	
		c.appendValue(self, "poll_interval")	
		panelutils.createManagerConfig(self)
		panelutils.createDefaultConfig(c)	

		c = AstConf("op_style.cfg")
		panelutils.createDefaultStyle(c)

		LABEL_FONT_SIZE = 20
		CLID_FONT_SIZE = 13
		BTN_WIDTH = 246
		BTN_HEIGHT = 70
		LED_SCALE = 90
		LED_MARGIN_TOP = 34
		LED_MARGIN_LEFT = 20
		ICON1_MARGIN_TOP = 43
		ICON1_MARGIN_LEFT = -34
		ICON1_SCALE = 17
		ICON2_MARGIN_TOP = 46
		ICON2_MARGIN_LEFT = -29
		ICON2_SCALE = 14
		ICON3_MARGIN_TOP = 34
		ICON3_MARGIN_LEFT = -36
		ICON3_SCALE = 20
		ICON4_MARGIN_TOP = 33
		ICON4_MARGIN_LEFT = -34
		ICON4_SCALE = 16
		ICON5_MARGIN_TOP = 32
		ICON5_MARGIN_LEFT = -33
		ICON5_SCALE = 16
		ICON6_MARGIN_TOP = 32
		ICON6_MARGIN_LEFT = -33
		ICON6_SCALE = 16
		IN_LEFT = -33
		ICON6_SCALE = 16
		MAIL_MARGIN_LEFT = -23
		MAIL_MARGIN_TOP = 13
		MAIL_SCALE = 9

		if self.btnsize == "vsmall": scale = 0.6
		elif self.btnsize == "small": scale = 0.8
		elif self.btnsize == "large": scale = 1.2
		elif self.btnsize == "vlarge": scale = 1.4
		else: scale = 1

		c.append("label_font_size=%s" % int(LABEL_FONT_SIZE * scale) )
		c.append("clid_font_size=%s" % int(CLID_FONT_SIZE * scale) )
		c.append("btn_width=%s" % int(BTN_WIDTH * scale) )
		c.append("btn_height=%s" % int(BTN_HEIGHT * scale) )
		c.append("led_scale=%s" % int(LED_SCALE * scale) )
		c.append("led_margin_top=%s" % int(LED_MARGIN_TOP * scale) )
		c.append("led_margin_left=%s" % int(LED_MARGIN_LEFT * scale) )
		c.append("icon1_margin_top=%s" % int(ICON1_MARGIN_TOP * scale) )
		c.append("icon1_margin_left=%s" % int(ICON1_MARGIN_LEFT * scale) )
		c.append("icon1_scale=%s" % int(ICON1_SCALE * scale) )
		c.append("icon2_margin_top=%s" % int(ICON2_MARGIN_TOP * scale) )
		c.append("icon2_margin_left=%s" % int(ICON2_MARGIN_LEFT * scale) )
		c.append("icon2_scale=%s" % int(ICON2_SCALE * scale) )
		c.append("icon3_margin_top=%s" % int(ICON3_MARGIN_TOP * scale) )
		c.append("icon3_margin_left=%s" % int(ICON3_MARGIN_LEFT * scale) )
		c.append("icon3_scale=%s" % int(ICON3_SCALE * scale) )
		c.append("icon4_margin_top=%s" % int(ICON4_MARGIN_TOP * scale) )
		c.append("icon4_margin_left=%s" % int(ICON4_MARGIN_LEFT * scale) )
		c.append("icon4_scale=%s" % int(ICON4_SCALE * scale) )
		c.append("icon5_margin_top=%s" % int(ICON5_MARGIN_TOP * scale) )
		c.append("icon5_margin_left=%s" % int(ICON5_MARGIN_LEFT * scale) )
		c.append("icon5_scale=%s" % int(ICON5_SCALE * scale) )
		c.append("icon6_margin_top=%s" % int(ICON6_MARGIN_TOP * scale) )
		c.append("icon6_margin_left=%s" % int(ICON6_MARGIN_LEFT * scale) )
		c.append("icon6_scale=%s" % int(ICON6_SCALE * scale) )
		c.append("mail_margin_left=%s" % int(MAIL_MARGIN_LEFT * scale) )
		c.append("mail_margin_top=%s" % int(MAIL_MARGIN_TOP * scale) )
		c.append("mail_scale=%s" % int(MAIL_SCALE * scale) )

	def row(self):
		return (self.shortName, self.name)
