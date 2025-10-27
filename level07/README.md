The script level06.php contains two main functions:

y($m): replaces the characters . with x and @ with y.

Original phrase preserved: “y($m) : remplace les caractères . par x et @ par y.”

x($y, $z): reads the contents of a file, then replaces occurrences of [x some_text] with y("some_text").

Original phrase preserved: “x($y, $z) : lit le contenu d'un fichier, puis remplace les occurrences de [x some_text] par y("some_text").”

```
The challenge uses a PHP version earlier than 8.2, where the syntax ${expression} is supported. That syntax lets you evaluate an expression inside a string. When combined with backticks (`), it becomes possible to execute shell commands.
```

L'idée est de créer une chaîne comme :

`getflag`

### Exploitation steps

. Create a file /tmp/command containing the PHP code (or payload) to be evaluated.

. Pass that file as an argument to the level06.php script.

. The script replaces [x getflag] with y("getflag").

-> PHP evaluates the resulting expression, thus executing getflag and retrieving the flag.


** The key point: the /e modifier applied to preg_replace() told PHP to treat the replacement string as PHP code and to evaluate that code.

### The code line id 

```bash
level06@SnowCrash:~$ echo '[x ${`getflag`}]' > /tmp/command
level06@SnowCrash:~$ ./level06 /tmp/command
```

