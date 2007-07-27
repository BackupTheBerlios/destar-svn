# -*- coding: utf-8 -*-
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


from configlets import *

STATIC_DIR = os.getenv('STATICPAGES_DIR','static') 
styles = []
for f in os.listdir('%s/themes/' % STATIC_DIR):
	styles.append((f,f))


countries = {
	"at": {"description": _("Austria"),
		"ringcadence": "1000,5000",
		"dial": "440",
		"busy": "440/400,0/400",
		"ringtone": "440/1000,0/5000",
		"congestion": "440/200,440/200",
		"callwait": "440/40,0/1950",
		"dialrecall": "425/500,0/50",
		"recordtone": "1400/500,0/15000",
		"info": "!950/330,!1450/330,!1850/330,0/1000",
		"stutter": "350+430"
		},
	"au": {"description": _("Australia"),
		"ringcadance": "400,200,400,2000",
		"dial": "413+438",
		"busy": "425/375,0/375",
		"ring": "413+438/400,0/200,413+438/400,0/2000",
		"congestion": "425/375,0/375,420/375,0/375",
		"callwaiting": "425/200,0/200,425/200,0/4400",
		"dialrecall": "413+438",
		"record": "!425/1000,!0/15000,425/360,0/15000",
		"info": "425/2500,0/500",
		"std": "!525/100,!0/100,!525/100,!0/100,!525/100,!0/100,!525/100,!0/100,!525/100",
		"facility": "425",
		"stutter": "413+438/100,0/40",
		"ringmobile": "400+450/400,0/200,400+450/400,0/2000",
		},
	"be": {"description": _("Belgium"),
		"ringcadence": "1000,4000",
		"dial": "425",
		"busy": "425/500,0/500",
		"ring": "425/1000,0/3000",
		"congestion": "425/167,0/167",
		"callwaiting": "1400/175,0/175,1400/175,0/3500",
		"dialrecall": "!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,350+440",
		"recordtone": "1400/500,0/15000",
		"info": "950/330,1400/330,1800/330,0/1000",
		"stutter": "!425/100,!0/100,!425/100,!0/100,!425/100,!0/100,!425/100,!0/100,!425/100,!0/100,!425/100,!0/100,425",
		},
	"br": {"description": _("Brazil"),
		"ringcadance": "1000,4000",
		"dial": "425",
		"busy": "425/250,0/250",
		"ring": "425/1000,0/4000",
		"congestion": "425/250,0/250,425/750,0/250",
		"callwaiting": "425/50,0/1000",
		"dialrecall": "350+440",
		"record": "425/250,0/250",
		"info": "950/330,1400/330,1800/330",
		},
	"cl": {"description": _("Chile"),
		"ringcadance": "1000,3000",
		"dial": "400",
		"busy": "400/500,0/500",
		"ring": "400/1000,0/3000",
		"congestion": "400/200,0/200",
		"callwaiting": "400/250,0/8750",
		"dialrecall": "!400/100,!0/100,!400/100,!0/100,!400/100,!0/100,400",
		"record": "1400/500,0/15000",
		"info": "950/333,1400/333,1800/333,0/1000",
		},
	"de": {"description": _("Germany"),
		"zaptel": "nl",		# zaptel doesn't know 'de', so we're using NL instead
		"ringcadance": "1000,4000",
		"dial": "425",
		"ring": "425/1000,0/4000",
		"busy": "425/480,0/480",
		"congestion": "425/480,0/480",
		"callwaiting": "425/2000,0/6000",
		"dialrecall": "425/500,0/500,425/500,0/500,425/500,0/500,1600/100,0/900",
		"record": "1400/500,0/15000",
		"info": "950/330,0/200,1400/330,0/200,1800/330,0/1000",
		},
	"es": {"description": _("Spain"),
		"ringcadence": "1500,3000",
		"dial": "425",
		"busy": "425/200,0/200",
		"ring": "425/1500,0/3000",
		"congestion": "425/200,0/200,425/200,0/200,425/200,0/600",
		"callwaiting": "425/175,0/175,425/175,0/3500",
		"dialrecall": "!425/200,!0/200,!425/200,!0/200,!425/200,!0/200,425",
		"record": "1400/500,0/15000",
		"info": "950/330,0/1000",
		"dialout": "500",
		},
	"fi": {"description": _("Finland"),
		"ringcadance": "1000,4000",
		"dial": "425",
		"busy": "425/300,0/300",
		"ring": "425/1000,0/4000",
		"congestion": "425/200,0/200",
		"callwaiting": "425/150,0/150,425/150,0/8000",
		"dialrecall": "425/650,0/25",
		"record": "1400/500,0/15000",
		"info": "950/650,0/325,950/325,0/30,1400/1300,0/2600",
		},
	"fr": {"description": _("France"),
		"ringcadance": "1500,3500",
		"dial": "440",
		"busy": "440/500,0/500",
		"ring": "440/1500,0/3500",
		"congestion": "440/250,0/250",
		"callwaiting": "440/300,0/10000",
		"dialrecall": "!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,350+440",
		"record": "1400/500,0/15000",
		"info": "!950/330,!1400/330,!1800/330",
		},
	"gr": {"description": _("Greece"),
		"ringcadance": "1000,4000",
		"dial": "425/200,0/300,425/700,0/800",
		"busy": "425/300,0/300",
		"ring": "425/1000,0/4000",
		"congestion": "425/200,0/200",
		"callwaiting": "425/150,0/150,425/150,0/8000",
		"dialrecall": "425/650,0/25",
		"record": "1400/400,0/15000",
		"info": "!950/330,!1400/330,!1800/330,!0/1000,!950/330,!1400/330,!1800/330,!0/1000,!950/330,!1400/33",
		},
	"in": {"description": _("India"),
		"ringcadence": "400,200,400,2000",
		"dial": "400*25",
		"busy": "400/750,0/750",
		"ring": "400*25/400,0/200,400*25/400,0/2000",
		"congestion": "400/250,0/250",
		"callwaiting": "400/200,0/100,400/200,0/7500",
		"dialrecall": "400/200,0/100,400/200,0/7500",
		"record": "1400/500,0/15000",
		"info": "!950/330,!1400/330,!1800/330,0/1000",
		"stutter": "!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,350+440",
		},
	"it": {"description": _("Italy"),
		"ringcadence": "1000,4000",
		"dial": "425/600,0/1000,425/200,0/200",
		"busy": "425/500,0/500",
		"ring": "425/1000,0/4000",
		"congestion": "425/200,0/200",
		"callwaiting": "425/200,0/600,425/200,0/10000",
		"dialrecall": "470/400,425/400",
		"record": "1400/400,0/15000",
		"info": "!950/330,!1400/330,!1800/330,!0/1000,!950/330,!1400/330,!1800/330,!0/1000,!950/330,!1400/330,!1800/330,!0/1000,0",
		},
	"jp": {"description": _("Japan"),
		"ringcadence:": "1000,2000",
		"dial": "400",
		"busy": "400/500,0/500",
		"ring": "400+15/1000,0/2000",
		"congestion": "400/500,0/500",
		"callwaiting": "400+16/500,0/8000",
		"dialrecall": "!400/200,!0/200,!400/200,!0/200,!400/200,!0/200,400",
		"record": "1400/500,0/15000",
		"info": "!950/330,!1400/330,!1800/330,0",
		"stutter": "!400/100,!0/100,!400/100,!0/100,!400/100,!0/100,!400/100,!0/100,!400/100,!0/100,!400/100,!0/100,400",
		},
	"nl": {"description": _("Netherlands"),
		"ringcadance": "1000,4000",
		"dial": "425",
		"busy": "425/500,0/500",
		"ring": "425/1000,0/4000",
		"congestion": "425/250,0/250",
		"callwaiting": "440/300,0/10000",
		"dialrecall": "425/500,0/50",
		"record": "1400/500,0/15000",
		"info": "950/330,1400/330,1800/330,0/1000",
		},
	"no": {"description": _("Norway"),
		"ringcadence": "1000,4000",
		"dial": "425",
		"busy": "425/500,0/500",
		"ring": "425/1000,0/4000",
		"congestion": "425/200,0/200",
		"callwaiting": "425/200,0/600,425/200,0/10000",
		"dialrecall": "470/400,425/400",
		"record": "1400/400,0/15000",
		"info": "!950/330,!1400/330,!1800/330,!0/1000,!950/330,!1400/330,!1800/330,!0/1000,!950/330,!1400/33",
		},
	"nz": {"description": _("New Zealand"),
		"ringcadence": "400,200,400,2000",
		"dial": "400",
		"busy": "400/250,0/250",
		"ring": "400+450/400,0/200,400+450/400,0/2000",
		"congestion": "400/375,0/375",
		"callwaiting": "!400/200,!0/3000,!400/200,!0/3000,!400/200,!0/3000,!400/200",
		"dialrecall": "!400/100!0/100,!400/100,!0/100,!400/100,!0/100,400",
		"record": "1400/425,0/15000",
		"info": "400/750,0/100,400/750,0/100,400/750,0/100,400/750,0/400",
		},
	"pl": {"description": _("Poland"),
		"ringcadance": "1000,4000",
		"dial": "425",
		"busy": "425/500,0/500",
		"ring": "425/1000,0/4000",
		"congestion": "425/500,0/500",
		"callwaiting": "425/150,0/150,425/150,0/4000",
		"dialrecall": "425/500,0/50",
		"record": "1400/500,0/15000",
		"info": "950/330,1400/330,1800/330,0/1000",
		},
	"pt": {"description": _("Portugal"),
		"ringcadance": "1000,5000",
		"dial": "425",
		"busy": "425/500,0/500",
		"ring": "425/1000,0/5000",
		"congestion": "425/200,0/200",
		"callwaiting": "440/300,0/10000",
		"dialrecall": "425/1000,0/200",
		"record": "1400/500,0/15000",
		"info": "950/330,1400/330,1800/330,0/1000",
		},
	"ru": {"description": _("Russia"),
		"ringcadance": "1000,4000",
		"dial": "425",
		"busy": "425/350,0/350",
		"ring": "425/1000,0/4000",
		"congestion": "425/350,0/350",
		"callwaiting": "425/200,0/5000",
		"dialrecall": "!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,350+440",
		"record": "1400/500,0/15000",
		"info": "!950/330,!1400/330,!1800/330,0",
		},
	"se": {"description": _("Sweden"),
		"ringcadance": "1000,5000",
		"dial": "425",
		"busy": "425/250,0/250",
		"ring": "425/1000,0/5000",
		"congestion": "425/250,0/750",
		"callwaiting": "425/200,0/500,425/200,0/8000",
		"info": "950/300,0/20,1400/300,0/20,1800/300,0/1000",
		"dialrecall": "425/325,0/25",
		"record": "1400/500,0/15000",
		},
	"tw": {"description": _("Taiwan"),
		"alias": "tw",
		"ringcadance": "1000,4000",
		"dial": "350+440",
		"busy": "480+620/500,0/500",
		"ring": "440+480/1000,0/2000",
		"congestion": "480+620/250,0/250",
		"callwaiting": "350+440/250,0/250,350+440/250,0/3250",
		"dialrecall": "300/1500,0/500",
		"record": "1400/500,0/15000",
		"info": "!950/330,!1400/330,!1800/330,0",
		},
	"uk": {"description": _("United Kingdom"),
		"ringcadance": "400,200,400,2000",
		"dial": "350+440",
		"specialdial": "350+440/750,440/750",
		"busy": "400/375,0/375",
		"congestion": "400/400,0/350,400/225,0/525",
		"specialcongestion": "400/200,1004/300",
		"unobtainable": "400",
		"ring": "400+450/400,0/200,400+450/400,0/2000",
		"callwaiting": "440/100,0/4000",
		"specialcallwaiting": "400/250,0/250,400/250,0/250,400/250,0/5000",
		"creditexpired": "400/125,0/125",
		"confirm": "1400",
		"switching": "400/200,0/400,400/2000,0/400",
		"info": "950/330,0/15,1400/330,0/15,1800/330,0/1000",
		"dialrecall": "350+440",
		"record": "1400/500,0/60000",
		},
	"us": {"description": _("United States / North America"),
		"ringcadance": "2000,4000",
		"dial": "350+440",
		"busy": "480+620/500,0/500",
		"ring": "440+480/2000,0/4000",
		"congestion": "480+620/250,0/250",
		"callwaiting": "440/300,0/10000",
		"dialrecall": "!350+440/100,!0/100,!350+440/100,!0/100,!350+440/100,!0/100,350+440",
		"record": "1400/500,0/15000",
		"info": "!950/330,!1400/330,!1800/330,0",
		},
	"za": {"description": _("South Africa"),
		"ringcadance": "400,200,400,2000",
		"dial": "400*33",
		"ring": "400*33/400,0/200,400*33/400,0/2000",
		"callwaiting": "400*33/250,0/250,400*33/250,0/250,400*33/250,0/250,400*33/250,0/250",
		"congestion": "400/250,0/250",
		"busy": "400/500,0/500",
		"dialrecall": "350+440",
		"record": "1400/500,0/10000",
		"info": "950/330,1400/330,1800/330,0/330",
		}
	}

