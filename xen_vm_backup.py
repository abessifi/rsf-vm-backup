#!/bin/usr/python

import commands, time

def get_backup_vms():

	result = []
	cmd = "xe vm-list is-control-domain=false is-a-snapshot=false"
	#List all VMs
	output = commands.getoutput(cmd)
	for vm in output.split("\n\n\n"):
		lines = vm.splitlines()
		#Search for the uuid and name of the VMs to backup
		uuid = lines[0].split(":")[1][1:]
		name = lines[1].split(":")[1][1:]
		result += [(uuid, name)]
	return result

def backup_vm(uuid, filename, timestamp):
	#Create a snapshot of each (running) VM
	cmd = "xe vm-snapshot uuid=" + uuid + " new-name-label=" + timestamp
	snapshot_uuid = commands.getoutput(cmd)
	#Transform the snapshot into a VM to be able to save it to a file
	cmd = "xe template-param-set is-a-template=false ha-always-run=false uuid=" + snapshot_uuid
	commands.getoutput(cmd)
	#Save the snapshot to file
	cmd = "xe vm-export vm=" + snapshot_uuid + " filename=" + filename
	commands.getoutput(cmd)
	#Remove the created snapshot
	cmd = "xe vm-uninstall uuid=" + snapshot_uuid + " force=true"
	commands.getoutput(cmd)

for (uuid, name) in get_backup_vms():
	timestamp = time.strftime("%Y%m%d-%H%M", time.gmtime())
	print timestamp, uuid, name
	filename = "\"" + timestamp + " " + name + ".xva\""
	backup_vm(uuid, filename, timestamp)