# -*- coding: iso-latin-1 -*-
# You should execfile() this config

CfgOptRtp(
	rtpstart = 16384,
	rtpend   = 16482,
	)

CfgOptLogger(
	console  = "error,warning,notice,verbose",
	messages = "error,warning",
	facility = "",
	syslog   = "error,warning",
	)

CfgOptMusic(
	name     = "default",
	type     = "mp3",
	dir      = "/var/lib/asterisk/mohmp3",
	)

CfgAppEcho(
	ext      = "90",
	)

CfgAppMilliwatt(
	ext      = "91",
	)

CfgAppRecord(
	ext      = "92",
	filename = "/tmp/record.gsm",
	)

CfgAppPlay(
	ext      = "93",
	filename = "/tmp/record.gsm",
	)

CfgAppMusic(
	ext      = "94",
	)

CfgOptVoicemail(
	format   = "wav49",
	maxmessage = 180,
	minmessage = 2,
	maxsilence = 2,
	silencethreshold = 150,
	maxlogins = 3,
	skipms   = 3,
	)

CfgPhoneSip(
	name     = "hschurig",
	secret   = "",
	host     = "192.168.233.101",
	ext      = "15",
	context  = "default",
	did      = True,
	callerid = "15",
	usevm    = False,
	usemwi   = False,
	pin      = "1111",
	)

