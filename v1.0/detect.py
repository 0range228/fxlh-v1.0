import requests
import importlib,sys,os
import subprocess

import binascii
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
importlib.reload(sys)
from PyQt5.QtWidgets import *
sys.path.append("./ysoserial-0.0.6-SNAPSHOT-all.jar")

class VulDetect:
    def __init__(self):
        self._LOGS = Queue()
    def GeneratePayload(self):
        str1 = 'java -jar verify_CVE-2017-12149.jar '
        os.system('java -jar verify_CVE-2017-12149.jar ')


