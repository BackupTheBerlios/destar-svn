# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Holger Schurig, some addons by Michael Bielicki, TAAN Softworks Corp.
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


import os
from config import *
import language
import configlets
import commands
import re


frontend_sessions = 0

def add_session():
	global frontend_sessions
	frontend_sessions += 1
	
def del_session():
	global frontend_sessions
	frontend_sessions -= 1
####################################################################################
#
# We start with functions that work on the configuration file level:
#


__loaded = False


def loadPythonConfig():
	"""This loads the destar_cfg.py config file either from
	/etc/asterisk or from the current directory."""


	global __loaded

	# Forget all config options
	configlets.configlet_tree = configlets.ConfigletTree()

	# Try to read destar_cfg.py from Asterisk directory
	# if this doesn't work, read it from current directory
	fn = os.path.join(configlets.CONF_DIR,DESTAR_CFG)
	try:
		try:
			reload(sys)
			sys.setdefaultencoding('utf-8')
			execfile(fn)
		except IOError:
			try:
				execfile(DESTAR_CFG)
			except IOError:
				print _("Warning: There is no %s or %s file yet." % (fn,DESTAR_CFG))
	except NameError:
		pass
		
	fixupConfiglets()
	__loaded = True

def fixupConfiglets():
	configlets.varlist_manager.updateTrunks()
	configlets.varlist_manager.updateDialouts()
	for obj in configlets.configlet_tree:
		obj.createVariables()
	for obj in configlets.configlet_tree:
		obj.fixup()
		obj.createDependencies()

def createPythonConfig(f=None):
	"""This writes /etc/asterisk/destar_cfg.py.

	The output will be written into file hand 'f' if you provide one.
	Use this for debugging, like this:

		import sys
		createPythonConfig(sys.stdout)
	"""

	if configlets.configlet_tree.empty():
		return
	
	fixupConfiglets()

	if f is None:
		f = open(os.path.join(configlets.CONF_DIR,DESTAR_CFG),"w")

	f.write("# -*- coding: utf-8 -*-\n")
	f.write("# You should execfile() this config\n\n")
	for c in configlets.configlet_tree:
		a = c.createPythonConfig()
		for s in a:
                        try:
                                f.write("%s\n" % s.encode('utf-8'))
                        except:
                                f.write("%s\n" % s)



