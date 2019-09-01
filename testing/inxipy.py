#!/usr/bin/python3


import re

import jk_sysinfo
import jk_json
import jk_flexdata
from jk_testing import Assert










result = {
}



data_lsb_release_a = jk_flexdata.createFromData(jk_sysinfo.get_lsb_release_a())
data_lshw = jk_flexdata.createFromData(jk_sysinfo.get_lshw())
data_mobo = jk_flexdata.createFromData(jk_sysinfo.get_motherboard_info())
data_bios = jk_flexdata.createFromData(jk_sysinfo.get_bios_info())
data_proccpu = [ jk_flexdata.createFromData(x) for x in jk_sysinfo.get_proc_cpuinfo() ]
data_cpu = jk_flexdata.createFromData(jk_sysinfo.get_cpu_info())
data_sensors = jk_flexdata.createFromData(jk_sysinfo.get_sensors())
data_sysload = jk_flexdata.createFromData(jk_sysinfo.get_proc_load_avg())
data_mem = jk_flexdata.createFromData(jk_sysinfo.get_proc_meminfo())
data_lsblk = jk_flexdata.createFromData(jk_sysinfo.get_lsblk())
data_reboot = jk_flexdata.createFromData(jk_sysinfo.get_needs_reboot())
data_mounts = jk_flexdata.createFromData(jk_sysinfo.get_mount())
data_df = jk_flexdata.createFromData(jk_sysinfo.get_df())
data_ifconfig = jk_flexdata.createFromData(jk_sysinfo.get_ifconfig())




################################################################

print("\n#### system ####\n")
print("static")
print("hostname:", data_lshw.id)	# hostname
print("\tos distribution:", data_lsb_release_a.distribution)
print("\tos version:", data_lsb_release_a.version)
print("\tis LTS version:", data_lsb_release_a.lts)
print("runtime")
print("\tprocesses:", data_sysload.processes_total)
print("\tsystem load:", data_sysload.load1, "/", data_sysload.load5, "/", data_sysload.load15)
print("-")

################################################################

print("\n#### bios ####\n")
print("static")
print("\tvendor:", data_bios.vendor)
print("\tversion:", data_bios.version)
print("\tdate:", data_bios.date)
print("-")

################################################################

print("\n#### motherboard ####\n")
print("static")
print("\tvendor:", data_mobo.vendor)
print("\tname:", data_mobo.name)
print("\tversion:", data_mobo.version)
print("-")

################################################################


print("\n#### cpu ####\n")
print("static")
print("\tvendor:", data_proccpu[0].vendor_id)
print("\tmodel:", data_proccpu[0].model_name)
print("\tspeed:", jk_sysinfo.formatFrequencyRangeS(data_cpu.freq_min * 1000000, data_cpu.freq_max  * 1000000))
print("\tcpu family:", data_proccpu[0].cpu_family)
print("\tcores:", len(data_proccpu), "(hyperthreading)" if ("ht" in data_proccpu[0].flags) else "")
if "cache_size" in data_proccpu[0]._keys():
	print("\tcpu cache size:", data_proccpu[0].cache_size)
print("\tbugs:", ", ".join(data_proccpu[0].bugs))
print("-")

################################################################

print("\n#### memory ####\n")
print("runtime")
mem = data_lshw._findR(id="memory")
assert mem.units == "bytes"
#print("size:", jk_sysinfo.formatBytesS(int(mem.size)))
print("\tmem total:", jk_sysinfo.formatBytesS(data_mem.MemTotal * 1024))
print("\tmem available:", jk_sysinfo.formatBytesS(data_mem.MemAvailable * 1024))
print("\tmem free:", jk_sysinfo.formatBytesS(data_mem.MemFree * 1024))
print("\tmem buffers:", jk_sysinfo.formatBytesS(data_mem.Buffers * 1024))
print("\tmem cached:", jk_sysinfo.formatBytesS(data_mem.Cached * 1024))
print("\tswap total:", jk_sysinfo.formatBytesS(data_mem.SwapTotal * 1024))
print("\tswap free:", jk_sysinfo.formatBytesS(data_mem.SwapFree * 1024))
print("\tswap cached:", jk_sysinfo.formatBytesS(data_mem.SwapCached * 1024))
print("-")

