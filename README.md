# PortForce

A Custom Port Brute Force Tool created for use in CTF's and Pentests.

<a href="https://raw.githubusercontent.com/jhalon/jhalon.github.io/master/images/port_force.png"><img src="https://raw.githubusercontent.com/jhalon/jhalon.github.io/master/images/port_force.png"></a>

Yes, there are a lot of tools out there that do Brute Force for Telnet, SSH, FTP, etc.

This tool was created to aid in brute forcing custom ports/dameons that don't typically run on SSH, FTP, etc.

## Install:

You can install PortForce by cloning this Git Repository

```console
$ git clone https://github.com/jhalon/PortForce.git
```

## Usage:

```console
Usage: ./port_force -t 192.168.0.1 -p 1234 -u users.txt -P pass.txt

-h --help            - display usage information
-t --target          - set IP address of Target
-p --port            - set Port for Target
-u --user           - set a list of usernames to brute force
-F --pass            - set a list of passwords to brute force
```

## Requirements:

Since this was created using Python v2.7.13 it will not be compatible with Python v3.x.

* Python v2.7.13 - [Download](https://www.python.org/downloads/release/python-2713/)

## Bugs?

* Please Submit a new Issue
* Submit a Pull Request
* Contact me
