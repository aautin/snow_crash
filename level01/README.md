# LEVEL 01

## Summary

Find the user flag01's password hash in /etc/passwd, use John the Ripper to crack it and get the flag.

## Workflow

1. The directory `/home/user/level01` is empty. Searching for files owned by user `flag01` but nothing.
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
	The files's names owned by flag00 were 'John', let's try to use John the Ripper to crack it.

3. Submodule John the Ripper and put the hash in John folder
	```
	level01 git:(aautin) ✗ git submodule add https://github.com/openwall/john.git
	level01 git:(aautin) ✗ echo '42hDRfypTqqnw' > john/hash
	```

4. Download the rockyou.txt wordlist.
	```
	level01 git:(aautin) ✗ wget https://weakpass.com/download/90/rockyou.txt.gz
	level01 git:(aautin) ✗ gunzip rockyou.txt.gz
	```

5. Crack the hash with John the Ripper
	```
	level01 git:(aautin) ✗ cd john/run
	level01 git:(aautin) ✗ ./john --wordlist=../../rockyou.txt ../hash
	Using default input encoding: UTF-8
	Loaded 1 password hash (descrypt, traditional crypt(3) [DES 256/256 AVX2])
	Cracked 1 password hash (is in ./john.pot), use "--show"
	No password hashes left to crack (see FAQ)
	level01 git:(aautin) ✗ cat ./john.pot
	42hDRfypTqqnw:abcdefg
	```

6. Use it to connect and get the flag.
	```
	level01 git:(aautin) ✗ ssh flag01@<ip_address> -p 4242
	flag01@<ip_address>'s password: XXXXXXXXXXXXXXXXXXXX
	Don't forget to launch getflag !
	flag01@SnowCrash:~$ getflag
	Check flag.Here is your token : f2av5il02puano7naaf6adaaf
	```