################################################################

print("\n#### display ####\n")
print("static")
for display in data_lshw._findAllR(id="display"):
	print("\tvendor:", display.vendor)
	print("\tproduct:", display.product)
	print("\tdriver:", display.configuration.driver)
	print("-")

################################################################

print("\n#### storage ####\n")
print("static")
for storage in data_lshw._findAllR(id="storage"):
	print("\tvendor:", storage.vendor)
	print("\tproduct:", storage.product)
	print("\tdescription:", storage.description)
	print("\tdriver:", storage.configuration.driver)
	print("-")
for storage in data_lshw._findAllR(id="cdrom"):
	print("\tvendor:", storage.vendor)
	print("\tproduct:", storage.product)
	print("\tdescription:", storage.description)
	print("-")

################################################################

print("\n#### multimedia ####\n")
print("static")
for multimedia in data_lshw._findAllR(id="multimedia"):
	print("\tvendor:", multimedia.vendor)
	print("\tproduct:", multimedia.product)
	print("\tdriver:", multimedia.configuration.driver)
	print("-")

################################################################

print("\n#### network (hardware) ####\n")
print("static")
for network in data_lshw._findAllR(id="network"):
	# jk_json.prettyPrint(network._toDict())
	print("\tvendor:", network.vendor)
	print("\tproduct:", network.product)
	print("\tdevice:", network.logicalname)		# network device name
	print("\thas_link:", network.configuration.link == "yes")
	if network.capabilities.tp:
		# regular twisted pair network

		speed = None
		for key in network.capabilities._keys():
			m = re.match(r"^(\d+)bt(-fd)?$", key)
			if m:
				speed = int(m.groups()[0]) * 1000000
		if speed is None:
			if network.size:
				speed = int(network.size)

		if speed:
			speed, unit = jk_sysinfo.formatBitsPerSecond(speed)
			#assert network.units == "bit/s"
			print("\tspeed maximum:", speed, unit)					# general speed in bits/s

		if network.configuration.speed:
			print("\tspeed current:", network.configuration.speed)			# current speed
		if network.configuration.duplex:
			print("\tduplex:", network.configuration.duplex)

	elif network.configuration.wireless:
		# regular wireless network

		print("\twireless standard:", network.configuration.wireless)			# "IEEE 802.11"

	else:
		raise Exception("Unknown network type")

	print("\tdescription:", network.description)
	print("\tdriver:", network.configuration.driver)
	print("\tmac_addr:", network.serial)
	print("-")

print("\n#### buses and bus devices ####\n")
print("static")

def printPCIStruct(data:jk_flexdata.FlexObject, indent:str=""):
	print(indent + data["class"].upper() + " " + data.product + " (" + data.vendor + ")")
	if data.children:
		for c in data.children:
			printPCIStruct(c, indent=indent + "\t")
#

bridge = data_lshw._findR(_class="bridge")
printPCIStruct(bridge, indent="\t")
print("-")

################################################################

print("\n#### sensors ####\n")

def formatSensorData(data:jk_flexdata.FlexObject) -> str:
	if data._isEmpty():
		return "n/a"
	if data.sensor == "fan":
		return str(data.value) + " rpm"
	elif data.sensor == "temp":
		if data.crit and data.max:
			return jk_sysinfo.formatTemperatureGraphC(data.value, data.crit) + " (max: " + str(data.max) + ", crit: " + str(data.crit) + ")"
			#return str(data.value) + " °C (max: " + str(data.max) + ", crit: " + str(data.crit) + ")"
		else:
			return jk_sysinfo.formatTemperatureGraphC(data.value)
			#return str(data.value) + " °C"
	else:
		jk_json.prettyPrint(data._toDict())
		raise Exception()
#

print("runtime")
for data in data_sensors._values():
	#jk_json.prettyPrint(data._toDict())
	for sensorItemName, sensorItemStruct in data.sensorData._items():
		print("\t" + data.device + "." + sensorItemName + ": " + formatSensorData(sensorItemStruct))