def initializeAsteriskConfig():
	"""This puts some hard coded default values into some asterisk
	config files:

	* adsi.conf
	* extconfig.conf
	* extensions.conf
	* sip.conf
	* iax.conf
	* chan_dahdi.conf
	* macros.inc
	"""

	tapisupport = False
        for obj in configlets.configlet_tree:
	        if obj.__class__.__name__ == 'CfgOptSettings':
		        if obj.tapi:
			        tapisupport = True

	# Start with empty config files
	configlets.asterisk_configfiles = []


	c = AstConf("adsi.conf")
	c.setSection("intro")
	c.append("greeting => Welcome to DeStar")



	c = AstConf("extconfig.conf")
	c.setSection("settings")
	c.append("")


	c = AstConf("extensions.conf")
	c.append("static=yes")
	c.append("writeprotect=yes")
	c.append('#include "macros.inc"')

	c.setSection("default")
	c.append("; This context should not be used directly")
	c.appendExten("s","Hangup")
	c.appendExten("i","Hangup")

	c = AstConf("sip.conf")
	c.append("language=%s" % getSetting('language', 'en'))
	c.append("maxexpiry=3600")
	c.append("defaultexpiry=120")
	c.append("disallow=all")
	c.append("limitonpeers=yes")
	c.append("t38pt_udptl = yes")

	c = AstConf("iax.conf")
	c.append("language=%s" % getSetting('language', 'en'))


	c = AstConf("chan_dahdi.conf")
	c.setSection("channels")
	c.append("language=%s" % getSetting('language', 'en'))
	c.append("immediate=no")
	c.append("overlapdial=yes")
	
	c = AstConf("op_server.cfg")
	c.setSection("general")
	c.append("language=%s" % getSetting('language', 'en'))

	needModule("pbx_functions")
	needModule("cdr_sqlite3_custom")
	c = AstConf("cdr_sqlite3_custom.conf")
	c.setSection("master")
	c.append("table => cdr")
	c.append("columns => clid,src,dst,dcontext,channel,dstchannel,lastapp,lastdata,start,answer,end,duration,billsec,disposition,amaflags,accountcode,uniqueid,userfield,pbx,intrunk,outtrunk,dialout")
	c.append("values => '${CDR(clid)}','${CDR(src)}','${CDR(dst)}','${CDR(dcontext)}','${CDR(channel)}','${CDR(dstchannel)}','${CDR(lastapp)}','${CDR(lastdata)}','${CDR(start)}','${CDR(answer)}','${CDR(end)}','${CDR(duration)}','${CDR(billsec)}','${CDR(disposition)}','${CDR(amaflags)}','${CDR(accountcode)}','${CDR(uniqueid)}','${CDR(userfield)}','${CDR(pbx)}','${CDR(intrunk)}','${CDR(outtrunk)}','${CDR(dialout)}'")

	needModule("res_indications")
	c = AstConf("macros.inc")
	c.append(";")
	c.append("; Macro to dial a standard local extension")
	c.append(";")
	c.append("; format: Macro(stdexten,dest,ext,pbx)")
	c.append(";")
	c.setSection("macro-dial-std-exten")
	c.append(";")
	c.append("; test for CF count")
	c.append('exten=s,1,GotoIf($[${cf_count} >= 2]?nocf:cfim)')
	c.append("exten=s,n(nocf),Goto(hangup)")
	c.append("; test for CFIM (Call Forwarding Immediate)")
	c.append("exten=s,n(cfim),Set(fw_ext=${DB(CFIM/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${fw_ext}" != ""]?fw)')
	c.append(";")
	c.append("; test for VMIM (VM Immediate)")
	c.append("exten=s,n,Set(vmim=${DB(VMIM/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${vmim}" != ""]?vmu)')
	c.append(";")
	c.append("; test for DND (Do Not Disturb)")
	c.append("exten=s,n,Set(dnd=${DB(DND/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${dnd}" != ""]?busy)')
	c.append(";")
	c.append("; get dial seconds")
	c.append("exten=s,n,Set(dsec=${DB(DSEC/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${dsec}" != ""]?dsecEnd)')
	c.append("exten=s,n,Set(dsec=25)")
	c.append("exten=s,n(dsecEnd),NoOp()")
	c.append(";")
	c.append("; get global dial options")
	c.append("exten=s,n,Set(dopt=${DIAL_OPTIONS})")
        if tapisupport:
	        c.append("exten=s,n,Set(dopt=${dopt}M(tapi^${UNIQUEID},${ARG1}))")
	c.append(";")
	c.append("; get early media")
	c.append("exten=s,n,Set(emedia=${DB(EMEDIA/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${emedia}" = ""]?emediaEnd)')
	c.append("exten=s,n,Set(dopt=${dopt}m(${emedia}))")
	c.append("exten=s,n,Answer()")
	c.append("exten=s,n(emediaEnd),NoOp()")
	c.append(";")
	c.append("; parallel ringing")
	c.append("exten=s,n,Set(prng=${DB(PRNG/${ARG4}/${ARG3})})")
	c.append(";")
	c.append("; Dial")
	c.append("exten=s,n(dialstart),NoOp()")
        if tapisupport:
                c.append("exten=s,n,UserEvent(TAPI,TAPIEVENT: LINE_NEWCALL ${ARG1})")
                c.append("exten=s,n,UserEvent(TAPI,TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_OFFERING)")
                c.append("exten=s,n,UserEvent(TAPI,TAPIEVENT: SET CALLERID ${CALLERID})")
                c.append("exten=s,n,UserEvent(TAPI,TAPIEVENT: LINE_CALLINFO LINECALLINFOSTATE_CALLERID)")
	if VICIDIAL_INTEGRATION:
		c.append("exten=s,n(MainDial),AGI(call_inbound.agi,${ARG1}-----${CALLERID}-----${CDR(intrunk)}-----x-----y-----z-----w)")
		c.append("exten=s,n,Dial(${ARG1}${prng},${dsec},TtWwr${dopt})")
	else:
		c.append("exten=s,n(MainDial),Dial(${ARG1}${prng},${dsec},TtWwr${dopt})")
	c.append(";")
	c.append("; Dial result was 'timeout'")
	c.append("exten=s,n(dialtimeout),Set(fw_ext=${DB(CFTO/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${fw_ext}" != ""]?fw)')
	c.append('exten=s,n,GotoIf($["${CDR(intrunk)}" = ""]?cftoend)')
	c.append("exten=s,n,Set(fw_ext=${DB(CFTO-TRUNK/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${fw_ext}" != ""]?fw)')
	c.append("exten=s,n(cftoend),NoOp()")
	c.append(";")
	c.append("; no CFTO (Call Forward Timeout), test VM U.")
	c.append("exten=s,n,Set(vmu=${DB(VMU/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${vmu}" != ""]?vmu)')
	c.append("exten=s,n,Goto(hangup)")
	c.append(";")
	c.append("; Dial result was 'busy'")
	c.append("exten=s,MainDial+101(busy),Set(fw_ext=${DB(CFBS/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${fw_ext}" != ""]?fw)')
	c.append('exten=s,n,GotoIf($["${CDR(intrunk)}" = ""]?cfbsend)')
	c.append("exten=s,n,Set(fw_ext=${DB(CFBS-TRUNK/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${fw_ext}" != ""]?fw)')
	c.append("exten=s,n(cfbsend),NoOp()")
	c.append(";")
	c.append("; no CFBS (Call Forward Busy), test VM Busy")
	c.append("exten=s,n,Set(vmbs=${DB(VMBS/${ARG4}/${ARG3})})")
	c.append('exten=s,n,GotoIf($["${vmbs}" != ""]?vmbs)')
	c.append("exten=s,n,Answer()")
	c.append("exten=s,n,PlayTones(busy)")
	#c.append("exten=s,n,Busy()")
	c.append("exten=s,n,Hangup()")
	c.append(";")
	c.append("exten=s,n(fw),Set(cf_count=$[${cf_count} + 1])")
	c.append("exten=s,n,Set(CALLERID(num)=${CALLERID(num)}-${ARG3})")
	c.append("exten=s,n,Goto(real-${ARG2},${fw_ext},1)")
	c.append(";")
	c.append('exten=s,n(vmu),Set(vmopt=u)')
	c.append("exten=s,n,Macro(voicemail,${ARG3},${ARG4},${vmopt})")
	c.append(";")
	c.append('exten=s,n(vmbs),Set(vmopt=b)')
	c.append("exten=s,n,Macro(voicemail,${ARG3},${ARG4},${vmopt})")
	c.append(";")
	c.append("exten=s,n(hangup),Hangup()")
	c.append(";")
	c.append("exten=i,0,Hangup")
        if tapisupport:
                c.append("exten=h,1,UserEvent(TAPI,TAPIEVENT: LINE_CALLSTATE LINECALLSTATE_IDLE)")

                c.append("[macro-tapi];")
                c.append("exten=s,1,UserEvent(TAPI,TAPIEVENT: [~${ARG1}&${ARG2}] LINE_CALLSTATE LINECALLSTATE_CONNECTED)")
                c.append("exten=s,2,UserEvent(TAPI,TAPIEVENT: [~${ARG1}&!${ARG2}] LINE_CALLSTATE LINECALLSTATE_HANGUP)")

	c.append(";")
	c.append("; format: Macro(voicemail,<VoiceMail arguments>,PBX)")
	c.append(";")
	c.setSection("macro-voicemail")
	c.append("exten=o,1,Goto(${ARG2},0,1)")
	c.append("exten=a,1,Goto(${ARG2},0,1)")
	c.append("exten => t,1,Hangup()")
	c.append("exten => T,1,Hangup()")
	c.append("exten => s,1,Answer")
	c.append("exten => s,2,Set(TIMEOUT(absolute)=7200)")
	c.append("exten => s,3,Wait(1)")
	c.append("exten => s,4,VoiceMail(${ARG1}@${ARG2},${ARG3})")
	c.append("exten => s,5,Hangup()")

	c.append(";")
	c.append("; format: Macro(sendfax,filename,waittime)")
	c.append(";")
	needModule("app_fax")
	context="macro-sendfax"
	context="faxout"
	c.setSection(context)
	c.appendExten("s", "Answer()", context)
	c.appendExten("s", "Wait(${ARG2})", context)
	c.appendExten("s", "Set(LOCALSTATIONID=%s)" getSetting('header_text', 'DeStar PBX'), context)
	c.appendExten("s", "SendFAX(${FAXFILE})", context)
	c.appendExten("s", "Hangup", context)
	c.appendExten("h", "NoOp(TX: REMOTESTATIONID is ${REMOTESTATIONID})", context)
	c.appendExten("h", "UserEvent(FAX|SEND: Call ended normally)", context)


	c.append(";")
	c.append("; format: Macro(call-forward,type,pbx,destination,message-to-play)")
	c.append(";")
	context="macro-call-forward"
	c.setSection(context)
	c.appendExten("s", "Answer()", context)
	c.appendExten("s", "Set(DB(${ARG1}/${ARG2}/${CALLERID(num)})=${ARG3})", context)
	c.appendExten("s", "Set(DB(${ARG1}_LASTNUM/${ARG2}/${CALLERID(num)})=${ARG3})", context)
	c.appendExten("s", "Playback(${ARG4})", context)
	c.appendExten("s", "Playback(has-been-set-to)", context)
	c.appendExten("s", "SayDigits(${ARG3})", context)
	c.appendExten("s", "Wait(1)", context)
	c.appendExten("s", "Playback(vm-goodbye)", context)
	c.appendExten("s", "Hangup", context)

	c.append(";")
	c.append("; format: Macro(call-forward-warning,destination,message-to-play)")
	c.append(";")
	context="macro-call-forward-warning"
	c.setSection(context)
	c.appendExten("s", "Answer()", context)
	c.appendExten("s", "Playback(${ARG2})", context)
	c.appendExten("s", "Playback(has-been-set-to)", context)
	c.appendExten("s", "SayDigits(${ARG1})", context)

	c.append(";")
	c.append("; format: Macro(record,filename,format,maxduration)")
	c.append(";")
	c.setSection("macro-record")
	c.append("exten => s,1,Answer")
	c.append("exten => s,n,Wait(1)")
	c.append("exten => s,n,Playback(vm-message)")
	c.append("exten => s,n,Playback(is-now-being-recorded)")
	c.append("exten => s,n,Playback(after-the-tone)")
	c.append("exten => s,n,Record(${ARG1}.${ARG2},1,${ARG3})")
	c.append("exten => s,n,Playback(vm-message)")
	c.append("exten => s,n,Playback(recorded)")

	c.append(";")
	c.append("; format: Macro(dial-result,[<cause>])")
	c.append(";")
	c.setSection("macro-dial-result")
	c.append("exten => s,1,Set(TIMEOUT(absolute)=35)")
	c.append("exten => s,2,GotoIf($[foo${ARG1} != foo]?cause_${ARG1},1:cause_${HANGUPCAUSE},1)")

	c.append("; undefined error (mostly when an existing extension is currently unavailable)")
	c.append("exten => _cause_0,1,Answer")
	c.append("exten => _cause_0,2,Wait(1)")
	c.append("exten => _cause_0,3,Playback(the-number-u-dialed,skip)")
	c.append("exten => _cause_0,4,Playback(is-curntly-unavail,skip)")
	c.append("exten => _cause_0,5,Playback(pls-try-call-later,skip)")
	c.append("exten => _cause_0,6,Wait(3)")
	c.append("exten => _cause_0,7,Goto(3)")

	c.append("; normal call clearing")
	c.append("exten => _cause_1,1,Hangup")

	c.append("; extension currently busy")
	c.append("exten => _cause_2,1,Answer")
	c.append("exten => _cause_2,2,PlayTones(busy)")
	c.append("exten => _cause_2,3,Wait(40)")
	c.append("exten => _cause_2,4,Goto(2)")

	c.append("; something failed")
	c.append("exten => _cause_3,1,Answer")
	c.append("exten => _cause_3,2,PlayTones(info)")
	c.append("exten => _cause_3,3,Wait(2)")
	c.append("exten => _cause_3,4,Playback(an-error-has-occured,skip)")
	c.append("exten => _cause_3,5,Playback(pls-try-call-later,skip)")
	c.append("exten => _cause_3,6,Wait(2)")
	c.append("exten => _cause_3,7,Goto(2)")

	c.append("; congestion")
	c.append("exten => _cause_4,2,Congestion")

	c.append("; unassigned number")
	c.append("exten => _cause_5,1,Answer")
	c.append("exten => _cause_5,2,PlayTones(info)")
	c.append("exten => _cause_5,3,Wait(2)")
	c.append("exten => _cause_5,4,Playback(ss-noservice,skip)")
	c.append("exten => _cause_5,5,Wait(2)")
	c.append("exten => _cause_5,6,Goto(2)")

	c.append("; unallowed number")
	c.append("exten => _cause_99,1,Answer")
	c.append("exten => _cause_99,2,PlayTones(info)")
	c.append("exten => _cause_99,3,Wait(2)")
	c.append("exten => _cause_99,4,Playback(discon-or-out-of-service,skip)")
	c.append("exten => _cause_99,5,Wait(2)")
	c.append("exten => _cause_99,6,Goto(2)")

	c.append("; unauthorized extension")
	c.append("exten => _cause_100,1,Answer")
	c.append("exten => _cause_100,2,PlayTones(info)")
	c.append("exten => _cause_100,3,Wait(2)")
	c.append("exten => _cause_100,6,Playback(your-extension,skip)")
	c.append("exten => _cause_100,7,Playback(not-yet-assigned,skip)")
	c.append("exten => _cause_100,8,Playback(please-contact-tech-supt,skip)")
	c.append("exten => _cause_100,9,Wait(2)")
	c.append("exten => _cause_100,10,Goto(2)")

	c.append("; all other errors")
	c.append("exten => _cause_X.,1,Answer")
	c.append("exten => _cause_X.,2,PlayTones(info)")
	c.append("exten => _cause_X.,3,Wait(2)")
	c.append("exten => _cause_X.,4,Playback(an-error-has-occured,skip)")
	c.append("exten => _cause_X.,5,Playback(error-number,skip)")
	c.append("exten => _cause_X.,6,GotoIf($[foo${ARG1} != foo]?7:11)")
	c.append("exten => _cause_X.,7,SayNumber(${ARG1})")
	c.append("exten => _cause_X.,8,Wait(1)")
	c.append("exten => _cause_X.,9,Playback(please-contact-tech-supt,skip)")
	c.append("exten => _cause_X.,10,Goto(14)")
	c.append("exten => _cause_X.,11,SayNumber(${HANGUPCAUSE})")
	c.append("exten => _cause_X.,12,Wait(1)")
	c.append("exten => _cause_X.,13,Playback(please-contact-tech-supt,skip)")
	c.append("exten => _cause_X.,14,Wait(2)")
	c.append("exten => _cause_X.,15,Goto(2)")
	c.append("exten => T,1,PlayTones(congestion)")
	c.append("exten => T,2,Wait(5)")
	c.append("exten => T,3,Hangup")

	if SAMBA_ENABLED:
		c = AstConf("smb.conf")
		c.setSection("global")
		c.append("workgroup = DeStarPBX")
		c.append("server string = DeStarPBX")
		c.append("log file = /var/log/samba/log.%m")
		c.append("security = user")
		c.append("socket options = TCP_NODELAY SO_RCVBUF=8192 SO_SNDBUF=8192")


