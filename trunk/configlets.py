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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA	02111-1307	USA
#


import sys, os, types, sha, binascii, time
import panelutils

CONF_DIR = "/etc/asterisk"
DOC_DIR = os.getenv('DESTAR_DOC_DIR', default='/tmp/destar-doc')
CONF_TAG = "; Automatically created by DESTAR\n"
ASTERISK_MODULES_DIR = os.getenv('ASTERISK_MODULES_DIR', default='/usr/lib/asterisk/modules') 


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
		if fn == 'op_server.cfg' or \
		   	fn == 'op_buttons.cfg' or\
			fn == 'op_style.cfg' :
			fn = os.path.join(panelutils.PANEL_CONF_DIR, fn)
		elif fn.find('/')==-1:
			fn = os.path.join(CONF_DIR, fn)
		self.fn		  = fn
		self.sections = {}		# dictionary of sections
		self.order	  = []		# ordered list of sections
		self.dirty	  = False		# nothing to write yet
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
			raise Exception


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


def needModule(mod,preload=False):
	c = AstConf("modules.conf")
	if not "modules" in dir(c):
		c.modules = Holder(
			pbx =	[
				"pbx_config",
				"pbx_spool",
				"pbx_functions",
				],
			codec = [
				],
			format = [
				],
			res =	[ "res_musiconhold",
				  "res_features" ],
			cdr =	[	
				  "cdr_sqlite3_custom",
				  "cdr_csv", #To be used as a backup
				],
			chan =	[ ],
			func =	[ 
				"func_callerid",
				],
			app =	[
				"app_db",
				"app_dial", # needs res_musiconhold, res_parking
				"app_macro",
				"app_playback",
				"app_cdr",
				],
			preload = [],
			)
		# Get list of codecs and formats from ASTERISK_MODULES_DIR
		for f in os.listdir(ASTERISK_MODULES_DIR):
			if f.startswith('codec_'): c.modules["codec"].append(f[:-3])
			if f.startswith('format_'): c.modules["format"].append(f[:-3])
	
	if preload:
		sect = c.modules["preload"]
	else: 
		sect = mod.split("_")[0]
		try:
			sect = c.modules[sect]
		except KeyError:
			# create new array
			c.modules[sect] = [mod]
			sect = c.modules[sect]
			return
	# sect contains now the entire section array
	if not mod in sect:
		sect.append(mod)



#########################################################################

class ConfigletTree:
	
	def __init__(self):
		self.groups = {}
		self.name = ''
	
	def __getitem__(self, key):
		if self.groups.has_key(key):
			return self.groups[key]
		else: return []

	def __setitem__(self, key, val):
		self.groups[key] = val
		
	def __iter__(self):
		for group in self.groups.values():
			for element in group:
				yield element
				
	def __str__(self):
		stringname = ''
		for element in self:
			stringname += str(element) + ', '
		return stringname[:-2]
	
	def __len__(self):
		length = 0
		for i in self.groups.values():
			length += len(i)
		return length
			
	def updateConfiglet(self, obj):
		configlet_list = self.groups[obj.groupName]
		
		
		for i in range(len(configlet_list)):
			if configlet_list[i]._id == obj._id:
				configlet_list[i] = obj
				
	def deleteConfiglet(self, _id):
		for group in self.groups.values():
			for i in range(len(group)):
				if group[i]._id == _id:
					for dep in group[i].dependent_objs:
						self.deleteConfiglet(dep.configlet._id)
					del group[i]
					return
					
	def moveConfigletUp(self, _id):
		obj = self.getConfiglet(_id)
		configlet_list = self.groups[obj.groupName]
		
		for i in range(len(configlet_list)):
			if configlet_list[i]._id == obj._id and i > 0:
				configlet_list[i] = configlet_list[i-1]
				configlet_list[i-1] = obj
				return obj
		return None
		
	def moveConfigletDown(self, _id):
		obj = self.getConfiglet(_id)
		configlet_list = self.groups[obj.groupName]
		
		for i in range(len(configlet_list)):
			if configlet_list[i]._id == obj._id and i < (len(configlet_list) -1):
				configlet_list[i] = configlet_list[i+1]
				configlet_list[i+1] = obj
				return obj
		return None
	
	def getConfigletsByGroup(self, groupName):
		return self[groupName]
	
	#TODO: Make this as fast as getConfigletsByGroup
	def getConfigletsByName(self, name):
		result = []
		for obj in self:
			if obj.shortName == name or obj.__class__.__name__ == name:
				result.append(obj)
		return result

	def getConfigletsByClass(self, _class):
		result = []
		for obj in self:
			if isinstance(obj, _class):
				result.append(obj)
		return result
		
	def hasConfiglet(self, _class):
		for obj in self:
			if obj.__class__.__name__ == _class: 
				return True
		return False
			

	def empty(self):
		return len(self)==0
		
	def getConfiglet(self, _id):
		for obj in self:
			try:
				if obj._id == int(_id):
					return obj
			except:
				pass
		return None
		
	def getConfigletByName(self, name):
		for obj in self:
			try:
				if obj.name == name:
					return obj
			except:
				pass
		return None
		
	def addConfiglet(self, configlet):
		if not self.groups.has_key(configlet.groupName):
			self.groups[configlet.groupName] = []
		self.groups[configlet.groupName].append(configlet)
	

