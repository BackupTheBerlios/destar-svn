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


import os
import configlets

DESTAR_CFG = "destar_cfg.py"
CONFIGLETS_DIR = "."





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
	configlets.config_entries = []

	# Try to read destar_cfg.py from Asterisk directory
	# if this doesn't work, read it from current directory
	fn = os.path.join(configlets.CONF_DIR,DESTAR_CFG)
	try:
		execfile(fn)
	except IOError:
		execfile(DESTAR_CFG)

	fixupConfiglets()

	__loaded = True





def createPythonConfig(f=None):
	"""This writes /etc/asterisk/destar_cfg.py.

	The output will be written into file hand 'f' if you provide one.
	Use this for debugging, like this:

		import sys
		createPythonConfig(sys.stdout)
	"""


	if not configlets.config_entries:
		return

	if not f:
		f = open(os.path.join(configlets.CONF_DIR,DESTAR_CFG),"w")

	f.write("# -*- coding: iso-latin-1 -*-\n")
	f.write("# You should execfile() this config\n\n")
	for c in configlets.config_entries:
		a = c.createPythonConfig()
		for s in a:
			f.write("%s\n" % s)




def initializeAsteriskConfig():
	"""This puts some hard coded default values into some asterisk
	config files:

	* extensions.conf
	* sip.conf
	* iax.cpnf
	* indications.conf
	"""


	# Start with empty config files
	configlets.asterisk_configfiles = []

	c = AstConf("extensions.conf")
	c.append("static=yes")
	c.append("writeprotect=yes")
	c.append('#include "macros.inc"')

	c.setSection("default")
	c.append("include=phones")

	c = AstConf("sip.conf")
	c.append("language=de")
	c.append("maxexpirey=3600")
	c.append("defaultexpirey=3600")
	c.append("disallow=all")
	c.append("allow=alaw")
	c.append("allow=ulaw")
	c.append("allow=ilbc")

	c = AstConf("iax.conf")
	c.append("language=de")

	c = AstConf("indications.conf")
	c.append("country=de")
	c.setSection("de")
	c.append("; http://www.teltone.com/prodmanuals/TLE Telephone Line Emulator, Rev M.pdf, Page 54")
	c.append("; http://www.hettronic.de/hettronic/computer/hardware/isdn/ta2ab/")
	c.append("description = Germany")
	c.append("ringcadance = 1000,4000")
	c.append("; Wählton")
	c.append("dial = 425")
	c.append("; Rufton")
	c.append("ring = 425/1000,0/4000")
	c.append("; Besetzt")
	c.append("busy = 425/480,0/480")
	c.append("; Identisch zu Besetzt, könnte Gassen-Belegt sein")
	c.append("congestion = 425/480,0/480")
	c.append("; Anklopfton")
	c.append("callwaiting = 425/2000,0/6000")
	c.append("; Besetzt, Rückruf möglich")
	c.append("dialrecall = 425/500,0/500,425/500,0/500,425/500,0/500,1600/100,0/900")
	c.append("; Keine Ahnung, was das ist. Kopiert von NL:")
	c.append("record = 1400/500,0/15000")
	c.append("; Tüt-Tüt-Tüt, kein Anschluß unter dieser Nummer")
	c.append("info = 950/330,0/200,1400/330,0/200,1800/330,0/1000")
	needModule("res_indications")

	# TODO InitializeMacros




def createAsteriskConfig():
	"""This creates all the Asterisk config files in /etc/asterisk.

	First, we create an in-memory representation of all config files
	to create. Then we check if any of the config files is already
	in use, but not by Asterisk. We return an array of strings with
	all file names that cannot overwritten.

	Only when all config files are safe to write, we creat all of
	them at once."""


	if not __loaded: loadPythonConfig()

	if not configlets.config_entries:
		return
	initializeAsteriskConfig()
	for c in configlets.config_entries:
		c.createAsteriskConfig()

	c = AstConf("modules.conf")
	for m in c.modules.preload:
		c.append("%s.so=yes" % m)

	c.setSection("modules")
	c.append("autoload=no")
	for sect in ("pbx", "codec", "format", "res", "cdr", "chan", "app"):
		for m in c.modules[sect]:
			c.append("load=%s.so" % m)

	# test if all config files are OK to be written or overwritten
	res = []
	for fn,cnf in configlets.asterisk_configfiles:
		#print "checking file", cnf.fn
		if os.path.exists(cnf.fn):
			f = open(cnf.fn, "r")
			s = f.readline()
			if s != configlets.CONF_TAG:
				#print "cnf.fn is not safe"
				res.append(fn)
	if res: return res
	
	# if we had no errors, write all stuff out
	for _fn,cnf in configlets.asterisk_configfiles:
		cnf.write()




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
# class.group and class.shortName. Only configlets that contains both of
# them are considered "ready for prime time", sheer descendance on Cfg isn't
# enought. That way CfgPerm, CfgPhone, CfgLine etc won't get listed.
#