def createAsteriskConfig():
	"""This creates all the Asterisk config files in /etc/asterisk.

	First, we create an in-memory representation of all config files
	to create. Then we check if any of the config files is already
	in use, but not by Asterisk. We make a backupof all file names 
	that cannot be overwritten.

	Only when all config files are safe to write, we creat all of
	them at once."""


	if not __loaded: loadPythonConfig()

	createPythonConfig()
	
	if configlets.configlet_tree.empty():
		return [] 
	initializeAsteriskConfig()
	# First write the options
	for c in configlets.configlet_tree:
		if isinstance(c, CfgOpt):
			c.createAsteriskConfig()
	# Then the rest
	for c in configlets.configlet_tree:
		if not isinstance(c, CfgOpt):
			c.createAsteriskConfig()

		
	available_modules = []
	missing_modules = []
	for f in os.listdir(ASTERISK_MODULES_DIR):
		if f.endswith('.so'): available_modules.append(f[:-3])
	c = AstConf("modules.conf")
	c.setSection("modules")
	c.append("autoload=no")
	for m in c.modules.preload:
		if not m in available_modules:
			missing_modules.append(m)
		else:
			c.append("preload=%s.so" % m)

	for sect in ("pbx", "codec", "format", "res", "cdr", "chan", "func", "app"):
		for m in c.modules[sect]:
			if not m in available_modules:
				missing_modules.append(m)
			else:
				c.append("load=%s.so" % m)

	# test if all config files are OK to be written or overwritten
	tmp_conf = []
	for fn,cnf in configlets.asterisk_configfiles:
		# system.conf can't have CONF_TAG at the top, so no need to search for it
		if os.path.exists(cnf.fn):
			f = open(cnf.fn, "r")
			s = f.readline()
			if s != configlets.CONF_TAG or fn == 'system.conf':
				# Backup file not created by us
				try:
					backupAsteriskConfig(fn)
				except OSError:
					print _("Error backing up %s") % fn 
		tmp_conf.append( (fn,cnf) )
	
	res=[]
	res.append(tmp_conf)
	res.append(missing_modules)

	return res 

