# Level 09

## Summary

In this level, we have access to the encoded token and to the binary that encoded it. By reverse engineering research on the binary, we can create a script to decode the token and get the flag.

## Workflow

1. List the files in the home directory. The binary is SUID and the token file is readable by the user.
	```
	level09@SnowCrash:~$ ls -l
	total 12
	-rwsr-sr-x 1 flag09 level09 7640 Mar  5  2016 level09
	----r--r-- 1 flag09 level09   26 Mar  5  2016 token
	```

2. Read the token file. It seems to be encoded.
	```
	level09@SnowCrash:~$ cat token
	f4kmm6p|=�p�n��DB�Du{��
	```

3. Run the binary without argument to see how it behaves.
	```
	level09@SnowCrash:~$ ./level09
	You need to provied only one arg.
	```

4. Run the binary with a long argument to see how it transforms the input. It seems to add the index of each byte to its value (mod 256).
	```
	./level09 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
	abcdefghijklmnopqrstuvwxyz{|}~��������������������������������������������������������������������������������������������������������������������������������


	�123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abc
	```

	```
	./level09 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | wc -c
	260
	```

5. Copy the token of the VM to the host machine. Create a python script to decode the token by reversing the transformation (subtracting the index to each byte value).
	```
	➜  level09 git:(aautin) ✗ scp -P 4242 level09@192.168.56.101:/home/user/level09/token token
		_____                      _____               _     
		/ ____|                    / ____|             | |    
		| (___  _ __   _____      _| |     _ __ __ _ ___| |__  
		\___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
		____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
		|_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
															
	Good luck & Have fun

			192.168.56.101 
	level09@192.168.56.101's password: 
	token                                              100%   26    12.5KB/s   00:00
	```

	```
	➜  level09 git:(aautin) ✗ chmod 666 token 
	```

6. Use the script I made to decode the token.
	```
	python3 decoder.py
	byte_values: [102, 52, 107, 109, 109, 54, 112, 124, 61, 130, 127, 112, 130, 110, 131, 130, 68, 66, 131, 68, 117, 123, 127, 140, 137, 10]
	0: 102 - 0 = 102 ('f')
	1: 52 - 1 = 51 ('3')
	2: 107 - 2 = 105 ('i')
	3: 109 - 3 = 106 ('j')
	4: 109 - 4 = 105 ('i')
	5: 54 - 5 = 49 ('1')
	6: 112 - 6 = 106 ('j')
	7: 124 - 7 = 117 ('u')
	8: 61 - 8 = 53 ('5')
	9: 130 - 9 = 121 ('y')
	10: 127 - 10 = 117 ('u')
	11: 112 - 11 = 101 ('e')
	12: 130 - 12 = 118 ('v')
	13: 110 - 13 = 97 ('a')
	14: 131 - 14 = 117 ('u')
	15: 130 - 15 = 115 ('s')
	16: 68 - 16 = 52 ('4')
	17: 66 - 17 = 49 ('1')
	18: 131 - 18 = 113 ('q')
	19: 68 - 19 = 49 ('1')
	20: 117 - 20 = 97 ('a')
	21: 123 - 21 = 102 ('f')
	22: 127 - 22 = 105 ('i')
	23: 140 - 23 = 117 ('u')
	24: 137 - 24 = 113 ('q')
	Decoded token: f3iji1ju5yuevaus41q1afiuq
	```

7. Connect to the flag09 account using the retrieved token, then run getflag.
	```
	flag09@192.168.56.101's password: 
	Don't forget to launch getflag !
	flag09@SnowCrash:~$ getflag
	Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
	```


