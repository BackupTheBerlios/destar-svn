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


import sys, os, types, sha, binascii, time


CONF_DIR = "/etc/asterisk"
CONF_TAG = "; Automatically created by DESTAR\n"


class AsteriskConfigFile:
	"""
	A class to generate Asterisk configuration files more easily.

	Create an AstConf class with the filename of the configfile, change
	sections and append lines or extension lines. When you call you
	destroy the class (normally at the end of program), the config file
	will be written. You can force a write with the write() method.

	This autowrite on destroy allows us to create an instance of this
	class at several places in the source code, add stuff and be sure that
	all those writes will make it into the config file.
	"""


	def __init__(self, fn):
		if fn == 'zaptel.conf':
			fn = os.path.join("/etc", fn)
		elif fn.find('/')==-1:
			fn = os.path.join(CONF_DIR, fn)
		self.fn       = fn
		self.sections = {}		# dictionary of sections
		self.order    = []		# ordered list of sections
		self.dirty    = False		# nothing to write yet
		self.extpriority = 1
		self.section  = "general"
		self.destar_comment = True
		self.lastext  = None

	def write(self, f=None):
		"Write myself into the config file"
		if self.dirty:
			if not f:
				f = open(self.fn, "w")
			if self.destar_comment:
				f.write(CONF_TAG)
			for sect in self.order:
				if sect:
					f.write("\n[%s]" % sect)
				f.write("\n")
				for l in self.sections[sect]:
					f.write(l)
					f.write("\n")
			self.dirty = False

	def setSection(self, sect):
		"Select a config file section where append() etc will put their data"
		self.section = sect
		self.extpriority  = 1

	def hasSection(self, sect):
		"Does the section already exists?"
		return sect in self.sections

	def append(self,l):
		"""Append an ordinary line to the current section"""
		try:
			self.sections[self.section].append(l)
		except KeyError:
			self.sections[self.section] = [l]
			self.order.append(self.section)
		self.dirty = True

	def prepend(self,l):
		"""Prepend an ordinary line to the current section"""
		try:
			self.sections[self.section].insert(0,l)
		except KeyError:
			self.sections[self.section] = [l]
			self.order.append(self.section)
		self.dirty = True

	def appendExten(self,ext,l,e=None):
		"""Append an extension line l to the current section. Append
		an optional error extenion e as well. Increments the priorty
		if the extension stays the same, resets the prio to 1 if the
		extension changes."""

		if ext != self.lastext:
			self.extpriority = 1
		self.lastext = ext
		self.append("exten=%s,%d,%s" % (ext, self.extpriority, l))
		if e:
			self.append("exten=%s,%d,%s" % (ext, self.extpriority+101, e))
			
		ret = self.extpriority
		self.extpriority = self.extpriority + 1
		return ret

	def setPriority(self,n):
		"""Manually set extension priority to an arbitrary number."""
		self.extpriority = n

	def appendValue(self,conf,var, name=None):
		"""Write an value that is inside an configuration class"""
		try:
			val = getattr(conf,var)
		except:
			return

		if not name:
			name = var

		if val==None:
			return

		if type(val) == types.IntType:
			self.append("%s=%d" % (name, val))
		elif type(val) == types.StringType:
			self.append("%s=%s" % (name, val))
		elif type(val) == types.FloatType:
			self.append("%s=%f" % (name, val))
		elif type(val) == types.BooleanType:
			if val:
				self.append("%s=yes" % name)
			else:
				self.append("%s=no" % name)
		else:
			print "invalid type ", val
			raise Error


asterisk_configfiles = []


def AstConf(fn):
	"""Retrieve the AsteriskConfigFile class that contains file 'fn'
	from our config file cache, create a new class if it doesn't exist."""
	global asterisk_configfiles
	for cfg, obj in asterisk_configfiles:
		if cfg == fn:
			return obj
	obj = AsteriskConfigFile(fn)
	asterisk_configfiles.append( (fn,obj) )
	return obj




#########################################################################

class __PasswordGeneratorClass:
	def __init__(self):
		self.hash = sha.new("D35tar r0ck5")
		self.hash.update(str(time.time()))

	def __call__(self, len=6, seed=""):
		try:
			self.hash.update(open("/dev/urandom", "rb").read(32))
		except IOError:
			self.hash.update(str(time.time()))

		if seed:
			self.hash.update(str(seed))
		return binascii.b2a_base64(self.hash.digest())[:len]

