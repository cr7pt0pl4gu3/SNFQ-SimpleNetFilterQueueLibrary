#!/usr/bin/env python3
import subprocess
import time

try:
    import netfilterqueue
    import scapy.all as scapy
except ModuleNotFoundError:
    print("Installing missing dependencies...")
    time.sleep(3)
    subprocess.call("apt-get update", shell=True)
    subprocess.call("apt-get install python3-pip git apache2 tcpdump libnfnetlink-dev libnetfilter-queue-dev -y",
                    shell=True)
    subprocess.call("pip3 install scapy --quiet", shell=True)
    subprocess.call("pip3 install -U git+https://github.com/kti/python-netfilterqueue --quiet", shell=True)
finally:
    subprocess.call("clear", shell=True)
