-> We saw a perl file. (.pl).
-> again with ls -l we saw that it is executed with the `SUID` right.

if we try to undestand and execute it we see that

```level04@SnowCrash:~$ ./level04.pl
Content-type: text/html
```

If we open it we see a script that execute a function that print something with `echo`.
For that it takes the x value and give it to echo, that is executed by the shell.

We saw in comment that a http request via the port `4747` launch the script.

With netstat -tulnp we see the port that are listening in the machine.

### Injection

To we just have to give a value at x, here we give getflag function for the value. So it can be executed by bash with al the necessarily rights.