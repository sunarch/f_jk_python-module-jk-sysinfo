

import re

from .parsing_utils import *
from .invoke_utils import run

from .get_etc_os_release import get_etc_os_release
from .get_vcgencmd import get_vcgencmd_get_config




#
# Returns:
#	{
#		"count": 4,
#		"cpus": [
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			},
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			},
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			},
#			{
#				"freq_max": 3900,
#				"freq_min": 800
#			}
#			],
#		"freq_max": 3900,
#		"freq_min": 800
#	}
#
def get_cpu_info(c = None) -> dict:
	os_release = get_etc_os_release(c)

	ret = {}

	stdout, _, _ = run(c, "/bin/ls /sys/devices/system/cpu/")
	cpus = []
	for x in stdout.strip().split():
		if x:
			if re.match(r"^cpu(\d+)$", x):
				cpus.append(x)

	ret = {
		"count": len(cpus),
		"cpus": [],
	}

	if os_release["distribution"] == "raspbian":
		# Raspian Linux
		_cfg_result = get_vcgencmd_get_config(c)
		ret["cpus"].append({
			"freq_min": _cfg_result["cpu"]["freq_min"],
			"freq_max": _cfg_result["cpu"]["freq_max"],
		})

	else:
		# other Linux
		for cpu in cpus:
			n = int(cpu[3:])
			stdoutMin, _, _ = run(c, "cat /sys/devices/system/cpu/cpufreq/policy" + str(n) + "/cpuinfo_min_freq")
			stdoutMax, _, _ = run(c, "cat /sys/devices/system/cpu/cpufreq/policy" + str(n) + "/cpuinfo_max_freq")
			freqMin = int(stdoutMin.strip()) // 1000
			freqMax = int(stdoutMax.strip()) // 1000
			ret["cpus"].append({
				"freq_min": freqMin,
				"freq_max": freqMax,
			})

	totalFreqMin = 999999999999999
	totalFreqMax = 0
	for cpu in ret["cpus"]:
		freqMin = cpu["freq_min"]
		freqMax = cpu["freq_max"]
		if freqMax > totalFreqMax:
			totalFreqMax = freqMax
		if freqMin < totalFreqMin:
			totalFreqMin = freqMin
	ret["freq_min"] = totalFreqMin
	ret["freq_max"] = totalFreqMax

	return ret
#