def writeAsteriskConfig():
	# write all stuff out
	res = True
	for _fn,cnf in configlets.asterisk_configfiles:
		if _fn == 'op_server.cfg' and panelutils.isConfigured() != 1:
			continue
		try:
			cnf.write()
		except OSError:
			print _("Error writing up %s") % _fn 
			res = False
	return res


def backupAsteriskConfig(fn):
	"""This backs up one file. It get's a pure filename, say
	'extensions.conf' and looks into configlets.asterisk_configfiles for
	the in-memory-representation of it. There we have the full path
	name.

	Using this path name, we simple rename it from x.conf to
	x.conf.orig."""


	for short_fn,cnf in configlets.asterisk_configfiles:
		if fn==short_fn:
			os.rename(cnf.fn, "%s.orig" % cnf.fn)
			return True
	return False




####################################################################################
#
# The following functions work on the pure class definitions.
#
# They fish out the configlets by checking if they have the two members
# class.groupName and class.shortName. Only configlets that contains both of
# them are considered "ready for prime time", sheer descendance on Cfg isn't
# enought. That way CfgPerm, CfgPhone, CfgTrunk etc won't get listed.
#


def configletsList(grp=None):
	"""Returns a list of all configuration objects. We return
	the classes directly (not instantiations of the classes!):

	[ class MilliWattTest,
	  class EchoTest,
	  class IsdnCapiLine,
	  ...
	]

	When 'groupName' is specified, then only return configlets of this
	group."""


	res = []
	for s in globals():
		obj = globals()[s]
		try:
			g,n = obj.groupName, obj.shortName
			if grp and grp != g: continue
			res.append(obj)
		except AttributeError:
			pass
	return res
	



