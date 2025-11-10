## Observation

This is binary file.

if we print the output :

```bash
level13@SnowCrash:~$ ./level13
UID 2013 started us but we we expect 4242
level13@SnowCrash:~$ 
```

Seems that we have to change the value of UID.
we can do that with gdb.

`gdb ./level13`

We need the entry point 

-> Entry point: 0x80483c0 (above)

### Dissasemble

With the command `disas main` we can see what is going in our main function

```bash
(gdb) disas main
Dump of assembler code for function main:
   0x0804858c <+0>:	push   %ebp
   0x0804858d <+1>:	mov    %esp,%ebp
   0x0804858f <+3>:	and    $0xfffffff0,%esp
   0x08048592 <+6>:	sub    $0x10,%esp
   0x08048595 <+9>:	call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   0x0804859f <+19>:	je     0x80485cb <main+63>
   0x080485a1 <+21>:	call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:	mov    $0x80486c8,%edx
   0x080485ab <+31>:	movl   $0x1092,0x8(%esp)
   0x080485b3 <+39>:	mov    %eax,0x4(%esp)
   0x080485b7 <+43>:	mov    %edx,(%esp)
   0x080485ba <+46>:	call   0x8048360 <printf@plt>
   0x080485bf <+51>:	movl   $0x1,(%esp)
   0x080485c6 <+58>:	call   0x80483a0 <exit@plt>
   0x080485cb <+63>:	movl   $0x80486ef,(%esp)
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    $0x8048709,%edx
   0x080485dc <+80>:	mov    %eax,0x4(%esp)
   0x080485e0 <+84>:	mov    %edx,(%esp)
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave  
   0x080485e9 <+93>:	ret    
End of assembler dump.
```

Between <> we see 2 call to getuid function.
. 0x080485a1 <+21>:	call   

. 0x8048380 <getuid@plt>


So let's ask a break to gdb to get into the function.

```bash
(gdb) break getuid
Breakpoint 1 at 0x8048380

(gdb) run
Starting program: /home/user/level13/level13 

Breakpoint 1, 0xb7ee4cc0 in getuid () from /lib/i386-linux-gnu/libc.so.6
(gdb) 
```

Then move step by step until the return function

```bash
(gdb) step
Single stepping until exit from function getuid,
which has no line number information.
0x0804859a in main ()
```

1 step is left :

```bash
Single stepping until exit from function getuid,
which has no line number information.
0x080485a6 in main ()
```

So, this is at this moment that we have to print aex.
We know that aex is the register use to take an integer.
So when getuid() returns the UID (an integer), the result will be in $eax.

```bash
(gdb) print $eax
$1 = 2013
(gdb) 
```

Otherwise, with the command `info register` we can print all the register used by the program at this moment. 

```bash
$1 = 2013
(gdb) info registers
eax            0x7dd	2013
ecx            0xbffff7c4	-1073743932
edx            0xbffff754	-1073744044
ebx            0xb7fd0ff4	-1208152076
esp            0xbffff710	0xbffff710
ebp            0xbffff728	0xbffff728
esi            0x0	0
edi            0x0	0
eip            0x80485a6	0x80485a6 <main+26>
eflags         0x200246	[ PF ZF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
```
We can the value of the register with `set` like that 

`(gdb) set $eax = 4242`

and after continue the execution :

```bash
(gdb) continue
Continuing.
UID 4242 started us but we we expect 4242
[Inferior 1 (process 2366) exited with code 01]
```

bash```
(gdb) step                 
token is print
Single stepping until exit from function main,
which has no line number information.
your token is 2A31L79asukciNyi8uppkEuSx
```