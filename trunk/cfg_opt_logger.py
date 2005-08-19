# -*- coding: iso-latin-1 -*-
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


class CfgOptLogger(CfgOptSingle):
	_opt = [('error',   _("Errors")),
	        ('warning', _("Warnings")),
	        ('notice',  _("Notifications")),
	        ('verbose', _("Verbose messages")),
	        ('debug',   _("Debug output")),
	      ]

	facility_options = ("","auth", "authpriv", "cron", "daemon",
		"ftp", "kern", "lpr", "mail",
	 	"mark", "news", "security", "syslog",
	 	"user", "uucp", "local0", "local1",
	 	"local2", "local3", "local4", "local5",
		"local6", "local7")

	shortName   = _("Logger options")
	description = _("Asterisk can emit many events to it's console or a log file, Here you can make it more (or less) verbose:")
	variables   = [VarType("console",
				title=_("Console output"),
				type="mchoice",
				options=_opt,
				optional=True,
				default="error,warning,notice,verbose"),
		       VarType("messages",
				title=_("Output in /var/log/asterisk/messages"),
				type="mchoice",
				options=_opt,
				optional=True,
				default="error,warning"),
		       VarType("facility",
				title=_("Log to syslog via facility"),
				type="choice",
				optional=True,
				options=zip(facility_options, facility_options)),
		       VarType("syslog",
				title=_("What kind of messages to log"),
				type="mchoice",
				options=_opt,
				optional=True,
				default="error,warning")]

	def createAsteriskConfig(self):
		c = AstConf("logger.conf")
		c.setSection("general")
		c.append("dateformat=%y%m%d-%H%M%S")

		c.setSection("logfiles")
		c.appendValue(self, "console")
		c.appendValue(self, "messages")

		if self.facility:
			c.append("syslog.%s=%s" % (self.facility, self.syslog))
