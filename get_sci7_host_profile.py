#!/usr/bin/env python

import sys
import subprocess
import json
from glob import glob


def wrap_call(command):
	#Not super secure, but just set shell=True; we're still on py2.7* in 2022
	try:
		return subprocess.check_output(command, shell=True)
	except: #extremely difficult to debug... turn this off if tweaking
		return ""

def write_to_outfile(out_dict, outfile):
	with open(outfile, 'a') as outf:
		out_text = json.dumps(out_dict, sort_keys=True, indent=4, separators=(',', ': '))
		outf.write(out_text)

if __name__ == "__main__":

	out_dict = dict()

	HOST = wrap_call("hostname | sed \"s,\\.$(hostname -d),,\"").strip()
	print(HOST)		
	OUTFILE = HOST + "_profile.json"
	print("Writing output to " + OUTFILE)

	HOSTNAME = wrap_call("hostname")
	DOMAIN = wrap_call("hostname -d")
	KERNEL = wrap_call("uname -a")
	DATE = wrap_call("date")
	LSBLK = wrap_call("lsblk").split("\n")
	LSSCSI = wrap_call("lsscsi").split("\n")
	IPLINK = wrap_call("ip -h -s link | sed \'s,link.*,,\'").split("\n")
	INTERFACES = wrap_call("netstat -i | awk \'{print $1}\' | sed \'1,2d\'").split("\n")
	if INTERFACES[-1] == '':
		INTERFACES.pop(-1)
	print(INTERFACES)
	dict_interfaces = dict()
	for I in INTERFACES:
		dict_interfaces[I] = wrap_call("ethtool "+I.strip()).split("\n")
	LSCPU = wrap_call("lscpu | sed \'s,Flags.*,,\'").split("\n")
	DMI_DEV = glob("/sys/devices/virtual/dmi/id/[bc]*")
	DMI_DEV.sort()
	dmi_dict = dict()
	for device in DMI_DEV:
		if device: #skip blank
			print("Getting info for: " + device.strip())
			dmi_dict[device.strip()] = wrap_call("grep \'\' "+device.strip()).strip()

	#build dict
	out_dict = {
		'kernel': KERNEL,
		'host': HOST,
		'domain': DOMAIN,
		'date': DATE,
		'devices_block': LSBLK,
		'devices_scsi': LSSCSI,
		'link_interfaces': INTERFACES,
		'link_stats': dict_interfaces,
		'devices_cpu': LSCPU,
		'devices_general': dmi_dict
	}

	write_to_outfile(out_dict, OUTFILE)