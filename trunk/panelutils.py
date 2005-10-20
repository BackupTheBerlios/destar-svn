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
import backend, manager
from configlets import *

EXT_APPS_CFG = "ext_cfg.py"


def check_dir (dir):
	op_panel = {}
	op_panel["flash"] = "%s/html/operator_panel.swf" % dir
	op_panel["server"] = "%s/op_server.pl" % dir
	op_panel["serv_cfg"] = "%s/op_server.cfg" % dir
	try:
		for file in op_panel.values():
			open(file)
		check = 1
	except IOError, (errno, strerror):
		check = 0
	return check

def copy_files_to_webserver (dir):
	try:
		os.mkdir("%s/static/panel" % os.getcwd())
	except OSError:
		pass
	for file in os.listdir("%s/html" % dir):
		try:
			src = "%s/html/%s" % (dir,file)
			dst = "%s/static/panel/%s" % (os.getcwd(),file)
			open(dst,"w").write(open(src).read())
		except IOError:
			return 0
	return 1

def change_conf (dir, code, name, mgr_name):
	for mgr in backend.getConfiglets(name="CfgOptManager"):
		if mgr.name == mgr_name:
			secret = mgr.secret
	try:
		conf =  open("%s/op_server.cfg" % dir,"r+")
		lines = conf.readlines()
		conf.seek(0)
		for line in lines:
			line = re.sub("(?<=manager_host=).*","localhost",line)
			line = re.sub("(?<=manager_user=).*",mgr_name,line)
			line = re.sub("(?<=manager_secret=).*",secret,line)
			line = re.sub("(?<=web_hostname=).*",name,line)
			line = re.sub("(?<=flash_dir=).*","%s/static/panel/" % os.getcwd(),line)
			line = re.sub("(?<=security_code=).*",code,line)
			line = re.sub("(?<=conference_context=).*","apps",line)
			conf.write(line)
		setConfigured(dir)
	except IOError:
		return -1
	return 1

def isConfigured ():
	"""Return a value depending on the panel configuration file."""

	ret = 0		# return 0 if there is not matching line
	try:
		f = open(EXT_APPS_CFG)
		for l in f.readlines():
			if re.match("\s*oppanel_configured\s*=\s*1\s*$",l):
				ret = 1
			if re.match("\s*oppanel_configured\s*=\s*0\s*$",l):
				ret = -1 	# -1 if there is a mtaching line with 0
		f.close()
	except IOError:
		pass
	return ret

def getDir():
	ret = None
	try:
                f = open(EXT_APPS_CFG)
                for l in f.readlines():
                        m = re.match("\s*oppanel_dir\s*=\s*(\S*)\s*$",l)
			if m:
				ret = m.group(1)
                f.close()
        except IOError:
                pass
        return ret


def setConfigured (dir):
	conf = isConfigured()
	if conf == 1:
		return
	elif conf == -1:
		try:
			lines = open(EXT_APPS_CFG).readlines()
			f = open(EXT_APPS_CFG,'w')
			for l in lines:
				if re.match("\s*oppanel_configured\s*=\s*0\s*$",l):
					l = l.replace('0','1')
				f.write(l)
			f.close()
		except IOError:
			pass
	elif conf == 0:
		try:
			f = open(EXT_APPS_CFG,'a')
			f.write("oppanel_configured=1\n")
			f.write("oppanel_dir=%s\n" % dir )
			f.close()
		except IOError:
			pass
		
	
def unsetConfigured ():
	conf = isConfigured()
	if conf == 0 or conf == -1:
		return
	elif conf == 1:
		try:
			lines = open(EXT_APPS_CFG).readlines()
			f = open(EXT_APPS_CFG,'w')
			for l in lines:
				if re.match("\s*oppanel_configured\s*=\s*1\s*$",l):
					l = l.replace("1","0")
				f.write(l)
			f.close()
		except IOError:
			pass

def fixup():
	backend.fixupConfiglets()

def createExtButton(self):
	p = AstConf("op_buttons.cfg")
	p.setSection("%s/%s" % (self.technology, self.name) )
	p.append("Position=n")
	p.append("Icon=1")
	p.append("Extension=%s" % self.ext)
	p.append("Label=%s" % self.name)

def createTrunkButton(self):
	p = AstConf("op_buttons.cfg")
	p.setSection("%s/%s" % (self.technology, self.channel) )
	p.append("Position=n")
	p.append("Icon=2")
	p.append("Extension=-1")
	p.append("Label=%s" % self.name)

def createMeetmeButton(self):
	p = AstConf("op_buttons.cfg")
	p.setSection(self.confno)
	p.append("Position=n")
	p.append("Icon=5")
	p.append('Label="%s %s"' % (_("Meetme"),self.confno))

def createParkButton(self):
	p = AstConf("op_buttons.cfg")
	p.setSection("%s%s" % (_("PARK"),self.ext))
	p.append("Position=n")
	p.append("Icon=3")
	p.append("Extension=%s" % self.ext)
	p.append('Label="%s %s"' % (_("Park"),self.ext))

def createQueueButton(self):
	p = AstConf("op_buttons.cfg")
	p.setSection(self.name)
	p.append("Position=n")
	p.append("Icon=3")
	p.append("Extension=-1")
	p.append("Label=%s" % self.name)

def startPanelDaemon():
        os.popen('%s/op_server.pl -d' % getDir())

def stopPanelDaemon():
        commands.getoutput('killall op_server.pl')

def restartPanelDaemon():
	stopPanelDaemon()
	startPanelDaemon()

def moveButFile():
	buttons_file =  "%s/op_buttons.cfg" % CONF_DIR
	try:
		if os.access(buttons_file, os.F_OK):
			shutil.move(buttons_file, getDir())
	except:
		print "Can't move the op_buttons.cfg file. Check permissions"

if isConfigured():
	print _("Starting the panel daemon ..")
	startPanelDaemon()

