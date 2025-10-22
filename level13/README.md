# Level 13

## Summary

This level demonstrates a privilege escalation vulnerability by manipulating CPU registers during program execution. The SUID binary checks the user's UID but can be bypassed using GDB to modify the EAX register value during runtime. GDB is available for the level13 user's in the SnowCrash VM.

## Workflow

1. Analyze the SUID binary and understand its behavior.
    ```
    level13@SnowCrash:~$ ls -l
    total 8
    -rwsr-sr-x 1 flag13 level13 7303 Aug 30  2015 level13
    ```

2. Test the binary execution to identify the protection mechanism.
    ```
    level13@SnowCrash:~$ ./level13
    UID 2013 started us but we we expect 4242
    ```

3. Disassemble the main function to understand the UID verification process.
    ```
    level13@SnowCrash:~$ gdb ./level13
    Reading symbols from /home/user/level13/level13...(no debugging symbols found)...done.
    (gdb) disas main
    Dump of assembler code for function main:
       0x0804858c <+0>:	push   %ebp
       0x0804858d <+1>:	mov    %esp,%ebp
       0x0804858f <+3>:	and    $0xfffffff0,%esp
       0x08048592 <+6>:	sub    $0x10,%esp
       0x08048595 <+9>:	call   0x8048380 <getuid@plt>
       0x0804859a <+14>:	cmp    $0x1092,%eax
       (...)
    ```

4. Set a breakpoint at the UID comparison and run the program in GDB.
    ```
    (gdb) break *main+14
    Breakpoint 1 at 0x804859a
    (gdb) r
    Starting program: /home/user/level13/level13

    Breakpoint 1, 0x0804859a in main ()
    ```

5. Manipulate the EAX register to bypass the UID check and retrieve the token.
    ```
    (gdb) set $eax=0x1092
    (gdb) print $eax
    $3 = 4242
    (gdb) cont
    Continuing.
    your token is 2A31L79asukciNyi8uppkEuSx
    [Inferior 1 (process 89027) exited with code 050]
    ```