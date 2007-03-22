# -*- coding: utf-8 -*-
# You should execfile() this config

CfgTrunkSiptrunk(
	name     = "Voicemaster",
	id       = "DID-IPPBX",
	pw       = "13579",
	host     = "201.8.67.79",
	register = True,
	insecure = True,
	contextin = "ivr",
	ivr      = "attendant1",
	dial     = "SIP/${ARG1}@Voicemaster",
	)

CfgOptUser(
	name     = "admin",
	secret   = "ad26.",
	level    = "3",
	)

CfgIVRAutoatt(
	name     = "attendant1",
	ext      = "queue1",
	pbx      = "pbx1",
	)

CfgPhoneQueue(
	pbx      = "pbx1",
	name     = "queue1",
	ext      = "0",
	strategy = "rrmemory",
	retry    = "5",
	monitor  = True,
	monitorfileformat = "wav49",
	monitorfilename = "${TIMESTAMP}",
	panel    = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "agent1",
	secret   = "/GPOyGmK",
	ext      = "2001",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "1",
	queues   = "queue1",
	panel    = True,
	calleridnum = "2001",
	calleridname = "Agent 1",
	dialout_emergency = True,
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	dialout_quickdial = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "agent2",
	secret   = "/GPOyGmK",
	ext      = "2002",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "1",
	queues   = "queue1",
	panel    = True,
	calleridnum = "2002",
	calleridname = "Agent 2",
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "agent3",
	secret   = "/GPOyGmK",
	ext      = "2003",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "1",
	queues   = "queue1",
	panel    = True,
	calleridnum = "2003",
	calleridname = "Agent 3",
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "phone1",
	secret   = "/GPOyGmK",
	ext      = "2004",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "2",
	panel    = True,
	calleridnum = "2004",
	calleridname = "Phone 1",
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "phone2",
	secret   = "/GPOyGmK",
	ext      = "2005",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "2",
	panel    = True,
	calleridnum = "2005",
	calleridname = "Phone 2",
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "phone3",
	secret   = "/GPOyGmK",
	ext      = "2006",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "3",
	panel    = True,
	calleridnum = "2006",
	calleridname = "Phone 3",
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	)

CfgPhoneSip(
	pbx      = "pbx1",
	name     = "phone4",
	secret   = "/GPOyGmK",
	ext      = "2007",
	dtmfmode = "rfc2833",
	enablecallgroup = True,
	callgroup = "3",
	panel    = True,
	calleridnum = "2007",
	calleridname = "Phone 4",
	dialout_local = True,
	dialout_international = True,
	dialout_018X_numbers = True,
	)

CfgOptPBX(
	name     = "pbx1",
	)

CfgAppGlobalQuickDial(
	pbx      = "pbx1",
	pin      = "1234",
	set      = "80",
	ext      = "81",
	)

CfgAppPhoneQuickDial(
	pbx      = "pbx1",
	set      = "82",
	ext      = "83",
	dialprefix = "03",
	)

CfgAppCallFW(
	pbx      = "pbx1",
	type     = "CFIM",
	set      = "84",
	ext      = "85",
	)

CfgAppCallFW(
	pbx      = "pbx1",
	type     = "CFBS",
	set      = "86",
	ext      = "87",
	)

CfgAppDirectory(
	pbx      = "pbx1",
	ext      = "88",
	)

CfgAppParking(
	pbx      = "pbx1",
	ext      = "89",
	)

CfgAppMeetme(
	pbx      = "pbx1",
	ext      = "9000",
	confno   = "9000",
	)

CfgAppDND(
	pbx      = "pbx1",
	set      = "90",
	unset    = "91",
	)

CfgAppVoiceMail(
	pbx      = "pbx1",
	ext      = "92",
	)

CfgAppVoiceMail(
	pbx      = "pbx1",
	ext      = "93",
	mailbox  = True,
	)

CfgDialoutNormal(
	name     = "emergency",
	pattern  = "_9XX",
	maxtime  = 3000,
	trunk_Voicemaster = True,
	)

CfgDialoutNormal(
	name     = "local",
	pattern  = "_ZXXXXXXXXX",
	addprefix = "1",
	trunk_Voicemaster = True,
	trunk_Voicemaster_price = 1,
	)

CfgDialoutNormal(
	name     = "national",
	pattern  = "_1XXXXXXXXXX",
	trunk_Voicemaster = True,
	trunk_Voicemaster_price = 2,
	)

CfgDialoutNormal(
	name     = "international",
	pattern  = "_011X.",
	rmprefix = "3",
	trunk_Voicemaster = True,
	trunk_Voicemaster_price = 3,
	)

CfgDialoutNormal(
	name     = "018X_numbers",
	pattern  = "_018X.",
	trunk_Voicemaster = True,
	trunk_Voicemaster_price = 4,
	)

CfgDialoutNormal(
	name     = "quickdial",
	pattern  = "02XX",
	rmprefix = "2",
	qlookup  = True,
	trunk_Voicemaster = True,
	trunk_Voicemaster_price = 5,
	)

CfgOptDID(
	did      = "001",
	trunk    = "Voicemaster",
	contextin = "ivr",
	ivr      = "attendant1",
	)

CfgOptCodec(
	name     = "speex",
	)

CfgOptCodec(
	name     = "gsm",
	)

CfgOptCodec(
	name     = "alaw",
	)

CfgOptCodec(
	name     = "ulaw",
	)

CfgOptRtp(
	)

CfgOptSettings(
	country  = "us",
	language = "en",
	)

CfgOptLogger(
	)

CfgOptManager(
	name     = "destarman",
	secret   = "9fYMbomD",
	read     = ",system,call,log,verbose,command,agent,user",
	write    = ",system,call,log,verbose,command,agent,user",
	)

CfgOptOPPanel(
	security_code = "op26.",
	manager  = "destarman",
	poll_interval = "8",
	)

CfgOptPickup(
	ext      = "*8",
	)

CfgOptVoicemail(
	format   = "gsm",
	silencethreshold = 15,
	)

CfgOptMonitor(
	ext      = "#3",
	)

CfgOptTransfer(
	blindxfer = "#1",
	atxfer   = "#2",
	)

