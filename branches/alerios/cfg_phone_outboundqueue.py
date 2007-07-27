# -*- coding: utf-8 -*-
#
# Destar has Copyright (C) 2005 by Holger Schurig,
# This file has Copyright (C) 2007 by Alejandro Rios P.
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
from cfg_phone_queue import *

STATIC_DIR = os.getenv('STATICPAGES_DIR','static') 

class CfgPhoneOutboundQueue(CfgPhoneQueue):

	shortName = _("Outbound Campaing")
	newObjectTitle= _("Outbound Campaing")
	description = _("General settings for an Outbound Campaing")
	technology = "QUEUE"
	groupName = "Queues"
	
	def createVariables(self):
		CfgPhoneQueue.createVariables(self)
		self.variables = self.variables + [
			VarType("OutboundLabel",
				title=_("Outbound campaing parammeters"),
				type="label"),
			VarType("ratio",
				title=_("'Calls per agent' ratio:"),
				hint=_("<calls>:<agents>"),
				default="1.5:1"),
			VarType("evalperiod",
				title=_("Evaluation period:"),
				hint=_("In seconds"),
				default=60,
				optional=True,
				type="int"),
			VarType("calltime",
				title=_("Average call time:"),
				hint=_("In seconds"),
				default=300,
				type="int"),
			VarType("resttime",
				title=_("Average pause time between calls:"),
				hint=_("In seconds"),
				default=120,
				type="int"),
			VarType("list",
				title=_("List of numbers to call"),
				hint="/static/outbound/",
				type="file",
				optional=True),
			]
	
	def checkConfig(self):
		res = CfgPhoneQueue.checkConfig(self)
		if res:
			return res
		max_size = 2000000
		if not len(self.ratio.split(":")) > 1:
			return _("Ratio must be in the format '<calls>:<agents>'")
		if self.list:
			upload = self.list
			pos = upload.fp.tell()  # Save current position in file.
			upload.fp.seek(0, 2)    # Go to end of file.
			size = upload.fp.tell() # Get new position (which is the file size).
			upload.fp.seek(pos, 0)  # Return to previous position.
			upload.size = size
			if size > max_size:
				msg = "The uploaded file is too big (size=%s, max=%s bytes)"
				msg %= (size, max_size)
				return _("File bigger than %s bytes") % max_size
	
	def createAsteriskConfig(self):
		CfgPhoneQueue.createAsteriskConfig(self)
		if self.list:
			upload = self.list
			dest = '%s/outbound/%s' % (STATIC_DIR, self.name)
			out = open(dest, 'wb')
			# Copy file in chunks to avoid using lots of memory.
			while 1:
				chunk = upload.read(1024 * 1024)
				if not chunk:
				   break
				out.write(chunk)
			out.close()
			upload.close()
		self.list = None 
