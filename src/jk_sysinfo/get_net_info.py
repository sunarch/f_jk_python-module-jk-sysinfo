

import sys
import re

import jk_json

from .parsing_utils import *
from .invoke_utils import run
from .get_ifconfig import get_ifconfig





def _get_network_file_list(c = None) -> dict:
	stdout, _, _ = run(c, "ls /sys/class/net/*/")
	groupsTemp = [ x.strip().split("\n") for x in stdout.split("\n\n") ]
	groups = {}
	for groupItems in groupsTemp:
		interface = groupItems[0].split("/")[4]
		groups[interface] = groupItems[1:]
	return groups
#



#
# Retrieve network information.
#
# Note: this function makes use of <c>get_ifconfig()</c> and adds more data. If you invoke <c>get_net_info()</c> there is no need to invoke <c>get_ifconfig()</c> any more.
#
# Returns:
#	{
#		"enp0s31f6": {
#			"ifname": "enp0s31f6",
#			"is_wlan": false,
#			"mac_addr": "c8:f7:50:43:fa:84",
#			"mtu": 1500
#		},
#		"lo": {
#			"ifname": "lo",
#			"ip4_addr": "127.0.0.1",
#			"ip4_broadcastAddr": null,
#			"ip4_netmask": "255.0.0.0",
#			"ip6_addr": "::1",
#			"ip6_scope": "host",
#			"is_wlan": false,
#			"mac_addr": "00:00:00:00:00:00",
#			"mtu": 65536
#		},
#		"wlp2s0": {
#			"ifname": "wlp2s0",
#			"ip4_addr": "192.168.99.236",
#			"ip4_broadcastAddr": "192.168.99.255",
#			"ip4_netmask": "255.255.255.0",
#			"ip6_addr": "fe80::a46e:9013:cc37:2a2c",
#			"ip6_scope": "link",
#			"is_wlan": true,
#			"mac_addr": "d4:3b:04:37:32:14",
#			"mtu": 1500
#		}
#	}
#
def get_net_info(c = None) -> dict:
	ret = {}

	data = get_ifconfig()

	groups = _get_network_file_list(c)
	interfaces = list(groups.keys())

	for interface in interfaces:
		filesAndDirs = groups[interface]

		stdout, _, _ = run(c, "cat /sys/class/net/" + interface + "/address")
		macAddr = stdout.strip()

		stdout, _, _ = run(c, "cat /sys/class/net/" + interface + "/mtu")
		mtu = int(stdout.strip())

		bIsWLAN = "wireless" in filesAndDirs

		data[interface]["mac_addr"] = macAddr
		data[interface]["mtu"] = mtu
		data[interface]["is_wlan"] = bIsWLAN

		for fileName in [ "rx_bytes", "rx_packets", "rx_errors", "rx_dropped", "tx_bytes", "tx_packets", "tx_errors", "tx_dropped" ]:
			stdout, _, _ = run(c, "cat /sys/class/net/" + interface + "/statistics/" + fileName)
			data[interface][fileName] = int(stdout.strip())

		if bIsWLAN:
			stdout, _, _ = run(c, "iwlist " + interface + " bitrate")

			"""
			wlp2s0		unknown bit-rate information.
						Current Bit Rate=144.4 Mb/s
			"""

			s = stdout.split("\n")[1].strip()
			pos = s.find(":")
			s = s[pos+1:]
			pos = s.find(" ")
			data[interface]["bitrate_current"] = {
				"value": float(s[:pos]),
				"unit": s[pos+1:].strip(),
			}

	return data
#














