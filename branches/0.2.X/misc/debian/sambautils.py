# -*- coding: iso-latin-1 -*-
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

SAMBA_RELOAD_CMD = "sudo /etc/init.d/samba reload"
USERADD_CMD = "sudo adduser"
USERDEL_CMD = "sudo userdel"
SMBPASSWD_CMD = "sudo smbpasswd"

def reloadDaemon():
        return commands.getoutput(SAMBA_RELOAD_CMD)

def setPassword(user, pswd):
	(stat, out) = commands.getstatusoutput("id %s" % user)
	if stat:
		os.popen("%s --system %s" % (USERADD_CMD, user) )
		os.popen("%s %s asterisk" % (USERADD_CMD, user) )
			
	p = os.popen("%s -s -a %s" % (SMBPASSWD_CMD, user), 'w')
	p.write(pswd+"\n")
	p.write(pswd+"\n")

def deleteUser(name):
	os.popen("%s -x %s" % (SMBPASSWD_CMD, name) )
	os.popen("%s %s" % (USERDEL_CMD, name) )
	
