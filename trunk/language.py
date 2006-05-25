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


#
# Import this module early into your python app
#
# The gettext.install() method will install _() into the builtin-dictionary,
# therefore all later imported python modules get _() as well.
#
# See http://docs.python.org/lib/module-gettext.html for more info.
#


import os, fnmatch, re, gettext

CONFIGLETS_DIR = os.getenv('CONFIGLETS_DIR', default='.') 

def listLanguages():
	try:
		names = fnmatch.filter(os.listdir(CONFIGLETS_DIR+'/lang/'), '*.gmo')
	except IOError:
	 	names = []
	d = dict([('en','en.gmo')] + [(re.sub(r'(.*)\.gmo',r'\1',x),x) for x in names]) 
	return d

def setLanguage(lang):
	"Set the language via gnuttext"
	if languages.has_key(lang):
		l = 'lang/' + languages[lang]
	else:
		l = 'lang/en.gmo'
	try:
	 translation = gettext.GNUTranslations(open(l,'rb'))
	except IOError:
	 translation = gettext.NullTranslations()
	translation.install()

def desactivateGettext():
	global _
	def _(message): return message

def activateGettext():
	global _
	del _

languages = listLanguages()

def encoding():
	"Returns the string used in the HTTP Header 'Content-Type: text/html; charset=...'"
	# TODO Detect right-to-left languages and return the proper string
	return "UTF-8"

# Some test code
if __name__ == '__main__':
	print _("This menu will contain all sorts of administration stuff:")
