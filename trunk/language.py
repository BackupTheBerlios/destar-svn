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


de_table = {
	# asterisk.py
	'Applications': 'Applikationen',
	'Options': 'Optionen',
	'Phones': 'Telefone',
	'Lines': 'Leitungen',
	'Park calls': 'Anrufe parken',
	'Echo test': 'Echotest',
	'Milliwatt test': 'Tontest',
	'Record sound': 'Ton aufzeichnen',
	'Play sound': 'Ton abspielen',
	'Music-on-hold test': 'Hintergrundmusik anh�ren',
	'Standard SIP phone': 'Normales SIP-Telefon',
	'Asterisk options': 'Asterisk-Einstellungen',
	'Background music': 'Hintergrundmusik',
	'ENUM search domain': 'ENUM-Suchdomain',
	'Loadable module': 'Ladbares Modul',
	'Logger options': 'Optionen f�r den Logger',
	'Manager access': 'Management-Zugang',
	'RTP options': 'RTP-Optionen',
	'Extension': 'Nummer',
	'Type': 'Typ',
	'Parking places': 'Anz. Parkpl�tze',
	'File name': 'Dateiname',
	'Subscriber number': 'Anschlu�nummer',
	'Mode of NTBA': 'Anschlu�typ',
	'Number of cards': 'Anzahl der Karten',
	'FWD-Number': 'FWD-Teilnehmernummer',
	'FWD-Password': 'FWD-Passwort',
	'Caller-Id for outgoing calls': 'Anruferkennung f�r ausgehende Anrufe',
	'Select phone for incoming calls': 'Telefon f�r ankommende Anrufe',
	'IP address': 'IP-Adresse',
	'Caller-Id': 'Anruferkennung',
	'Password': 'Passwort',
	'Allow direct dialling from outside?': 'Externe Anrufe zulassen?',
	'Start of RTP port area': 'Anfang der IP-Ports f�r RTP',
	'End of RTP port area': 'Ende der IP-Ports f�r RTP',


	# Template.ptl
	'User': 'Benutzer',
	'Admin': 'Wartung',
	'Config': 'Konfiguration',
	'Menu': 'Men�',
	'Submit': 'Senden',
	'Update': '�ndern',

	# DeStar.ptl
	'Main menu': 'Hauptmen�',
	'Page not found': 'Seite nicht gefunden',
	'This page does not exist': 'Diese Seite existiert nicht',

	# Cfg.ptl
	'Cnt': 'Anz',
	'Configuration': 'Konfiguration',
	'You can configure the following things': 'Diese Dinge sind konfigurierbar',
	'Edit': '�ndern',
	'Add': 'Hinzuf�gen',
	'Currently defined:': 'Derzeit definiert',

	# Missing.ptl
	'Page missing': 'Seite fehlt',
	'MissingTODO': 'Diese Seite steht auf meiner TODO-Liste :-)',
}

def _(s,key=None):
	#return de_table.get(key or s,s)
	return s