def configletsGrouped():
	"""Returns a list of all configuration objects, organized into groups:

	{ 'applications': [class MilliWattTest, class EchoTest, ...],
	  'options':      [class AsteriskOptions, class RtpOptions, ... ],
	  ...
	}
	"""

	res = {}
	for obj in globals():
		obj = globals()[obj]
		try:
			g,n = obj.groupName, obj.shortName
			res.setdefault(g,[]).append(obj)
		except AttributeError:
			pass
	return res




####################################################################################
#
# These functions work with actual instantiations of the configlets.
#
# Some of them are fairly simply, but are here to have very little backend
# functionality in Config.ptl or other frontend parts.
#
# **** TODO: This functions are no longer necessary, and now are used as stub
#            only


def newConfiglet(clazz):
	"""Create a new configlet with the class name 'clazz'. This new
	configlet is not added configlist.configlet_tree, you have to do
	this manually with addConfiglet()."""

	return globals()[clazz](autoAdd=False)




def addConfiglet(obj):
	"""Adds the configlet 'obj' to configlets.configlet_tree."""


	configlets.configlet_tree.addConfiglet(obj)



def updateConfiglet(obj):
	"""Updates the configlet 'obj' in configlets.configlet_tree."""


	configlets.configlet_tree.updateConfiglet(obj)



