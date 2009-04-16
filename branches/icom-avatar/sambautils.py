# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Diego Andrés Asenjo
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

import os, commands

SAMBA_RESTART_CMD = "/etc/init.d/samba reload"

def restartDaemon():
        return commands.getoutput(SAMBA_RESTART_CMD)

def setPassword(user, pswd):
	(stat, out) = commands.getstatusoutput("id %s" % user)
	if stat:
		os.popen("useradd %s" % user)
			
	p = os.popen("smbpasswd -s -a %s" % user, 'w')
	p.write(pswd+"\n")
	p.write(pswd+"\n")

def deleteUser(name):
	os.popen("smbpasswd -x %s" % name)
	os.popen("userdel %s" % name)
	
