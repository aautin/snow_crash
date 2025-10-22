# Level 14

## Summary

This level demonstrates a reverse engineering and anti-debugging bypass challenge. Unlike previous levels, there are no SUID binaries or scripts in the user directory. Instead, the challenge involves analyzing and exploiting the `/bin/getflag` binary itself, which contains anti-debugging protections (ptrace detection) and UID-based token selection logic that can be bypassed using GDB to retrieve the flag14 token. Same logic as level13.

## Workflow

1. No files owned by flag14, no file in home directory, but getflag exists and is executable by everyone.
	```
	level14@SnowCrash:~$ ls -l
	total 0

	level14@SnowCrash:~$ find / -user flag14 2>/dev/null | grep -v /proc/

	level14@SnowCrash:~$ find / -name getflag 2>/dev/null
	/bin/getflag
	/rofs/bin/getflag

	level14@SnowCrash:~$ ls -l /bin/getflag 
	-rwxr-xr-x 1 root root 11833 Aug 30  2015 /bin/getflag
	```

2. We can run gdb on getflag since /proc/sys/kernel/yama/ptrace_scope is set to 1, so we can debug a process we are the parent of. GDB create a child process when launching a program, unless we use -p and debug an existing process with its pid (which is here impossible with ptrace_scope set to 1). Anyway, we can still debug getflag.
	```
	level14@SnowCrash:~$ cat /proc/sys/kernel/yama/ptrace_scope
	1
	```
	=> "the default ptrace_scope value of 1 blocks one process from examining and modifying another process unless the second process (child) was started by the first process (parent)." [documentation](https://www.idealsimulations.com/guides/simworks-troubleshooting/)

3. Let's analyse the getflag run with gdb.
	```
	level14@SnowCrash:~$ gdb getflag
	(gdb) run
	Starting program: /bin/getflag 
	You should not reverse this
	[Inferior 1 (process 2901) exited with code 01]

	(gdb) disas main
	Dump of assembler code for function main:
	...
	0x08048962 <+28>:	movl   $0x0,0x10(%esp)
	0x0804896a <+36>:	movl   $0x0,0xc(%esp)
	0x08048972 <+44>:	movl   $0x1,0x8(%esp)
	0x0804897a <+52>:	movl   $0x0,0x4(%esp)
	0x08048982 <+60>:	movl   $0x0,(%esp)
	0x08048989 <+67>:	call   0x8048540 <ptrace@plt>
	0x0804898e <+72>:	test   %eax,%eax
	0x08048990 <+74>:	jns    0x80489a8 <main+98>
	...
	```

4. ptrace is called in getflag to prevent debugging. We can bypass it by forcing its return value to 0 (success) right after its call. It was preventing us from going further, we put a breakpoint before retval but then we have a final "Nope there is no token here for you sorry" message.
	```
	(gdb) b *main+72
	Breakpoint 1 at 0x804898e
	(gdb) run
	Starting program: /bin/getflag 

	Breakpoint 1, 0x0804898e in main ()
	(gdb) p $eax=0
	$1 = 0
	(gdb) continue
	Continuing.
	Check flag.Here is your token : 
	Nope there is no token here for you sorry. Try again :)
	[Inferior 1 (process 2931) exited normally]
	```

5. Further in the program, a getuid call is made to select the right token to return and obviously it takes the uid of level14 so it won't return the flag14's token. Let's take the flag14's uid, put a breakpoint after getuid and change eax to this uid.
	```
	(gdb) disass main
	0x08048b06 <+448>:	mov    0x18(%esp),%eax
	0x08048b0a <+452>:	cmp    $0xbbe,%eax
	0x08048b0f <+457>:	je     0x8048ccb <main+901>
	0x08048b15 <+463>:	cmp    $0xbbe,%eax
	0x08048b1a <+468>:	ja     0x8048b68 <main+546>
	0x08048b1c <+470>:	cmp    $0xbba,%eax
	0x08048b21 <+475>:	je     0x8048c3b <main+757>
	0x08048b27 <+481>:	cmp    $0xbba,%eax
	0x08048b2c <+486>:	ja     0x8048b4d <main+519>
	0x08048b2e <+488>:	cmp    $0xbb8,%eax
	0x08048b33 <+493>:	je     0x8048bf3 <main+685>
	...
	0x08048bb6 <+624>:	cmp    $0xbc6,%eax
	0x08048bbb <+629>:	je     0x8048de5 <main+1183>
	0x08048bc1 <+635>:	jmp    0x8048e06 <main+1216>
	0x08048bc6 <+640>:	mov    0x804b060,%eax
	```

	```
	level14@SnowCrash:~$ cat /etc/passwd | grep flag14
	flag14:x:3014:3014::/home/flag/flag14:/bin/bash
	```

	```
	(gdb) b *main+72
	Breakpoint 1 at 0x804898e
	(gdb) b *main+452
	Breakpoint 2 at 0x8048b0a
	(gdb) run
	Starting program: /bin/getflag 

	Breakpoint 1, 0x0804898e in main ()
	(gdb) p $eax=0
	$1 = 0
	(gdb) continue
	Continuing.

	Breakpoint 2, 0x08048b0a in main ()
	(gdb) p $eax=3014
	$2 = 3014
	(gdb) continue
	Continuing.
	Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
	[Inferior 1 (process 2959) exited normally]
	```

6. Finally, we have the flag14 token, we can su to flag14.
	```
	level14@SnowCrash:~$ su flag14
	Password: 
	Congratulation. Type getflag to get the key and send it to me the owner of this livecd :)
	```