# -*- coding: utf-8 -*-
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


class CfgOptVoicemail(CfgOptSingle):

	shortName = _("Voicemail settings")
	newObjectTitle = _("Voicemail settings")
	
	def createVariables(self):
		self.variables = [
				 VarType("enable", title=_("Enable Voicemail on phones"), type="bool", default=True),
				 VarType("recording", title=_("Recording settings"), type="label"),
				 VarType("format", title=_("File format for voicemail messages"), type="choice",
								   options=[('wav49',_('WAV (common sound format)')),('gsm',_('GSM (smaller)'))], default="wav49"),
				 VarType("maxmessage", title=_("Maximal message length (in seconds)"), type="int", default=180, len=3),
				 VarType("minmessage", title=_("Minimal message length (in seconds)"), type="int", default=2, len=3),
				 VarType("maxsilence", title=_("Seconds of silence to end the recording"), type="int", default=2, len=2),
				 VarType("silencethreshold", title=_("Silence threshold (what we consider silence, the lower, the more sensitive)"), type="int", default=150, len=2),
	
				 VarType("playback", title=_("Playback settings"), type="label"),
				 VarType("maxlogins", title=_("Max number of failed login attempts"), type="int", default=3, len=2),
				 VarType("skipms", title=_("Seconds to skip forward/backward"), type="int", default=3, len=2),
	
				 VarType("emailsettings", title=_("E-mail integration settings"), type="label"),
				 VarType("emailintegration", title=_("Activate email voicemail notifications?"), type="bool"),
				 VarType("serveremail", title=_("Who the e-mail notification should appear to come from"), hint=_("destar_pbx@yourdomain"), optional=True, len=30),
				 VarType("fromstring", title=_("Change the From: string"), default=_("The Asterisk/DeStar PBX"), optional=True, len=50),
				 VarType("emailsubject", title=_("Change email Subject"), default=_("[DeStar PBX]: New message from ${VM_CALLERID} in mailbox ${VM_MAILBOX}"), optional=True, len=80),
				 VarType("emailbody", title=_("Change email Body"), type="text", 
					default=_("Dear ${VM_NAME}:\\n\\n\\tjust wanted to let you know you were just left a ${VM_DUR} long message (number ${VM_MSGNUM})\\n\\tin mailbox ${VM_MAILBOX} from ${VM_CALLERID}, on ${VM_DATE}, so you might\\n\\twant to check it when you get a chance. Thanks!\\n\\n\\t\\t\\t--Asterisk/Destar PBX."), 
					optional=True),
				 VarType("attach", title=_("Should the email contain the voicemail as an attachment?"), type="bool"),
				 VarType("mailcmd", title=_("Override the default program to send e-mail"), hint=_("i.e.: /usr/sbin/sendmail -t"), optional=True),
	
				# pbxskip=yes
				# charset=iso-8859-1
				]

	def createAsteriskConfig(self):
		c = AstConf("voicemail.conf")
        	c.setSection("general")
		c.appendValue(self, "format")
		c.appendValue(self, "maxmessage")
		c.appendValue(self, "minmessage")
		c.appendValue(self, "maxsilence")
		c.appendValue(self, "silencethreshold")
		c.appendValue(self, "maxlogins")
		c.append("skipms=%d" % (self.skipms * 1000))
		c.append("operator=yes")
		
		if self.enable:
			needModule("res_adsi")
			needModule("app_voicemail")

		if self.emailintegration and self.serveremail:
			c.appendValue(self,"serveremail")
			if self.fromstring:
				c.appendValue(self,"fromstring")
			if self.emailsubject:
				c.appendValue(self,"emailsubject")
			if self.emailbody:
				emailbody = self.emailbody.replace("\n","\\n")
				emailbody = emailbody.replace("\t","\\t")
				c.append("emailbody=%s" % emailbody)
			if self.attach:
				c.append("attach=yes")
			if self.mailcmd:
				c.appendValue(self,"mailcmd")

		c.setSection("zonemessages")
		# TODO: find out our own timezone somehow
		c.append("cest=Europe/Berlin,'vm-received' Q 'digits/at' k 'oclock' M")