generatePassword = __PasswordGeneratorClass()


#########################################################################


def needModule(mod):
	#print "Need module", mod
	c = AstConf("modules.conf")
	if not "modules" in dir(c):
		#print "setting c.modules"
		c.modules = Holder(
			pbx =	[
				"pbx_config",
				"pbx_spool",
				],
			# TODO: get list of codecs and format from /usr/lib/asterisk/modules
			codec = [
				"codec_a_mu",
				"codec_adpcm",
				"codec_alaw",
				"codec_g726",
				"codec_gsm",
				"codec_ilbc",
				"codec_lpc10",
				"codec_ulaw",
				],
			format = [
				"format_g726",
				"format_g729",
				"format_gsm",
				"format_h263",
				"format_ilbc",
				"format_jpeg",
				"format_pcm",
				"format_pcm_alaw",
				"format_vox",
				"format_wav",
				"format_wav_gsm",
				],
			res =   [ "res_musiconhold",
				  "res_features" ],
			cdr =   [ ],
			chan =	[ ],
			app =	[
				"app_db",
				"app_dial",	# needs res_musiconhold, res_parking
				"app_macro",
				"app_playback",
				],
			preload = [],
			)

	sect = mod.split("_")[0]
	#print "sect", sect
	try:
		sect = c.modules[sect]
		#print "sect now:", sect
	except KeyError:
		# create new array
		c.modules[sect] = [mod]
		return
	# sect contains now the entire section array
	if not mod in sect:
		sect.append(mod)
	#print "sect finally", sect



#########################################################################

context_entries = []

def useContext(ctx):
	"""Use this function to remember all contexts that are in use."""

	if ctx not in context_entries:
		context_entries.append(ctx)
	#print context_entries



#########################################################################

class Holder(object):
	"""
	This is a simple wrapper class so that you can write

	 foo = Holder(bar = 1,
	            baz = "test")
	instead of

	 foo["bar"] = 1
	 baz["bar"] = "test"

	Holder will be a base class for all configuration options and
	modules.
	"""

	def __init__(self, **kw):
		self.__dict__.update(kw)

	def keys(self):
		"""Return list of stored variables."""
		return self.__dict__.keys()

	def __getitem__(self,key):
		"""Allows access to the variables via obj[name] syntax."""
		return self.__dict__[key]

	def __setitem__(self,key,val):
		"""Allows access to the variables via obj[name] syntax."""
		self.__dict__[key] = val

	def __repr__(self):
		return "<configlets.Holder object: " + self.__dict__.__repr__()




class VarType(Holder):
	"""We use this class to store meta-information about configuration variables"""

	def __init__(self,name,**kw):
		Holder.__init__(self,**kw)
		self.name = name
		self.__dict__.setdefault("type","string")
		self.__dict__.setdefault("len",60)
		self.__dict__.setdefault("size",20)
		self.__dict__.setdefault("title",self.name)
		self.__dict__.setdefault("hint","")
		self.__dict__.setdefault("optional", False)
		self.__dict__.setdefault("read", "admin")		# admin, user, all
		self.__dict__.setdefault("write", "admin")
		#self.__dict__.setdefault("default", "")
		self.__dict__.setdefault("hide", False)
		self.__dict__.setdefault("render_br", True)
	



config_entries = []

