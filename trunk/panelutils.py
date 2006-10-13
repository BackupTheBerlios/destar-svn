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

import os, re, commands, shutil
import backend
from configlets import *

# To use with asternic.org op_panel tarball:
#PANEL_CONF_DIR	= "/usr/local/op_panel"
#PANEL_HTML_DIR	= "/usr/local/op_panel/html"
#PANEL_START_CMD	= "/usr/local/op_panel/op_server.pl -d"
#PANEL_STOP_CMD	= "pkill op_server"


# Configuration to use with op-panel .deb package:
PANEL_CONF_DIR	= "/etc/op-panel"
PANEL_HTML_DIR	= "/usr/share/op-panel/flash"
PANEL_RESTART_CMD = "/etc/init.d/op-panel restart"

def isConfigured ():
	import configlets
	configured=0
	for obj in configlets.configlet_tree:
		if obj.__class__.__name__ == 'CfgOptOPPanel':                                
			configured=1
			continue
	return configured

def createManagerConfig(obj):
	c = AstConf("op_server.cfg")
	c.setSection("general")
	c.append("manager_host=127.0.0.1")
	c.append("manager_user=%s" % obj.manager)
	manager = backend.getConfiglet(name=obj.manager)
	c.append("manager_secret=%s" % manager.secret)

def createDefaultConfig(c):
	c.append("flash_dir=%s" % PANEL_HTML_DIR)
	#TODO: put some of the following on cfg_opt_oppanel.py
	c.append("auth_md5=1")
	c.append("poll_voicemail=0")
	c.append("kill_zombies=0")
	c.append("debug=0")
	c.append("conference_context=apps")
	c.append("clid_format=(xxx)xxx-xxxx")
	c.append("clid_privacy=0")
	c.append("show_ip=0")
	c.append("rename_label_agentlogin=0")
	c.append("rename_label_callbacklogin=0")
	c.append("rename_label_wildcard=0")
	c.append("rename_to_agent_name=1")
	c.append("agent_status=1")
	c.append("rename_queue_member=0")
	c.append("change_led_agent=1")
	c.append("reverse_transfer=0")
	c.append("clicktodial_insecure=0")
	c.append('transfer_timeout="%s"' % _("0,No timeout|300,5 minutes|600,10 minutes|1200,20 minutes|2400,40 minutes|3000,50 minutes"))
	c.append("enable_restart = 0")

def createExtButton(obj):
	p = AstConf("op_buttons.cfg")
	p.setSection("%s/%s" % (obj.technology, obj.name) )
	p.append("Position=n")
	p.append("Icon=1")
	p.append("Extension=%s" % obj.ext)
	p.append("Label=%s" % obj.name)

def createTrunkButton(obj):
	p = AstConf("op_buttons.cfg")
	p.setSection("%s/%s" % (obj.technology, obj.name) )
	p.append("Position=n")
	p.append("Icon=2")
	p.append("Extension=-1")
	p.append("Label=%s" % obj.name)

def createMeetmeButton(obj):
	p = AstConf("op_buttons.cfg")
	p.setSection(obj.confno)
	p.append("Position=n")
	p.append("Icon=5")
	p.append('Label="%s %s"' % (_("Meetme"),obj.confno))

def createParkButton(obj):
	p = AstConf("op_buttons.cfg")
	p.setSection("%s%s" % (_("PARK"),obj.ext))
	p.append("Position=n")
	p.append("Icon=3")
	p.append("Extension=%s" % obj.ext)
	p.append('Label="%s %s"' % (_("Park"),obj.ext))

def createQueueButton(obj):
	p = AstConf("op_buttons.cfg")
	p.setSection(obj.name)
	p.append("Position=n")
	p.append("Icon=3")
	p.append("Extension=-1")
	p.append("Label=%s" % obj.name)

def restartPanelDaemon():
	s = []
	s.append(_("Restarting the panel daemon ..."))
        commands.getoutput(PANEL_RESTART_CMD)
	return s

if isConfigured():
	restartPanelDaemon()