def deleteConfiglet(id):
	"""Deletes the configlet with index 'id' from configlets.configlet_tree."""


	configlets.configlet_tree.deleteConfiglet(int(id))




def moveConfigletUp(id):
	if not __loaded: loadPythonConfig()

	return configlets.configlet_tree.moveConfigletUp(id)



def moveConfigletDown(id):
	if not __loaded: loadPythonConfig()

	return configlets.configlet_tree.moveConfigletDown(id)

def countConfiglets(groupName=None, clazz=None):
	"Returns the count of all configlets in a given 'group'."


	if not __loaded: loadPythonConfig()
	if groupName is not None:
		return len(configlets.configlet_tree[groupName])
	if clazz is not None:
		return len(configlets.configlet_tree.getConfigletsByName(clazz))
	return len(configlets.configlet_tree)

def getConfiglets(group=None, name=None):
	"""Return a list of all configlets in a given 'group', with a given
	shortname or classname as defined in 'name'.

	Note that the short names are probably localized.

	Whenever we retrieve configlets, we're setting the attribute
	_id. You can use this id later with getConfiglet().
	"""


	if not __loaded: loadPythonConfig()
	
	result = []
	
	if group is not None: 
		result += configlets.configlet_tree.getConfigletsByGroup(group)
	if name is not None:
		result += configlets.configlet_tree.getConfigletsByName(name)
	return result