def configletsList(grp=None):
	"""Returns a list of all configuration objects. We return
	the classes directly (not instantiations of the classes!):

	[ class MilliWattTest,
	  class EchoTest,
	  class IsdnCapiLine,
	  ...
	]

	When 'group' is specified, then only return configlets of this
	group."""


	res = []
	for s in globals():
		obj = globals()[s]
		try:
			g,n = obj.group, obj.shortName
			if grp and grp != g: continue
			res.append(obj)
		except AttributeError:
			pass
	return res
	



def configletsGrouped():
	"""Returns a list of all configuration objects, organized into groups:

	{ 'Applications': [class MilliWattTest, class EchoTest, ...],
	  'Options':      [class AsteriskOptions, class RtpOptions, ... ],
	  ...
	}
	"""

	res = {}
	for obj in globals():
		obj = globals()[obj]
		try:
			g,n = obj.group, obj.shortName
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


def newConfiglet(clazz):
	"""Create a new configlet with the class name 'clazz'. This new
	configlet is not added configlist.config_entries, you have to do
	this manually with addConfiglet()."""

	return globals()[clazz](autoAdd=False)




def addConfiglet(obj):
	"""Adds the configlet 'obj' to configlets.config_entries."""


	configlets.config_entries.append(obj)




def deleteConfiglet(id):
	"""Deletes the configlet with index 'id' from configlets.config_entries."""


	del configlets.config_entries[int(id)]




def moveConfigletUp(id):
	if not __loaded: loadPythonConfig()

	id = int(id)
	obj = configlets.config_entries[id]
	id2 = id-1
	while id2 >= 0:
		if configlets.config_entries[id2].group==obj.group:
			configlets.config_entries[id] = configlets.config_entries[id2]
			configlets.config_entries[id2] = obj
			return True
		id2 = id2 - 1
	return False



def moveConfigletDown(id):
	if not __loaded: loadPythonConfig()

	id = int(id)
	obj = configlets.config_entries[id]
	id2 = id+1
	while id2 < len(configlets.config_entries):
		if configlets.config_entries[id2].group==obj.group:
			configlets.config_entries[id] = configlets.config_entries[id2]
			configlets.config_entries[id2] = obj
			return True
		id2 = id2 + 1
	return False



def fixupConfiglets():
	"""Calls the fixup() method for all configlets. This should be done
	whenever the configlets get loaded, added, deleted or modified. This
	way, configlets can react on the presence of other configlets.

	Example: if a telco line with DID (direct inward dialling) is
	present, then the DID settings in the phone configuration configlets
	can be unhidden."""


	for obj in configlets.config_entries:
		obj.fixup()




def countConfiglets(group=None, clazz=None):
	"Returns the count of all configlets in a given 'group'."


	if not __loaded: loadPythonConfig()
	n = 0
	for s in configlets.config_entries:
		#print s.group
		if group and s.group == group:
			n = n + 1
		elif clazz and s.__class__.__name__==clazz:
			n = n + 1
	return n




def getConfiglets(group=None, name=None):
	"""Return a list of all configlets in a given 'group', with a given
	shortname or classname as defined in 'name'.

	Note that the short names are probably localized.

	Whenever we retrieve configlets, we're setting the attribute
	_id. You can use this id later with getConfiglet().
	"""


	if not __loaded: loadPythonConfig()
	a = []
	n = 0
	for obj in configlets.config_entries:
		obj._id = n
		n = n + 1
		if obj.group == group:
			a.append(obj)
		if obj.shortName==name or obj.__class__.__name__==name:
			a.append(obj)
	return a




def getConfiglet(id=None, name=None):
	"""This returns a configlet by the 'id'. The id is not set
	in stone, but is only valid from one getConfiglets() call
	to the next."""


	if not __loaded: loadPythonConfig()

	if name:
		n = 0
		for obj in configlets.config_entries:
			try:
				if obj.name == name:
					obj._id = n
					return obj
			except AttributeError:
				pass
			n = n + 1
		return None

	# If we have no name and no id, we can't do better:
	if id==None:
		return None

	try:
		obj = configlets.config_entries[int(id)]
		obj._id = id
		return obj
	except:
		return None
configlets.getConfiglet = getConfiglet


def getChoice(clazz, key='name',val='name'):
	"""This is used to generate a list of tupled which we later use
	in the select widgets of type "choice" or "mchoice".

	'clazz' is the classname the configlet must have."""


	if not __loaded: loadPythonConfig()
	a = []
	n = 0
	obj2 = globals()[clazz]
	for obj in configlets.config_entries:
		obj._id = n
		n = n + 1
		if isinstance(obj, obj2):
			a.append( (obj.__dict__[key],obj.__dict__[val]) )
	return a




####################################################################################
#
# Functions to determine phone state
#

def lookupPhone(phones, channel):
	"""Searches for channel in phones[].channel()"""

	#print "lookupPhone", channel
	for p in phones:
		#print p.channel()
		if channel==p.channel():
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
	for p in configlets.config_entries:
		try:
			chan = p.channel()
		except AttributeError:
			continue


		#print p.name
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

		if p.group=="Phones":
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
