# LEVEL 01

## Summary

## Workflow

1. The directory `/home/user/level01` is empty. Searching for files owned by user `flag01` but nothing
	```
	level01@SnowCrash:~$ find / -user flag01 2>/dev/null

	```

2. Since we have no more clue, we can print the files where passwords and login are stored in an hashed format. The user accounts must be stored in /etc/passwd but not passwords, those are contained in /etc/shadow (root read-only). We can still cat /etc/passwd to ensure no passwd is stored there.
	```
	level01@SnowCrash:~$ cat /etc/passwd | grep flag
	flag00:x:3000:3000::/home/flag/flag00:/bin/bash
	flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
	flag02:x:3002:3002::/home/flag/flag02:/bin/bash
	...
	```
	The flag01's hashed password has been put directly in as `42hDRfypTqqnw` !