# TODO: examine the real utility of this three next functions

def getConfiglet(_id=None, name=None):
	"""This returns a configlet by the 'id'. The id is not set
	in stone, but is only valid from one getConfiglets() call
	to the next."""


	if not __loaded: loadPythonConfig()

	if name is not None:
		return configlets.configlet_tree.getConfigletByName(name)
	if _id is not None:
		return configlets.configlet_tree.getConfiglet(_id)


# Configlets can't import the Backend (because the Backend loads/imports
# the configlets. So we make this method manually known in the configlets module.
configlets.getConfiglet = getConfiglet


# FIXME: What an ugly function!!!
def getConfig(clazz, name, default=None):
	"""This searches for the first found configlet with the class
	'clazz'. If found, it looks if this configlet has the attribute name
	and returns it value or some default."""

	obj = configlets.configlet_tree.getConfigletsByName(clazz)
	if obj is not None and len(obj) > 0:
		obj = obj[0]
		return getattr(obj, str(name), default)
	return default

# Configlets can't import the Backend (because the Backend loads/imports
# the configlets. So we make this method manually known in the configlets module.
configlets.getConfig = getConfig

# FIXME: here is a mix of backend and frontend stuff, needs to be refactored
# FIXME: this is an ugly function too
def getChoice(clazz, key='name',val='name',sort=True):
	"""This is used to generate a list of tuples which we later use
	in the select widgets of type "choice" or "mchoice".

	'clazz' is the classname the configlet must have."""

	# TODO: this sould be changed for something like CheckConfig
	if not __loaded:
		loadPythonConfig()
	a = []
	n = 0
	try:
		obj2 = globals()[clazz]
	except KeyError:
		return a

	for obj in configlets.configlet_tree.getConfigletsByClass(obj2):
		a.append( (obj.__dict__[val], obj.__dict__[key]) )
		
	if a == [] :
		a.append( ('', '(None)') )
		
	if sort:
		a.sort()

	return a

