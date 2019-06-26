#!/usr/bin/env python
import subprocess
import optparse
import re


def monitor_mode(interface):
    print("[+]Changing " + interface + " to monitor mode")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["airmon-ng", "check", "kill"])
    subprocess.call(["iwconfig", interface, "mode", "monitor"])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter interface to change its mode")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    else:
        return options


def checkER(interface):
    result = subprocess.check_output(["iwconfig", interface])
    correct_result = re.search(r"Mode:Monitor", result)
    if correct_result:
        print("[+] " + interface + " has changed to monitor mode successfully.")
    else:
        print("[-] Sorry " + interface + " didn't changed , check your interface. ")


options = get_arguments()
monitor_mode(options.interface)
checkER(options.interface)
