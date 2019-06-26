#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():  # This method designed to get arguments from terminal
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface wanted to change its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new MAC address, use --help for more info.")
    else:
        return options


def mac_changer(interface, new_mac):  # This method designed to get MAC address changing by using same console command
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):  # This method designed to get the current to compare it in next step
    result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)

    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Could not read MAC address. ")


options = get_arguments()

current_mac = get_current_mac(options.interface)  # get the old MAC Address
print("Current MAC = " + str(current_mac))

mac_changer(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)  # refresh the variable to get new MAC Address
if current_mac == options.new_mac:  # Comparing old MAC address with new MAC address
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address didn't changed")
