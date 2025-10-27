We can see a cesar cipher with an incrementation of +1 of difference

level09@SnowCrash:~$ ./level09 token
tpmhr
level09@SnowCrash:~$ 

`(−0, −1, −2, −3, −4) = token`

bash```
level09@SnowCrash:~$ cat token
f4kmm6p|=�p�n��DB�Du{��
```
It can be our flag but cipher.

We loss some data so let's convert it into base 16 with `hexdump`

`level09@SnowCrash:~$ hexdump -C token`

66 34 6b 6d 6d 36 70 7c  3d 82 7f 70 82 6e 83 82 44 42 83 44 75 7b 7f 8c  89 0a

Let's remove the `0a` wich is the newline.

level09@SnowCrash:~$ hexdump -C token
00000000  66 34 6b 6d 6d 36 70 7c  3d 82 7f 70 82 6e 83 82  |f4kmm6p|=..p.n..|
00000010  44 42 83 44 75 7b 7f 8c  89 0a                    |DB.Du{....|
0000001a

### Reverse

-> Create a python program that takes the strings in hexadecimal, convert it in decimal in a first time and after 
apply the increment cipher.

```bash 
hex_string = "66 34 6b 6d 6d 36 70 7c 3d 82 7f 70 82 6e 83 82 44 42 83 44 75 7b 7f 8c 89" 

hex_bytes = hex_string.split(" ")
shift = 0
for byte in hex_bytes:
    decimal = int(byte, 16) - shift   # Convert hex to decimal and reverse the shift
    character = chr(decimal)          # Convert to ASCII
    print(character, end="")
    shift += 1
```

### Conclusion

It gives you the su flag09 when you execute the python program
```
-> ➜  level09 ✗ python3 decode.py
f3iji1ju5yuevaus41q1afiuq
```

```bash
level09@SnowCrash:~$ su flag09
Password: 
Don't forget to launch getflag !
flag09@SnowCrash:~$ getflag
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```