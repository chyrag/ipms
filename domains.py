#!/usr/bin/env python

import gevent
from gevent import socket as gsock
import random
import string
import os

"""
The idea is to generate

"""

if __name__ == "__main__":
    os.makedirs("output")
    os.chdir("output")
    for i in range(10000):
        domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + ".com"