configlet_tree = ConfigletTree()

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


class DepType(Holder):
	"""We use this class to store meta-information about dependendencies"""
	
	def __init__(self,name,**kw):
		Holder.__init__(self,**kw)
		self.name = name
		self.__dict__.setdefault("type","hard")
		self.__dict__.setdefault("message", _("This is a Dependency"))

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
	




class DependentObject:
	def __init__(self, configlet, dependency):
		self.configlet = configlet
		self.dependency = dependency

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
	#group	   = "Generic option"
	variables  = []
	dependent_objs = []
	dependencies = []


	def __init__(self,autoAdd=True,**kw):
		"""Stores values from '*kw' into self.__dict__ and add the
		newly instantiated object into configlets.configlet_tree if
		'autoAdd' says so."""

		Holder.__init__(self,**kw)

		# Store the object into global array
		global configlet_tree
		self._id = len(configlet_tree)
		if autoAdd:
			configlet_tree.addConfiglet(self)
		else:
			self.createVariables();
			self.fixup();

		for v in self.variables:
			# Labels don't have values. We set 'optional' to True
			# so that we later don't get warnings about missing
			# values.
			if v.type=="label":
				v.optional = True
				continue
				
		self.dependent_objs = []
		self.dependencies = []
				
	def __getattr__(self, field):
		self.createVariables()
		self.fixup()
		if self.__dict__.has_key(field):
			return self.__dict__[field]
		else:
			raise AttributeError

	def lookPanel(self):
		if panelutils.isConfigured() == 1:
			for v in self.variables:
				if v.name == "panelLab" or v.name == "panel":
					v.hide = False
					
	def renameDependencies(self, new_name):
		for dep in self.dependent_objs:
				dep.configlet.__dict__[dep.dependency.name] = new_name

	def hasDependencies(self):
		return len(self.dependent_objs) > 0

	def createDependencies(self):
		for dep in self.dependencies:
			if self.__dict__.has_key(dep.name):
				obj_name = self.__dict__[dep.name]
				import configlets
				obj = configlets.configlet_tree.getConfigletByName(obj_name)
				if obj is None:
					return
				dependent_obj = DependentObject(self, dep)
				obj.dependent_objs.append(dependent_obj)

	def createVariables(self):
		variables = []
		
	def clearDependencies(self):
		self.dependent_objs = []

	def fixup(self):
		"""Each configlet's fixup() method get's called after the
		modules have been loaded from the config file."""

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

		# Make sure we don't add two thingies with the same extension on the same pbx
		global configlet_tree
		if self.__dict__.has_key('ext'):
			for o in configlet_tree:
				if o==self: continue
				try:
					if o.ext == self.ext and o.pbx == self.pbx:
						return ("ext", _("Extension already in use on that PBX"))
				except AttributeError:
					pass

		# Make sure we don't add two thingies with the same name
		if self.__dict__.has_key('name'):
			if self.name.find("-") > 1 or self.name.find(" ") > 1:
				return ("name", _("Name should not contain '-' or spaces"))
			for o in configlet_tree:
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
			if _v == None or _v == "":
				continue
			#print v.name,v.type,_v
			if v.__dict__.has_key("default") and _v==v.default:
				continue
			if v.type in ("string","rostring","choice","mchoice","radio"):
				cont = '"%s"' % _v
			elif v.type=="text":
				cont = '"""%s"""' % _v
			elif v.type=="int":
				if _v == 0:
					print v.name
					continue
				else:
					cont = _v
			elif v.type=="bool":
				if _v:
					cont = "True"
				else:
					continue
			elif v.type=="label":
				continue
			else:
				print "unknown type", v.type
				cont = v.type
			python_cfg.append("\t%-8s = %s," % (v.name, cont))
		python_cfg.append("\t)")
		python_cfg.append("")
		return python_cfg

	def writeDoc(self, d=None):
		"Write my documentation"
		if not d:
			d = DOC_DIR
		fn = os.path.join(d, "%s.xml" % self.__class__.__name__.lower())
		f = open(fn, "w")
		f.write('<?xml version="1.0" encoding="UTF-8"?>')
		f.write("\n")
		f.write("<!-- file: autogenerated/%s.xml -->" % self.__class__.__name__.lower())
		f.write("\n")
		f.write("<!-- File automatically created by DESTAR -->")
		f.write("\n")
		f.write('<!-- xml-parent-document: "../configlets.xml" -->')
		f.write("\n")
		f.write("<!-- Destar Manual -->")
		f.write("\n")
		f.write("<!-- Distributed under the same Destar license  -->")
		f.write("\n\n")
		f.write('<sect2 id="%s">\n\n' % self.__class__.__name__.lower())
		f.write("<title>%s - %s</title>\n\n" % (self.groupName,self.shortName))

		try:
			if self.description:
				f.write("<para>%s</para>\n\n" % self.description)
		except AttributeError:
			print _("The configlet '%s' does not have a description" % self.__class__.__name__)
		
		f.write("<para>Form fields:</para>\n\n<itemizedlist>\n\n")
		for var in self.variables:
			if var.title:
				f.write("  <listitem>\n    <para>\n")
				if var.type == "label":
					f.write("Section [%s]" % var.title)
				else:
					f.write("%s" % var.title)
					if var.hint:
						f.write(": %s" % var.hint)
				f.write("\n    </para>\n  </listitem>\n")
		f.write("</itemizedlist>\n\n")
		f.write("</sect2>")
	

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
	configlets.configlet_tree to get a list of, say, all Phones. So this
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
		configlet_tree.

		If	a child class, e.g.	 CfgOptZapAudio.isAddable(), wants
		to call us, then 'self' is no longer CfgOptZapAudio, but it
		is CfgOptSingle. This is because of the classMethod
		attribute of isAddable. So we have an optional parameter
		'clazz' where the child class can tell us which class should
		be unique in the configlet_tree."""

		global configlet_tree
		if not clazz:
			clazz = self
		for o in configlet_tree:
			#print o.__class__, clazz
			if o.__class__ == clazz: return False
		return True
	isAddable = classmethod(isAddable)

class VarListManager:

	def __init__(self):
		self.trunks = []
		self.dialouts = []
		
	def hasTrunks(self):
		return len(self.trunks)>0
		
	def getTrunks(self):
		return self.trunks
		
	def updateTrunks(self):
		self.trunks = []
		global configlet_tree
		for obj in configlet_tree['Trunks']:
			self.trunks.append(VarType("trunk_%s" % obj.name, title=_("%s") % obj.name, type="bool", optional=True,render_br=False))
			self.trunks.append(VarType("trunk_%s_price" % obj.name, title=_("Price/Account_code for this pattern"), type="int", optional=True, len=10, default=0))

	def hasDialouts(self):
		return len(self.dialouts)>0

	def getDialouts(self):
		return self.dialouts

	def updateDialouts(self):
		self.dialouts = []
		global configlet_tree
		for obj in configlet_tree['Dialout']:
			self.dialouts.append(VarType("dialout_%s" % obj.name, title=_("%s") % obj.name, type="bool", optional=True,render_br=False))
			self.dialouts.append(VarType("dialout_%s_secret" % obj.name, title=_("Password:"), len=50, optional=True))

varlist_manager = VarListManager()


class CfgTrunk(Cfg):
	"""Base class for external lines."""

	groupName = "Trunks"


	def __init__(self,**kw):
		Cfg.__init__(self,**kw)

	def fixup(self):
		Cfg.fixup(self)
		self.lookPanel()


	def head(self):
		return (_("Name"), _("Type"), _("Dial Command"))


	def row(self):
		return (self.name, self.shortName, self.dial)


	def channel(self):
		return "%s/%s" % (self.technology, self.name)

	def isAddable(self):
		"We can only add this object if we have at least one other phone defined."

		# BUG: it does somehow not work to simply write for obj in configlet_tree,
		# despite the "from configlets import *" above
		global configlet_tree
		if len(configlet_tree['Phones']) > 0:
			return True
		else:
			return False
	isAddable = classmethod(isAddable)
	# BUG: if the choosed phone is deleted, we have a problem

	def checkConfig(self):
		res = Cfg.checkConfig(self)
		if res:
			return res
		if self.contextin == 'phone' and not self.phone:
			return ('phone',_("You should select a phone to ring to"))

	def createIncomingContext(self): 
		c = AstConf("extensions.conf")
		contextin = "in-%s" % self.name
		c.setSection(contextin)
		c.appendExten("s","Set(CDR(intrunk)=%s)" %  self.name)
		if self.clid:
			needModule("func_callerid")
			c.appendExten("s","Set(CALLERID(name)=%s)" %  self.clid)
		global configlet_tree
		if self.contextin == 'phone' and self.phone:
			obj = configlet_tree.getConfigletByName(self.phone)
			try:
				pbx = obj.pbx
				c.appendExten("s", "Goto(%s,%s,1)" % (pbx,self.phone))
			except AttributeError:
				pass
		if self.contextin == 'ivr' and self.ivr:
			c.appendExten("s", "Goto(%s,s,1)" % self.ivr)
		if self.contextin == 'pbx' and self.pbx:
			c.appendExten("s", "Goto(%s,s,1)" % self.pbx)

		c.appendExten("_X.","Set(CDR(intrunk)=%s)" %  self.name)
		if self.clid:
			needModule("func_callerid")
			c.appendExten("_X.","Set(CALLERID(name)=%s)" %  self.clid)
		global configlet_tree
		if self.contextin == 'phone' and self.phone:
			obj = configlet_tree.getConfigletByName(self.phone)
			try:
				pbx = obj.pbx
				c.appendExten("_X.", "Goto(%s,%s,1)" % (pbx,self.phone))
			except AttributeError:
				pass
		if self.contextin == 'ivr' and self.ivr:
			c.appendExten("_X.", "Goto(%s,s,1)" % self.ivr)
		if self.contextin == 'pbx' and self.pbx:
			c.appendExten("_X.", "Goto(%s,${EXTEN},1)" % self.ivr)

		
class CfgPhone(Cfg):
	"""Base class for all phone devices."""

	groupName = "Phones"


	def __init__(self,**kw):
		self.did = True
		Cfg.__init__(self,**kw)


	def head(self):
		return (_("Type"), _("Extension"), _("Name"), _("Virtual PBX"))


	def row(self):
		try:
			ext = self.ext
			pbx = self.pbx
		except AttributeError:
			ext = _('None')
			pbx = _('None')
		return (self.shortName, ext, self.name, pbx)


	def channelString(self):
		return "%s/%s" % (self.technology, self.name)


	def fixup(self):
		Cfg.fixup(self)
		self.lookPanel()
		global configlet_tree
		if configlet_tree.hasConfiglet('CfgPhoneQueue'):
			for v in self.variables:
				if v.name == "QueueLab" or v.name == "queues":
					v.hide = False

	def createDialEntry(self, extensions, exten, pbx, ext):
		ret = extensions.appendExten(exten, "Macro(dial-std-exten,%s/%s,out-%s,%d,%s,%s)" % (
			self.technology,
			self.name,
			self.name,
			int(self.usevm),
			ext,
			pbx
			))

	def createExtensionConfig(self):
		needModule("res_adsi")
		needModule("app_voicemail")
		extensions = AstConf("extensions.conf")
                try:
                        pbx = self.pbx
                except AttributeError:
                        pbx = "phones"
                extensions.setSection(pbx)
		extensions.appendExten(self.ext,"Set(CDR(pbx)=%s,CDR(userfield)=%s)" % (pbx,self.name))
		self.createDialEntry(extensions, self.ext, pbx, self.ext)
		extensions.appendExten(self.name,"Set(CDR(pbx)=%s,CDR(userfield)=%s)" % (pbx,self.name))
		self.createDialEntry(extensions, self.name, pbx, self.ext)

	def createHintConfig(self):
		extensions = AstConf("extensions.conf")
        	try:
            		pbx = self.pbx
        	except AttributeError:
            		pbx = "phones"
        	extensions.setSection(pbx)
		extensions.append("exten=%s,hint,%s/%s" % (self.ext, self.technology, self.name))

	def createVoicemailConfig(self, conf):
		if self.ext and self.usevm:
			needModule("res_adsi")
			needModule("app_voicemail")
			if self.usemwi:
				conf.append("mailbox=%s@%s" % (self.ext,self.pbx))

			vm = AstConf("voicemail.conf")
			vm.setSection(self.pbx)
			try:
				pin = self.pin
			except:
				pin = ""
			#TODO: deal with timezones
			#options = "tz=cest"
			options = ""
			if self.email:
				vm.append("%s=%s,%s,%s,%s" % (self.ext, pin, self.name, self.email, options))
			else:
				vm.append("%s=%s,%s,,%s" % (self.ext, pin, self.name, options))
	
	def createQueuesConfig(self):
		try:
			if self.queues:
				c = AstConf("queues.conf")
				for queue in self.queues.split(','):
					c.setSection(queue)
					c.append("member => %s/%s" % (self.technology,self.name))
		except AttributeError:
			pass

	def createOutgoingContext(self):
		c = AstConf("extensions.conf")
		c.setSection("out-%s" % self.name)
		try:
			pbx = self.pbx
		except AttributeError:
			pbx = "phones"
		c.append("include=>%s" % pbx)
		c.appendExten("i","Playback(privacy-invalid)")
		try:
			timeoutvalue = not self.timeout and "0" or "1"
		except AttributeError:
			timeoutvalue=0
		global configlet_tree
		for obj in configlet_tree:
			if obj.__class__.__name__ == 'CfgDialoutNormal':
				try:
					if self.__getitem__("dialout_"+obj.name):
						c.appendExten("%s" % obj.pattern,"Set(CDR(pbx)=%s)" % (self.pbx))
						c.appendExten("%s" % obj.pattern,"Set(CDR(userfield)=%s)" % (self.name))
						c.appendExten("%s" % obj.pattern,"Set(CDR(dialout)=%s)" % (obj.name))
						if self.calleridnum:
							c.appendExten("%s" % obj.pattern,"Set(CALLERID(number)=%s)" % self.calleridnum)
							
						if self.monitor:
							needModule("app_mixmonitor")	
							options = ""
							if self.monitorappend:
								options = 'a' 
							if self.monitorwhenbridged:
								options = options+'b'
							if self.heardvol == self.spokenvol:
								options = options+'W(%s)' % (self.heardvol)
							else:          
								options = options+'v(%s)V(%s)' % (self.heardvol, self.spokenvol)        
							if self.monitorfilename:
								c.appendExten("%s" % obj.pattern, "MixMonitor(%s.%s|%s)" % (self.monitorfilename,self.monitorfileformat,options))
							else:
								c.appendExten("%s" % obj.pattern, "MixMonitor(${TIMESTAMP}-${CALLERIDNAME}(${CALLERIDNUM})-${EXTEN}.%s|%s)" % (self.monitorfileformat,options))
						
						secret = self.__getitem__("dialout_%s_secret" % obj.name)							
						if secret:
							c.appendExten("%s" % obj.pattern,"Macro(%s,%s${EXTEN:%s},%s,%s)" % (obj.name,obj.addprefix,obj.rmprefix,secret,timeoutvalue))
						else:
							c.appendExten("%s" % obj.pattern,"Macro(%s,%s${EXTEN:%s},n,%s)" % (obj.name,obj.addprefix,obj.rmprefix,timeoutvalue))
				except KeyError:
					pass
			elif obj.__class__.__name__ == 'CfgAppPhoneQuickDial':
				prefix = obj.dialprefix
				c.appendExten("_%sXX" % prefix,"Set(dest=${DB(QUICKDIALLIST/${CALLERIDNUM}/${EXTEN:%d})})" % len(prefix), e="Playback(privacy-invalid)")
				c.appendExten("_%sXX" % prefix,"Goto(${dest},1)")
	
	def createPanelConfig(self):
		try:
			if panelutils.isConfigured() == 1 and self.panel:
				panelutils.createExtButton(self)
		except AttributeError:
			pass

class CfgApp(Cfg):
	"""Base class for all applications (an application is a piece
	of software that has a number and that you can dial)."""

	groupName ="Applications"

	def head(self):
		return (_("Extension"), _("Type"), _("Virtual PBX"))

	def row(self):
		try:
			pbx = self.pbx
		except AttributeError:
			pbx = _('None')
		return (self.ext, self.shortName, pbx)
 
	
class CfgDialout(Cfg):
	"""Base class for dialout entries."""

	groupName = "Dialout"


	def __init__(self,**kw):
		Cfg.__init__(self,**kw)


	def head(self):
		return (_("Extension"), _("Name"), _("Type"))


	def row(self):
		try:
			ext = self.pattern
		except AttributeError:
			ext = _('None')
		return (ext, self.name, self.shortName)

class CfgIVR(Cfg):
	"""Base class for IVRs."""

	groupName = "IVRs"


	def __init__(self,**kw):
		Cfg.__init__(self,**kw)

	def head(self):
		return (_("Name"),_("Info"))


	def row(self):
		return (self.shortName,self.name)

