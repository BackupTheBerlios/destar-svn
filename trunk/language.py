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


#
# Import this module early into your python app
#
# The gettext.install() method will install _() into the builtin-dictionary,
# therefore all later imported python modules get _() as well.
#
# See http://docs.python.org/lib/module-gettext.html for more info.
#


import os, gettext
try:
	translation = gettext.GNUTranslations(open('destar.mo','rb'))
except IOError:
	translation = gettext.NullTranslations()
translation.install()

if __name__ == '__main__':
	print _("Have fun!")
