- Use the command ```find``` to find by key word something with flag00 label.

find / -user 'flag00' 2>/dev/null

$ find / -user 'flag00' 2>/dev/null
/usr/sbin/john
/rofs/usr/sbin/john

cat /usr/sbin/john give you the flag

Try to become su doesn't work. So we have to decode it.

The site https://www.dcode.fr/ helps us to find which cifer has been used by bruteforcing and give us a probability.
The reponse is
-> Affine cifer. With a=1 and b=15.

2>/dev/null is used to not print potential error placing ot directly on the bin.

`level00@SnowCrash:~$ su flag00
Password: 
Don't forget to launch getflag !`