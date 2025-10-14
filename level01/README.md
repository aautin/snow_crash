- When you look at /etc/passwd, you see a flag. But this dosn't works to become su so let's try to decode it.

- No cipher is detected with dcode website.

- So maybe that's a ```hash```.

- We now that the user that has the flag in level00 was called John. Maybe that's the clue.

-> John is a software that bruteforce hash with a list of candidate. We have to give it a algorithm of hashing so it can compare the output of each candidate with the output of the cibled phrase.

- We saw a number at the beginning of the phrase 42hDRfypTqqnw. Maybe it is a ```salt```. A salt is used to have different output even if the passwd is the same.

Bcrypt uses salt.

So let's try to use bcrypt algorithm :

A list that is commonly used with this kind of bruteforce is rockyou.txt.

Let's dl this list.

`
zcat rockyou.txt.gz | john --stdin --format=descrypt hashes.txt`

`
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 128/128 SSE2])
Will run 20 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
abcdefg          (?)
1g 0:00:00:00 33.33g/s 2730Kp/s 2730Kc/s 2730KC/s 123456..emolove1
Use the "--show" option to display all of the cracked passwords reliably
Session completed
`

`level01@SnowCrash:~$ su flag01
Password: 
Don't forget to launch getflag !`

Go connect in ssh to the next level 
`ssh level02@192.168.0.107 -p 4242 
	   _____                      _____               _     
	  / ____|                    / ____|             | |    
	 | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
	  \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
	  ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
	 |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          192.168.0.107 
level02@192.168.0.107's password:
`




