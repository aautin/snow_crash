## Exploration

```bash
level14@SnowCrash:~$ ls
level14@SnowCrash:~$ 
```

Nothing...

## Strategy

Let's try to reverse this with gdb.

gdb /bin/getflag

(gdb) run
Starting program: /bin/getflag
You should not reverse this
[Inferior 1 (process 2215) exited with code 01]

> Seems to have a anti reverse protection

but you can disas the main function :

```bash
(gdb) disas main
Dump of assembler code for function main:
   0x08048946 <+0>:	push   %ebp
   0x08048947 <+1>:	mov    %esp,%ebp
   0x08048949 <+3>:	push   %ebx
   0x0804894a <+4>:	and    $0xfffffff0,%esp
   0x0804894d <+7>:	sub    $0x120,%esp
   0x08048953 <+13>:	mov    %gs:0x14,%eax
   0x08048959 <+19>:	mov    %eax,0x11c(%esp)
   0x08048960 <+26>:	xor    %eax,%eax
   0x08048962 <+28>:	movl   $0x0,0x10(%esp)
   0x0804896a <+36>:	movl   $0x0,0xc(%esp)
   0x08048972 <+44>:	movl   $0x1,0x8(%esp)
   0x0804897a <+52>:	movl   $0x0,0x4(%esp)
   0x08048982 <+60>:	movl   $0x0,(%esp)
   0x08048989 <+67>:	call   0x8048540 <ptrace@plt>
   0x0804898e <+72>:	test   %eax,%eax
   0x08048990 <+74>:	jns    0x80489a8 <main+98>
   0x08048992 <+76>:	movl   $0x8048fa8,(%esp)
   0x08048999 <+83>:	call   0x80484e0 <puts@plt>
   0x0804899e <+88>:	mov    $0x1,%eax
   0x080489a3 <+93>:	jmp    0x8048eb2 <main+1388>
   0x080489a8 <+98>:	movl   $0x8048fc4,(%esp)
   0x080489af <+105>:	call   0x80484d0 <getenv@plt>
   0x080489b4 <+110>:	test   %eax,%eax
   0x080489b6 <+112>:	je     0x80489ea <main+164>
   0x080489b8 <+114>:	mov    0x804b040,%eax
   0x080489bd <+119>:	mov    %eax,%edx
   0x080489bf <+121>:	mov    $0x8048fd0,%eax
   0x080489c4 <+126>:	mov    %edx,0xc(%esp)
   0x080489c8 <+130>:	movl   $0x25,0x8(%esp)
   0x080489d0 <+138>:	movl   $0x1,0x4(%esp)
   0x080489d8 <+146>:	mov    %eax,(%esp)
   0x080489db <+149>:	call   0x80484c0 <fwrite@plt>
   0x080489e0 <+154>:	mov    $0x1,%eax
   0x080489e5 <+159>:	jmp    0x8048eb2 <main+1388>
   0x080489ea <+164>:	movl   $0x0,0x4(%esp)
   0x080489f2 <+172>:	movl   $0x8048ff6,(%esp)
   0x080489f9 <+179>:	call   0x8048500 <open@plt>
   0x080489fe <+184>:	test   %eax,%eax
   0x08048a00 <+186>:	jle    0x8048a34 <main+238>
   0x08048a02 <+188>:	mov    0x804b040,%eax
   0x08048a07 <+193>:	mov    %eax,%edx
   0x08048a09 <+195>:	mov    $0x8048fd0,%eax
   0x08048a0e <+200>:	mov    %edx,0xc(%esp)
   0x08048a12 <+204>:	movl   $0x25,0x8(%esp)
   0x08048a1a <+212>:	movl   $0x1,0x4(%esp)
   0x08048a22 <+220>:	mov    %eax,(%esp)
   0x08048a25 <+223>:	call   0x80484c0 <fwrite@plt>
   0x08048a2a <+228>:	mov    $0x1,%eax
   0x08048a2f <+233>:	jmp    0x8048eb2 <main+1388>
   0x08048a34 <+238>:	movl   $0x0,0x4(%esp)
   0x08048a3c <+246>:	movl   $0x8049009,(%esp)
   0x08048a43 <+253>:	call   0x804871c <syscall_open>
   0x08048a48 <+258>:	mov    %eax,0x14(%esp)
```

-> We see that the program call ptrace. This is apparently that call that
block the debugging with gdb.

-> we saw that this is the firt fucntion call.

## Explanation

-> this is possible to put a breakpoint and after insert some insructions at this moment.

This is possible with `commands <id>`

```bash
(gdb) catch syscall ptrace
Catchpoint 1 (syscall 'ptrace' [26])
(gdb) commands 1
```

Catchpoints id is 1, so we have to put commands 1.

So we just have to change the return of the fucntion to bypass this call :

```bash
(gdb) catch syscall ptrace
(gdb) commands 1
> set $eax=0
> continue
> end
```

(A catchpoint is like a breakpoint but for an event and not for a memory address).

There is also a call to `getuid` function. Between a bunch of other calls.

We know that we are the flag14 user, so let's have his corresponding id.

```bash
level14@SnowCrash:/bin$ id flag14
uid=3014(flag14) gid=3014(flag14) groups=3014(flag14),1001(flag)
level14@SnowCrash:/bin$
```

So let's do everything since the beginning :

-> Change ptrace return

then 

```bash
(gdb) b getuid
Note: breakpoints 1 and 2 also set at pc 0xb7ee4cc0.
Breakpoint 4 at 0xb7ee4cc0
(gdb) run
Starting program: /bin/getflag 

Catchpoint 3 (call to syscall ptrace), 0xb7fdd428 in __kernel_vsyscall ()

Catchpoint 3 (returned from syscall ptrace), 0xb7fdd428 in __kernel_vsyscall ()

Breakpoint 1, 0xb7ee4cc0 in getuid () from /lib/i386-linux-gnu/libc.so.6
```

It works !! the anti reverse protection has been removed.

`step` until the return of getuid in getflag. to change the id value.

```bash
(gdb) step
Single stepping until exit from function getuid,
which has no line number information.
0x08048b02 in main ()
(gdb) set $eax=3014
(gdb) step
Single stepping until exit from function main,
which has no line number information.
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
0xb7e454d3 in __libc_start_main () from /lib/i386-linux-gnu/libc.so.6
```

Here is our token !