#!/usr/bin/env python3
import setup
import subprocess
import netfilterqueue
import atexit


class SNFQ:
    def __init__(self, process_packet_func, qnum=0, destination="forward", apache=True):
        self.qnum = qnum
        __class__.apache = apache
        if destination == "forward":
            subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(self.qnum), shell=True)
        elif destination == "sslstrip":
            subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num {}".format(self.qnum), shell=True)
            subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num {}".format(self.qnum), shell=True)
            subprocess.call("sudo iptables -t nat -A PREROUTING -p tcp"
                            " --destination-port 80 -j REDIRECT --to-port 10000", shell=True)
        elif destination == "local":
            subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num {}".format(self.qnum), shell=True)
            subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num {}".format(self.qnum), shell=True)
        else:
            raise DestinationIncorrectException
        self.queue = netfilterqueue.NetfilterQueue()
        self.bind_queue(process_packet_func, qnum)
        if __class__.apache:
            self.apache_start()
        self.run_queue()

    def bind_queue(self, process_packet_func, qnum):
        self.queue.bind(qnum, process_packet_func)

    def run_queue(self):
        print("Running a Queue...")
        self.queue.run()

    @staticmethod
    def apache_start():
        print("Starting apache2 service...")
        try:
            subprocess.check_output(["service", "apache2", "start"])
        except subprocess.CalledProcessError:
            print("Installing and starting apache2 service...")
            subprocess.call("apt-get install apache2 -y", shell=True)
            subprocess.call("service apache2 start", shell=True)
        print("Completed.")

    @staticmethod
    @atexit.register
    def exit():
        # subprocess.call("clear", shell=True)
        print("Restoring normal connections...")
        subprocess.call("iptables --flush", shell=True)
        if __class__.apache:
            subprocess.call("service apache2 stop", shell=True)
        print("Quitting.")


class DestinationIncorrectException(Exception):
    pass
