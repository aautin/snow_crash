# Level 10

## Summary

In this level, we have access to a SUID binary that checks file permissions before reading them, and a restricted token file. By exploiting a race condition (TOCTOU vulnerability) in the binary using symbolic links, we can bypass the access control and retrieve the token.

The vulnerability arises between the access() system call and the actual file open operation, allowing us to switch the target file in between these two operations.

## Workflow

1. List the files in the home directory. The binary is SUID and the token file is owned by flag10.
    ```
    level10@SnowCrash:~$ ls -l
    total 16
	-rwsr-sr-x+ 1 flag10 level10 10817 Mar  5  2016 level10
	-rw-------  1 flag10 flag10     26 Mar  5  2016 token
    ```

2. Try to read the token file directly - access denied.
    ```
    level10@SnowCrash:~$ cat token
    cat: token: Permission denied
    ```

3. Run the binary without arguments to see how it behaves.
    ```
    level10@SnowCrash:~$ ./level10
    ./level10 file host
        sends file to host if you have access to it
    ```

4. Test the binary with different files to understand its behavior.
    ```
    level10@SnowCrash:~$ ./level10 token 127.0.0.1
    You don't have access to token
    ```

    ```
    level10@SnowCrash:~$ echo "test" > /tmp/accessible
    level10@SnowCrash:~$ ./level10 /tmp/accessible 127.0.0.1
    Connecting to 127.0.0.1:6969 .. Unable to connect to host 127.0.0.1
    ```

5. Taking a look at disassembled code, we can identify the access() then open() calls.
   ```
   level10@SnowCrash:~$ objdump -M intel -d ./level10
   080486d4 <main>:
	...
	8048746:	89 04 24             	mov    DWORD PTR [esp],eax
	8048749:	e8 92 fe ff ff       	call   80485e0 <access@plt>
	...
	8048898:	89 04 24             	mov    DWORD PTR [esp],eax
	804889b:	e8 00 fd ff ff       	call   80485a0 <open@plt>
	80488a0:	89 44 24 34          	mov    DWORD PTR [esp+0x34],eax
	...
   ```

6. Set up the TOCTOU attack using three scripts:
   - **listener**: Captures the token when sent over the network
   - **exploiter**: Rapidly switches symbolic links between accessible and restricted files
   - **executor**: Continuously runs the level10 binary

7. Create the attack scripts on your host machine and deploy them (using run script from the host machine).

8. Connect to the flag10 account using the retrieved token, then run getflag.
    ```
	flag10@192.168.56.101's password: 
	Don't forget to launch getflag !
	flag10@SnowCrash:~$ getflag
	Check flag.Here is your token : feulo4b72j7edeahuete3no7c
    ```