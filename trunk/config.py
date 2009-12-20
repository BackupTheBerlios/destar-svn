#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Global variables used by destar
#
import os

# - DESTAR SETTINGS

DESTAR_CFG = "destar_cfg.py"

CONFIGLETS_DIR = os.getenv('CONFIGLETS_DIR', default='.') 

DOC_DIR = os.getenv('DESTAR_DOC_DIR', default='/tmp/destar-doc')

CONF_TAG = "; Automatically created by DESTAR\n"

MAXSECRETLENGTH = 45

# -  ASTERISK PATHS

CONF_DIR = "/etc/asterisk"

ASTERISK_MODULES_DIR = os.getenv('ASTERISK_MODULES_DIR', default='/usr/lib/asterisk/modules') 

# - MYSQL INFO

DBHOST = "172.30.0.4"
DBNAME = "asterisk"
DBUSER = "root"
DBPASSWD = "q931avt+-"

# - FLASH OPERATOR PANEL SETTINGS

# Uncomment to use with asternic.org op_panel tarball:
#PANEL_CONF_DIR	= "/usr/local/op_panel"
#PANEL_HTML_DIR	= "/usr/local/op_panel/flash"
#PANEL_RESTART_CMD = "killall -HUP op_server.pl"

# Uncomment to use with op-panel .deb package:
PANEL_CONF_DIR	= "/etc/op-panel"
PANEL_HTML_DIR	= "/usr/share/op-panel/flash"
PANEL_RESTART_CMD = "killall -HUP op_server"


# - OTHER APPS INTEGRATION

VICIDIAL_INTEGRATION = 0
SAMBA_ENABLED = 0
SAMBA_RESTART_CMD = "/etc/init.d/samba reload"
