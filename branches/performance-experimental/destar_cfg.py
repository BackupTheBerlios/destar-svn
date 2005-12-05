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
	dir      = "/usr/share/asterisk/mohmp3",
	)

CfgAppEcho(
	ext      = "90",
	)

CfgAppMilliwatt(
	ext      = "91",
	)

CfgAppRecord(
	ext      = "92",
	filename = "/tmp/record",
	format   = "WAV",
	)

CfgAppPlay(
	ext      = "93",
	filename = "/tmp/record",
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
