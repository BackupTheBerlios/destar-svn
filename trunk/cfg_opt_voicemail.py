# -*- coding: iso-latin-1 -*-
#
# Copyright (C) 2004 by Holger Schurig
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
	variables = [VarType("recording", title=_("Recording settings"), type="label"),
		     VarType("format", title=_("File format for voicemail messages"), type="choice", options=[('wav49','WAV (common sound format)'),('gsm','GSM (smaller)')], default="wav49"),
		     VarType("maxmessage", title=_("Maximal message length (in seconds)"), type="int", default=180, len=3),
		     VarType("minmessage", title=_("Minimal message length (in seconds)"), type="int", default=2, len=3),
		     VarType("maxsilence", title=_("Seconds of silence to end the recording"), type="int", default=2, len=2),
		     VarType("silencethreshold", title=_("Silence threshold (what we consider silence, the lower, the more sensitive)"), type="int", default=150, len=2),

		     VarType("playback", title=_("Playback settings"), type="label"),
		     VarType("maxlogins", title=_("Max number of failed login attempts"), type="int", default=3, len=2),
		     VarType("skipms", title=_("Seconds to skip forward/backward"), type="int", default=3, len=2),

			# E-Mail settings:
			# serveremail=asterisk@somedomain
			# fromstring=Some subject
			# emailsubject
			# emailbody
			# mailcmd
			# pbxskip=yes
			# attach=yes
			# charset=iso-8859-1
		    ]

	def createAsteriskConfiglet(self):
		c = AstConf("voicemail.conf")
        	c.setSection("general")
		c.appendValue(self, "format")
		c.appendValue(self, "maxmessage")
		c.appendValue(self, "minmessage")
		c.appendValue(self, "maxsilence")
		c.appendValue(self, "silencethreshold")
		c.appendValue(self, "maxlogins")
		c.append("skipms=%d" % (self.skipms * 1000))

		c.setSection("zonemessages")
		# TODO: find out our own timezone somehow
		c.append("cest=Europe/Berlin|'vm-received' Q 'digits/at' k 'oclock' M")

