# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 by Santiago José Ruano Rincón
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

INTERFACES_FILE="/etc/network/interfaces"
RESOLV_FILE="/etc/resolv.conf"

DEFAULT_IFACES= "\
# This file describes the network interfaces available on your system\n\
# and how to activate them. For more information, see interfaces(5).\n\n\
# The loopback network interface\n\
auto lo\n\
iface lo inet loopback\n\n\
# The primary network interface\n\
auto eth0\n\
iface eth0 inet static\n\
	address 192.169.19.1\n\
	netmask 255.255.255.252\n\
	network 192.169.19.0\n"
		

class CfgOptNetworking(CfgOptSingle):

	shortName = _("Network configuration")
	newObjectTitle = _("Network Configuration")
	variables = [
			VarType("if1_label", type="label", title=_("Internal interface") ),
			VarType("if1_dhcp", title=_("Use DHCP?"), type="bool"),
			VarType("if1_ipaddr", title=_("IP Address"), default="192.169.19.1", optional=True ),
			VarType("if1_netmask", title=_("Netmask"), default="255.255.255.252", optional=True ),
			VarType("if1_gateway", title=_("Gateway"), default="192.168.19.2", optional=True ),

			VarType("if2_label", type="label", title=_("External interface"), optional=True ),
			VarType("if2_dhcp", title=_("Use DHCP?"), type="bool"),
			VarType("if2_ipaddr", title=_("IP Address"), default="", optional=True ),
			VarType("if2_netmask", title=_("Netmask"), default="", optional=True ),
			VarType("if2_gateway", title=_("Gateway"), default="", optional=True ),

			VarType("dnsserver1", title=_("Primary DNS Server"), optional=True ),
			VarType("dnsserver2", title=_("Secondary DNS Server"), optional=True ),
			VarType("domain", title=_("Search domain"), optional=True ),


		]

	def checkConfig(self):
		ret = CfgOpt.checkConfig(self)
		if ret:
			return ret
		if not self.if1_dhcp and not self.if1_ipaddr:
			return ("if1_ipaddr", _("Must have a value"))
		if not self.if1_dhcp and not self.if1_netmask:
			return ("if1_netmask", _("Must have a value"))



	def createAsteriskConfig(self):
		f = open(INTERFACES_FILE, "w")
		f.write(DEFAULT_IFACES)

		eth0_0 = "auto eth0:0\n" 
		if self.if1_dhcp:
			eth0_0 += "iface eth0:0 inet dhcp\n"
		else:
			eth0_0 += "iface eth0:0 inet static\n"
			eth0_0 += "	address %s\n" % self.if1_ipaddr
			eth0_0 += "	netmask %s\n" % self.if1_netmask
			if self.if1_gateway:
				eth0_0 += "	gateway %s\n" % self.if1_gateway

		f.write("\n" + eth0_0)

		eth1 = "\n"
 
		if self.if2_dhcp or self.if2_ipaddr:
			eth1 = "\nauto eth1\n" 
		if self.if2_dhcp:
			eth1 += "iface eth1 inet dhcp\n"
		elif self.if2_ipaddr and self.netmask:
			eth1 += "iface eth1 inet static\n"
			eth1 += "	address %s\n" % self.if2_ipaddr
			eth1 += "	netmask %s\n" % self.if2_netmask
			if self.if2_gateway:
				eth1 += "	gateway %s\n" % self.if2_gateway
		if eth1:
			f.write("\n" + eth1)

		
		f = open(RESOLV_FILE, "w")
		if self.domain:
			f.write("search %s" % self.domain)

		if self.dnsserver1:
			f.write("\nnameserver %s" % self.dnsserver1)

		if self.dnsserver2:
			f.write("\nnameserver %s" % self.dnsserver2)
		


