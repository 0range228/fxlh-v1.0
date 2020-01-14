import socket
import time
from time import sleep
import datetime
import re
import logging
import argparse
import socket
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, wait
import importlib,sys
from PyQt5.QtWidgets import *
#logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",filename="log/logs", filemode="a")
DEBUG = False

class PortScan:
    def __init__(self):
        self._LOGS = Queue()
# 判断ip地址输入是否符合规范
    def check_ip(self,ipAddr):
        compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(ipAddr):
            return True
        else:
            return False

    def PortScanner(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            QApplication.processEvents()
            self.print_logs(" [+] " + str(host) + ":" + str(port) + " is opened.")
            QApplication.processEvents()
            s.close
        except Exception as e:
            pass

    def CPortScan(self, ip):
        if self.check_ip(ip):
            ip = str(ip)
        else:
            self.print_logs(" [*] " + "扫描失败，IP地址输入错误")
            exit(1)
        self.print_logs(" [*] " + "开始常规端口扫描")
        port = [21, 22, 23, 25, 53, 69, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 110, 135, 139, 143, 443, 445, 465, 993,
                995, 1080, 1158, 1433, 1521, 1863, 2100, 3128, 3306, 3389, 7001, 8080, 8081, 8082, 8083, 8084, 8085,
                8086, 8087, 8088, 8888, 9080, 9090]
        start_time = datetime.datetime.now()
        for p in port:
            t = threading.Thread(target=self.PortScanner, args=(ip, p))
            sleep(0.001)
            t.start()
        end_time = datetime.datetime.now()
        cost_time = (end_time - start_time).microseconds
        print("扫描完成,用时:", cost_time)
        return cost_time

    def FPortScan(self, ip):
        if self.check_ip(ip):
            ip = str(ip)
        else:
            self.print_logs(" [*] " + "扫描失败，IP地址输入错误")
            exit(1)
        self.print_logs(" [*] " + "开始全部端口扫描")

        while True:
            if ip:
                start_time = datetime.datetime.now()
                executor = ThreadPoolExecutor(max_workers=700)
                QApplication.processEvents()
                t = [executor.submit(self.PortScanner ,ip, n) for n in range(1, 65536)]
                QApplication.processEvents()
                if wait(t, return_when='ALL_COMPLETED'):
                    end_time = datetime.datetime.now()
                    QApplication.processEvents()
                    cost_time = (end_time - start_time).seconds
                    print("扫描完成,用时:", cost_time)
                    break

        return cost_time


    def print_logs(self, msg):
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()) + msg)
        logging.info(msg)
        self._LOGS.put(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()) + msg)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('[*] Try to use -h or --help show message')
        exit(1)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''use examples:
            python postscanner.py -i 192.168.1.1
            python postscanner.py -ip 192.168.1.1
            python postscanner.py -i 192.168.1.1 -a
            python postscanner.py -ip 192.168.1.1 -all 
            ''')
    parser.add_argument('-i', '--ip', metavar='', dest="ip",
                        help='The IP address that needs to be scanned for the port.')
    parser.add_argument('-a', '--all', action="store_true", dest="all",
                        help='Full port scan mode.')
    options = parser.parse_args()
    portscan = PortScan()
    if options.all:
        portscan.FPortScan(ip=options.ip)
    else:
        portscan.CPortScan(ip=options.ip)