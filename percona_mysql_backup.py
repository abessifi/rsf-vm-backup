#!/usr/bin/python

import commands, time


USER='root'
PASSWORD='admin'
MYSQL_CONFIG_FILE='/etc/mysql/my.cnf'
BACKUP_FILE_PATH = '/tmp/mysql_tables'

mysql_tables=["wp2"]

def percona_backup():
	localtime  = time.localtime()
	timeString  = time.strftime("%Y-%m-%d-%H-%M-%S", localtime)

	percona_cmd = "innobackupex-1.5.1 --user="+ USER +" --password="+ PASSWORD +" --no-lock --defaults-file=" + MYSQL_CONFIG_FILE +" --databases=\""+ ' '.join(mysql_tables) +"\" --stream=tar ./ | gzip -c -1  > "+ BACKUP_FILE_PATH +"."+ timeString +".tar.gz"

	percona_output = commands.getoutput(percona_cmd)

	print percona_output

percona_backup()