class Cfg(Holder):
	"""Base class for all configlets.

	Configlets belong to a group, see CfgPhone, CfgOpt, CfgTrunk etc. The
	group is also stored in the variable 'group'.

	Configlets also contain data. This data is stored quite normally, as
	anyone would store data inside a class. What is not so normal is that
	a configurable has a variables[] array that contains various VarType
	objects that describe those variables (name, description, default
	value, length etc). This descriptions are used to automatically
	create forms.

	And, last not least, a configurabe also have a name, stored in 'shortName'
	(to keep 'name' available for actual data)."""

	#shortName = "Cfg class (do not use directly)"
	#group     = "Generic option"
	variables  = []


	def __init__(self,autoAdd=True,**kw):
		"""Stores values from '*kw' into self.__dict__ and add the
		newly instantiated object into configlets.config_entries if
		'autoAdd' says so."""

		Holder.__init__(self,**kw)

		# Store the object into global array
		global config_entries
		if autoAdd:
			self._id = len(config_entries)
			config_entries.append(self)

		for v in self.variables:
			# Labels don't have values. We set 'optional' to True
			# so that we later don't get warnings about missing
			# values.
			if v.type=="label":
				v.optional = True
				continue

			# When we have a default value, then store the value
			# but don't overwrite an old value
			if v.__dict__.has_key("default") and v.default:
				try:
					if not self.__dict__[v.name]:
						self.__dict__[v.name] = v.default
				except:
					self.__dict__[v.name] = v.default


	def fixup(self):
		"""Each configlet's fixup() method get's called after the
		modules have been loaded from the config file."""

		global context_entries
		context_entries = []

		# Make sure all variables are set:
		for v in self.variables:
			if not self.__dict__.has_key(v.name):
				_v = ""
				#print v.name,v.type
				if v.__dict__.has_key("default"):
					#print "set",v.name,"to default",v.default
					_v = v.default
				elif v.type in ["string","rostring","choice","mchoice","radio"]:
					#print "set",v.name,"to ''"
					_v = ""
				elif v.type=="int":
					#print "set",v.name,"to 0"
					_v = 0
				elif v.type=="bool":
					#print "set",v.name,"to false"
					_v = False
				elif v.type=="label":
					continue
				else:
					print "didn't set",v.name,"to anything"
				#print "set %s %s to" % (v.type, v.name), _v
				self.__dict__[v.name] = _v


	def head(self):
		"""Configlets can return a tuple of headers and values via
		row() that can be used to display them in tables.

		This method gives the header. Usually it will be overwritten."""

		return ( _("Extension"),_("Type") )


	def row(self):
		"""Like head(), but returns a table row."""

		try:
			ext = self.ext
		except AttributeError:
			ext = _('None')
		return (ext, self.shortName)


	def isAddable(self):
		"""Teturns True if it is OK to create instances of this class.

		This can be used to check if a configlet should be presented
		in the menu. The method is a classMethod, so that we can call
		it without instantiating an object, e.g. we can call this
		like CfgOptPhoneZap.isAddable()."""

		# Normally every object is addable
		return True
	isAddable = classmethod(isAddable)


	def checkConfig(self):
		"""Test if all variables are set, used by createAsteriskConfig().
		May be overridden for additional test."""

		# Make sure we don't add two thingies with the same extension
		if self.__dict__.has_key('ext'):
			for o in config_entries:
				if o==self: continue
				try:
					if o.ext == self.ext:
						return ("ext", _("Extension already in use"))
				except AttributeError:
					pass

		# Make sure we don't add two thingies with the same name
		if self.__dict__.has_key('name'):
			for o in config_entries:
				if o==self: continue
				try:
					if o.name == self.name:
						return ("name", _("Name already in use"))
				except AttributeError:
					pass



	def createAsteriskConfig(self):
		"Creates AsteriskConfigFile entries if checkConfig() gave us an 'ok'."
		if self.checkConfig()==None:
			self.createAsteriskConfig()


	def createPythonConfig(self):
		"""Returns an array of strings that resends this class in Python
		syntax. Can be stored in cfg.py (or whereever) and re-read with
		execfile()."""

		python_cfg = []
		python_cfg.append("%s(" % self.__class__.__name__)
		for v in self.variables:
			if not self.__dict__.has_key(v.name): continue
			_v = self.__dict__[v.name]
			if _v == None:
				continue
			#print v.name,v.type,_v
			if v.type in ("string","rostring","choice","mchoice","radio"):
				cont = '"%s"' % _v
			elif v.type=="text":
				cont = '"""%s"""' % _v
			elif v.type=="int":
				cont = _v
			elif v.type=="bool":
				cont = ("False","True")[_v]
			elif v.type=="label":
				continue
			else:
				print "unknown type", v.type
				cont = v.type
			python_cfg.append("\t%-8s = %s," % (v.name, cont))
		python_cfg.append("\t)")
		python_cfg.append("")
		return python_cfg




#######################################################################
#
# Accessors for various settings
#

def getSetting(name, default=None):
	return getConfig('CfgOptSettings',name, default)