configlets.__getChoice = getChoice



####################################################################################
#
# Functions to determine phone state
#

def lookupPhone(phones, channel):
	"""Searches for channel in phones[].channel()"""

	#print "lookupPhone", channel
	for p in phones:
		#print p.channelString()
		if channel==p.channelString():
			return p
	return None





def determineStateOfPhones():
	"""This will look into all configlets and look if there is some manager
	state for them. All state is collapsed into configlet._state, but the
	individual states are appended to configlet._states[]"""



	# TOOD: we could add code to update a phone state only every X seconds
	# to save processing power

	import manager

	if not __loaded: loadPythonConfig()

	phones = []
	other  = []
	for p in configlets.configlet_tree:
		try:
			chan = p.channelString()
		except AttributeError:
			#print "no channel in", p
			continue
		except TypeError:
			#print "type error in ", p
			continue


		p._states = []
		p._state = Holder()
		t = 0
		for r in manager.registry:
			r = manager.registry[r]
			if r.Peer == chan:
				p._states.append(r)
				p._state.__dict__.update(r.__dict__)
				t = max(t, r.LastUpdate)
		for mgr_chan in manager.channels:
			c = manager.channels[mgr_chan]
			if manager.normalizeChannel(mgr_chan) == chan:
				p._states.append(c)
				p._state.__dict__.update(c.__dict__)
				t  = max(t, c.LastUpdate)
				
		p._state.LastUpdate = t
		if not t:
			p._state.State = 'Off'
		elif not p._state.__dict__.has_key('State'):
			if p._state.__dict__.has_key('PeerStatus'):
				p._state.State = p._state.PeerStatus
			else:
				p._state.State = 'Unknown'

		if p.groupName=="Phones":
			phones.append(p)
		else:
			other.append(p)

		#k = p._state.keys()
		#k.sort()
		#for s in k:
		#	#print " ", s, p._state[s]
		#print

	return (phones, other)
				

def time2HMS(t):
	s = t % 60
	t = (t - s) / 60
	m = t % 60
	t = (t - m) / 60
	return "%02d:%02d:%02d" % (t,m,s)



####################################################################################
#
# Import all cfg_*.py files once when the module loads.
#

for f in os.listdir(CONFIGLETS_DIR):
	if not f.startswith('cfg_'): continue
	if not f.endswith('.py'): continue
	exec "from " + f[:-3] + " import *"





####################################################################################
#
# Test code if this file is called with 'python backend.py':
#


if __name__ == "__main__":
	loadPythonConfig()
	createPythonConfig()
	createAsteriskConfig()

def reloadAsterisk():
	"""This reloads the Asterisk PBX."""
	createPythonConfig()
	createAsteriskConfig()
	writeAsteriskConfig()
	import manager
	s = manager.reloadAsterisk()
	if configlets.configlet_tree.hasConfiglet('CfgOptMusic'):
		s += manager.reloadMoH()
	if panelutils.isConfigured():
		s += panelutils.restartPanelDaemon()
	return "".join(s)

def createDocs():
	for c in configletsList():
		cfg = globals()[c.__name__](autoAdd=False)
		cfg.writeDoc()
