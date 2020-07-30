#   Copyright 2020 Lunarixus
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import random
import socket
import sys
import threading
import os.path
import time
import urllib.request
import json

print("""

     _______.  ______     ___      .__   __. .__   __. ____    ____ 
    /       | /      |   /   \     |  \ |  | |  \ |  | \   \  /   /   
   |   (----`|  ,----'  /  ^  \    |   \|  | |   \|  |  \   \/   /     
    \   \    |  |      /  /_\  \   |  . `  | |  . `  |   \_    _/       
.----)   |   |  `----./  _____  \  |  |\   | |  |\   |     |  |        
|_______/     \______/__/     \__\ |__| \__| |__| \__|     |__|        
 
- A simple Python-written mass scanner tool

Warning: This program is only for educational use and research only!

""")

#
# Change the ports you'd like to scan here
#
ports = (["80"])

def ping(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remoteServerIP = socket.gethostbyname(ip)
        sock.settimeout(3)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print("[*] Host is up!")
            return 0
        else:
            print("[!] Host does not have port %s open!" % port)
            return 1
    except:
        return 1

def getservice(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((ip, port))
        if(result == 0):
            service = s.recv(256).decode('utf-8').strip("\n").strip("\r")
            return service
        else:
            return 'Unknown'
    except:
        return 'Unknown'

def generateresultsfile():
    file = open("SCANNY_RESULTS.txt", "a+")
    file.write("This file was generated by:")
    file.write("\n\n")
    file.write("""     _______.  ______     ___      .__   __. .__   __. ____    ____  \n""")
    file.write("""    /       | /      |   /   \     |  \ |  | |  \ |  | \   \  /   /  \n""")
    file.write("""   |   (----`|  ,----'  /  ^  \    |   \|  | |   \|  |  \   \/   /   \n""")
    file.write("""    \   \    |  |      /  /_\  \   |  . `  | |  . `  |   \_    _/    \n""")
    file.write(""".----)   |   |  `----./  _____  \  |  |\   | |  |\   |     |  |      \n""")
    file.write("""|_______/     \______/__/     \__\ |__| \__| |__| \__|     |__|      \n""")
    file.write("""                                                                     \n""")
    file.write("""- A simple Python-written mass scanner tool                          \n""")
    file.write("""                                                                     \n""")
    file.write("""    Warning: This program is only for educational use and research only!      \n""")
    file.write("\n")
    file.write("\n")
    file.write("IP                    Port        Service (if detected)   ISP                                Country\n\n")
    file.close()
    

def saveip(ip, port, service, isp, country):
    file = open("SCANNY_RESULTS.txt", "a+")
    file.write(str(ip))
    file.write("          ")
    file.write(str(port))
    file.write("          ")
    file.write(str(service))
    file.write("          ")
    file.write(str(isp))
    file.write("          ")
    file.write(str(country))
    file.write("\n")

def parseipinformation(data):
    data = json.loads(data)
    isp = data["isp"]
    country = data["country"]
    return isp, country

def getipinformation(ip):
    url = "http://ip-api.com/json/%s" % ip
    request = urllib.request.urlopen(url)
    data = request.read()
    isp, country = parseipinformation(data)
    return isp, country

def genandcheck(ports):
    while True:
        ip = "{0}.{1}.{2}.{3}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        print("[*] Generated IP is:", ip)
        for port in ports:
            print("[*] Testing for port %s..." % port)
            returnval = ping(ip, int(port))
            if returnval == 0:
                print("[*] Generated IP %s has ports open!" % ip)
                service = getservice(ip, int(port))
                isp, country = getipinformation(ip)
                saveip(ip, port, service, isp, country)
                break

threads = int(input("How many threads do you wanna run? "))

if str(os.path.exists("SCANNY_RESULTS.txt")) != "True":
        print("[!] Results file does not exist!")
        print("[*] Generating results file...")
        generateresultsfile()

for makenewthread in range(0, threads):
    t = threading.Thread(target=genandcheck, args=([ports]))
    t.start()
