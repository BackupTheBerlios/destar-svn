# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig,
# This file has Copyright (C) 2009 by Alejandro Rios.
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

from configlets import *


class CfgPhoneRxfax(CfgPhone):

	shortName = _("RxFax extension")
	newObjectTitle = _("New RxFax extensiom")
	description = _("This is an extension to receive faxes through the ReceiveFax asterisk 1.6 application.")
	groupName = "Fax"
	
	def createVariables(self):
		self.variables = [
			VarType("pbx",    
				title=_("Virtual PBX"), 
				type="choice", 
				options=getChoice("CfgOptPBX")),

			VarType("name",
				title=_("Name"),
				len=15),

			VarType("ext",
				title=_("Extension"),
				len=13),
				
			VarType("filename",
					title=_("Fax .tiff file name"),
					hint=_("Otherwise it will use UniqueID"),
					len=25,
					optional=True)]
					
		self.dependencies = [
			DepType("pbx", 
					type="hard",
					message = _("This is a Dependency")),]

	def isAddable(self):
		"We can only add this object if we have at least one pbx defined."

		# BUG: it does somehow not work to simply write for obj in config_entries,
		# despite the "from configlets import *" above
		import configlets
		if len(configlets.configlet_tree.getConfigletsByName('CfgOptPBX')) > 0:
			return True
		return False
	isAddable = classmethod(isAddable)

	def createAsteriskConfig(self):
		needModule("app_fax")
		needModule("app_system")
		fax = AstConf("extensions.conf")
		fax.setSection(self.pbx)
		if self.filename:
			dest_file = "/var/spool/asterisk/fax_%s" % self.filename
		else:
			dest_file = "/var/spool/asterisk/fax_${UNIQUEID}"
		fax.appendExten("_%s" % self.ext,"Goto(fax,${EXTEN},1)")
		fax.setSection("fax")
		fax.append("exten=>_%s,1,Set(FAXFILE=%s)" % (self.ext,dest_file))
		fax.append("exten=>_%s,n,ReceiveFAX(${FAXFILE}.tif)" %  (self.ext))
		fax.append("exten=>_%s,n,Wait(2)" %  (self.ext))
		fax.append('''exten=>_%s,n,System(fax2mail --cid-number "${CALLERID(num)}" --cid-name "${CALLERID(name)}" -f "${FAXFILE}"''' %  (self.ext) )
		fax.append("exten=>_%s,n,Hangup()" %  (self.ext))