countries_lookup = map(lambda e: (e, countries[e]['description']) , countries)
countries_lookup.sort()	


class CfgOptSettings(CfgOptSingle):

	shortName = _("General settings")
	newObjectTitle= _("General settings")
	
	def createVariables(self):
		self.variables = [VarType("country",
			title=_("Country"),
			hint=_("The country is used for generating dialtone, ringtone, busytone etc"),
			type="choice",
			options=countries_lookup),
		     VarType("language",
			title=_("Language"),
			hint=_("The language is used for voice prompts"),
			len=10,
			type="string"),
		     VarType("header_text",
			title=_("Header text"),
			len=20,
			type="string"),
		     VarType("style",
			title=_("Web UI theme to use"),
			type="choice",
			options=styles),
		     VarType("logo",
			title=_("Web UI logo to use"),
			hint="/static/logo",
			type="file",
			optional=True),
		     VarType("tapi",
			title=_("Tapi Support"),
			type="bool",
			default = True),
		]

	def checkConfig(self):
		res = CfgOpt.checkConfig(self)
		if res:
			return res
		max_size = 2000000
		if self.logo:
			upload = self.logo
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
		country = countries[self.country]

		c = AstConf("indications.conf")
		c.append("country=%s" % self.country)
		for k in countries:
			c.setSection(k)
			for s in countries[k]:
				if s == "zapata": continue
				c.append("%s = %s" % (s, countries[k][s]) )


		if country.has_key('zaptel'):
			zapcountry = country['zaptel']
		else:
			zapcountry = self.country
		c = AstConf("zaptel.conf")
		c.setSection("")
		c.destar_comment = False
		c.append("loadzone = %s" % zapcountry)
		if self.country != 'us':
			c.append("defaultzone = %s" % zapcountry)
		if self.tapi:
			needModule("app_userevent")
			needModule("app_cut")
		if self.logo:
			upload = self.logo
			dest = '%s/logo' % STATIC_DIR
			out = open(dest, 'wb')
			# Copy file in chunks to avoid using lots of memory.
			while 1:
				chunk = upload.read(1024 * 1024)
				if not chunk:
				   break
				out.write(chunk)
			out.close()
			upload.close()
		self.logo = None 