################################################################

print("\n#### network (os) ####\n")
# TODO: list logical network adapters
jk_json.prettyPrint(data_ifconfig._toDict())

################################################################

print("\n#### drives ####\n")

print("runtime")

def printDevice(data:jk_flexdata.FlexObject, data_mounts:jk_flexdata.FlexObject, data_df:jk_flexdata.FlexObject, indent:str=""):
	Assert.isInstance(data, jk_flexdata.FlexObject)

	if data.mountpoint and data.mountpoint.startswith("/snap"):
		return
	s = indent + data.dev

	if data.mountpoint:
		s += " @ "
		s += data.mountpoint
		sAdd = " :: "
	else:
		sAdd = " :: "

	if data.uuid:
		s += sAdd + repr(data.uuid)
		sAdd = " ~ "
	if data.fstype:
		s += sAdd + data.fstype
		sAdd = " ~ "

	print(s)
	indent += "\t"

	if data_mounts and data.mountpoint:
		data_df_2 = data_df._get(data.mountpoint)
		#jk_json.prettyPrint(data_mounts._toDict())
		#jk_json.prettyPrint(data_df._toDict())
		if data_df_2:
			print(indent
				+ "total:", jk_sysinfo.formatBytesS(data_df_2.spaceTotal)
				+ ", used:", jk_sysinfo.formatBytesS(data_df_2.spaceUsed)
				+ ", free:", jk_sysinfo.formatBytesS(data_df_2.spaceFree)
				+ ", filled:", jk_sysinfo.formatPercentGraphC(data_df_2.spaceUsed, data_df_2.spaceTotal), jk_sysinfo.formatPercent(data_df_2.spaceUsed, data_df_2.spaceTotal)
				)
			#jk_json.prettyPrint(data_df_2._toDict())
		else:
			print("Not found: " + data.mountpoint)

	if data.children:
		for c in data.children:
			printDevice(c, data_mounts, data_df, indent)
#

# TODO: drive models

#print(data_lsblk._keys())
for d in data_lsblk.deviceTree:
	printDevice(d, data_mounts, data_df, "\t")
	# TODO: list logical drives

################################################################

print()



"""
System:    Host: selenium Kernel: 4.4.0-154-generic x86_64 (64 bit) Desktop: MATE 1.12.1
           Distro: Ubuntu 16.04 xenial
Machine:   Mobo: MSI model: B150M ECO (MS-7994) v: 1.0 Bios: American Megatrends v: 1.A0 date: 12/06/2017
CPU:       Quad core Intel Core i5-6600 (-MCP-) cache: 6144 KB 
           clock speeds: max: 3900 MHz 1: 799 MHz 2: 799 MHz 3: 799 MHz 4: 799 MHz
Graphics:  Card: Intel HD Graphics 530
           Display Server: X.Org 1.18.4 drivers: intel (unloaded: fbdev,vesa) Resolution: 1920x1200@59.95hz
           GLX Renderer: Mesa DRI Intel HD Graphics 530 (Skylake GT2) GLX Version: 3.0 Mesa 18.0.5
Audio:     Card Intel 100 Series/C230 Series Family HD Audio Controller driver: snd_hda_intel
           Sound: Advanced Linux Sound Architecture v: k4.4.0-154-generic
Network:   Card: Intel Ethernet Connection (2) I219-V driver: e1000e
           IF: enp0s31f6 state: up speed: 1000 Mbps duplex: full mac: d8:cb:8a:ec:5f:05
Drives:    HDD Total Size: 1000.2GB (76.7% used) ID-1: /dev/sda model: CT1000MX500SSD1 size: 1000.2GB
Partition: ID-1: / size: 917G used: 715G (83%) fs: ext4 dev: /dev/sda1
RAID:      No RAID devices: /proc/mdstat, md_mod kernel module present
Sensors:   System Temperatures: cpu: 29.8C mobo: 27.8C
           Fan Speeds (in rpm): cpu: N/A
Info:      Processes: 281 Uptime: 8 days Memory: 10592.6/31123.7MB Client: Shell (bash) inxi: 2.2.35 


·
•
○

"""







