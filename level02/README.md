When we arrived 
`level02@SnowCrash:~$ ls
level02.pcap
`

pcap is packet transfert log

we ll use wireshark to read the network exchanges

If you want to copy paste the file in youre host machine you can encode it in base64 to have all the charactere even the non printable. after you can copy, paste on you host and decode it.

Once we have the level02.pcap file we can open it with wireshark.

we can filter containt of the exchange with the command 
`tcp contains '...'`
Let's try with 'Password'

-> one tcp exchange is visible. 
Then we can print all the exchanges by goind throught `Analyze` -> `Follow` -> `TCP stream`
We see a windows with the content.

PHOTO

we saw a password : ft_wandr...NDRel.L0L

But it doesn't work.

If we print the content in Hex dump we saw the correspondance of the charactere in hexa. We saw that the point is `7f`
`7f` is DEL in ASCII
So let's try to del the write and dell when writing the password.
It gives us `ft_waNDReL0L`

`level02@SnowCrash:~$ su flag02
Password: 
Don't forget to launch getflag !
flag02@SnowCrash:~$ 
`