def getChoice(clazz):
	"""
	Here we actually use a trick. In the configlets, the variables[]
	get's build once at configlets load-time. While the configlets are
	in the middle of being loaded, you can't really iterate in
	configlets.config_entries to get a list of, say, all Phones. So this
	iteration needs to be postponed. We do this with a lambda function.

	This getChoice() uses __getChoice(), which is not defined here in
	configlets. It comes from backend.py. But because backend.py imports
	us, we don't import backend.py. Therefore, backend.py "implants"
	this helper function with "configlets._getChoice = getChoice".
	"""

	return (lambda : __getChoice(clazz=clazz))


#######################################################################
#
# Base classes for the different configlet groups
#

class CfgOpt(Cfg):
	"""Base class for all Asterisk options."""

	groupName = "Options"


	def __init__(self,**kw):
		Cfg.__init__(self,**kw)

	def head(self):
		return (_("Name"),_("Info"))


	def row(self):
		return (self.shortName,'')




class CfgOptSingle(CfgOpt):
	"""Some Asterisk options should only exist exactly once in the
	config. Descend them from this class."""

	groupName = "Options"


	def isAddable(self, clazz=None):
		"""Allow Options to be added exactly once. We'll enforce this
		by looking if the current class is already contained in
		config_entries[].

		If  a child class, e.g.  CfgOptZapAudio.isAddable(), wants
		to call us, then 'self' is no longer CfgOptZapAudio, but it
		is CfgOptSingle. This is because of the classMethod
		attribute of isAddable. So we have an optional parameter
		'clazz' where the child class can tell us which class should
		be unique in the config_entries."""

		if not clazz:
			clazz = self
		for o in config_entries:
			#print o.__class__, clazz
			if o.__class__ == clazz: return False
		return True
	isAddable = classmethod(isAddable)



class CfgTrunk(Cfg):
	"""Base class for external lines."""

	groupName = "Trunks"


	def __init__(self,**kw):
		Cfg.__init__(self,**kw)



	def head(self):
		return (_("Extension"), _("Name"), _("Type"))


	def row(self):
		try:
			ext = self.ext
		except AttributeError:
			ext = _('None')
		return (ext, self.name, self.shortName)


	def channel(self):
		return "%s/%s" % (self.technology, self.name)

	def isAddable(self):
		"We can only add this object if we have at least one other phone defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		for obj in configlets.config_entries:
			if obj.groupName == 'Phones':
				return True
		return False
	isAddable = classmethod(isAddable)
	# BUG: if the choosed phone is deleted, we have a problem



class CfgPhone(Cfg):
	"""Base class for all phone devices."""

	groupName = "Phones"


	def __init__(self,**kw):
		self.did = True
		Cfg.__init__(self,**kw)


	def head(self):
		return (_("Type"), _("Extension"), _("Name"))


	def row(self):
		try:
			ext = self.ext
		except AttributeError:
			ext = _('None')
		return (self.shortName, ext, self.name)


	def channelString(self):
		return "%s/%s" % (self.technology, self.name)


	def fixup(self):
		Cfg.fixup(self)
		useContext("phones")


	def createDialEntry(self, extensions, exten):
		ret = extensions.appendExten(exten, "Macro(dial-std-exten,%s/%s,%s,%d)" % (
			self.technology,
			self.name,
			"phones",
			int(self.usevm))
		      )

	def createExtensionConfig(self):
		needModule("res_adsi")
		needModule("app_voicemail")
		extensions = AstConf("extensions.conf")
		extensions.setSection("phones")
		if self.ext:
			self.createDialEntry(extensions, self.ext)
		self.createDialEntry(extensions, self.name);


	def createVoicemailConfig(self, conf):
		if self.ext and self.usevm:
			needModule("res_adsi")
			needModule("app_voicemail")
			if self.usemwi:
				conf.append("mailbox=%s@default" % self.ext)

			vm = AstConf("voicemail.conf")
			vm.setSection("default")
			try:
				pin = self.pin
			except:
				pin = ""
			options = "tz=cest"
			vm.append("%s=%s,%s,,%s" % (self.ext, pin, self.name, options))


class CfgApp(Cfg):
	"""Base class for all applications (an application is a piece
	of software that has a number and that you can dial)."""

	groupName ="Applications"
