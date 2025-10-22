# SnowCrash - 42 School Security Challenge

SnowCrash is an educational cybersecurity wargame developed by 42 School to teach students about Linux security vulnerabilities and exploitation techniques. This project consists of 14 progressive levels that simulate real-world security flaws, providing hands-on experience with various attack vectors and privilege escalation methods.


## Vulnerability Categories Exploited

##### **Injection Attacks**
- **Command Injection**: Direct execution of shell commands through unsanitized input (Perl CGI, Lua scripts, PHP code)
- **Code Injection**: Execution of arbitrary code through dynamic evaluation (`preg_replace /e` modifier in PHP)
- **Environment Variable Injection**: Manipulation of system environment variables to inject malicious commands
- **PATH Manipulation**: Hijacking executable resolution by modifying the PATH environment variable

#### **Privilege Escalation**
- **SUID/SGID Exploitation**: Leveraging Set User ID binaries to execute commands with elevated privileges

#### **Race Condition Attacks**
- **TOCTOU (Time-of-Check-Time-of-Use)**: Exploiting the gap between file access verification and actual file operation
- **Symlink Attacks**: Creating symbolic links to bypass file access restrictions during race windows

#### **Reverse Engineering & Binary Analysis**
- **Register Manipulation**: Using debuggers (GDB) to modify CPU registers and bypass security checks
- **Anti-Debug Bypass**: Circumventing ptrace detection and other anti-debugging mechanisms
- **Binary Decoding**: Analyzing and reversing custom encoding algorithms

#### **Cryptographic Reversing & Hashing Guessing Tools**
#### **Network PCAP Analysis**


## Security Best Practices & Mitigation Strategies

#### **Input Validation & Sanitization**
- **Whitelist Validation**: Always validate input against known good patterns rather than blacklisting bad ones
- **Parameterized Queries**: Use prepared statements and parameterized queries to prevent injection attacks
- **Input Encoding**: Properly encode all user input before processing or executing
- **Escape Special Characters**: Sanitize shell metacharacters in system calls

#### **Privilege Management**
- **Principle of Least Privilege**: Grant only the minimum necessary permissions required for functionality
- **SUID/SGID Auditing**: Regularly audit and minimize the use of SUID/SGID binaries
- **User Separation**: Use dedicated service accounts with restricted permissions
- **Capability-Based Security**: Prefer Linux capabilities over traditional privilege escalation

#### **File System Security**
- **Atomic Operations**: Use atomic file operations to prevent TOCTOU vulnerabilities
- **File Locking**: Implement proper file locking mechanisms for concurrent access
- **Directory Traversal Protection**: Validate and restrict file path access
- **Secure Temporary Files**: Use secure temporary file creation functions (`mkstemp()`)

#### **Code Security Practices**
- **Static Code Analysis**: Regularly scan code for security vulnerabilities
- **Dynamic Testing**: Perform runtime security testing and fuzzing
- **Security Code Reviews**: Implement mandatory security-focused code reviews
- **Dependency Management**: Keep all dependencies updated and monitor for vulnerabilities

#### **System Hardening**
- **Environment Variable Control**: Carefully manage and validate environment variables
- **Path Security**: Ensure PATH variable integrity and avoid relative paths in scripts
- **Process Isolation**: Use containers, chroot, or other isolation mechanisms
- **Anti-Debug Protection**: Implement multiple layers of anti-debugging and tampering detection


## Level Themes Summary

| Level | Theme | Description |
|-------|-------|-------------|
| **00** | Cryptographic Analysis | Caesar cipher decryption and basic cryptanalysis |
| **01** | Password Cracking | John the Ripper and hash-based authentication bypass |
| **02** | Network Forensics | PCAP analysis and network traffic credential extraction |
| **03** | PATH Manipulation | Environment variable exploitation and executable hijacking |
| **04** | Web Application Security | Perl CGI command injection via HTTP parameters |
| **05** | Cron Job Exploitation | Scheduled task privilege escalation through ACL manipulation |
| **06** | PHP Code Injection | Dynamic code evaluation vulnerability in regex replacement |
| **07** | Environment Injection | System environment variable command injection |
| **08** | Symlink Race Conditions | File access bypass using symbolic link manipulation |
| **09** | Reverse Engineering | Binary analysis and custom encoding algorithm decryption |
| **10** | TOCTOU Race Conditions | Time-of-check-time-of-use file access vulnerability |
| **11** | Lua Command Injection | Network service exploitation through script injection |
| **12** | Perl CGI Exploitation | Advanced command injection in web service parameters |
| **13** | GDB Register Manipulation | Debugger-based privilege escalation and UID spoofing |
| **14** | Anti-Debug Bypass | Binary exploitation with anti-debugging countermeasures |


## Note

This is an educational project designed to teach cybersecurity concepts in a controlled environment. All techniques should only be used for legitimate security research and learning purposes.