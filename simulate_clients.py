#!/usr/bin/env python


"""The idea is to simulate test load on IPMS security system, by creating given
number of clients, where each client will try to upload readings, images every n
seconds. The readings are randomly generated, and images are taken from a
directory randomly."""

import argparse
import gevent
from gevent import socket
from gevent.pool import Pool
import random

""" Simulate a client """
def simulate_client(clientid):
    pass


""" Simulate load on the server """
def simulate_load(clients, interval, imgdir):
    print "Simulating %d clients uploading data every %d seconds from %s" % (args.clients, args.interval, args.imgdir)
    pool = Pool(clients)
    for clientid in range (clients):
        pool.spawn(simulate_client, clientid)
    pool.join()


""" Start here """
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulate test conditions for IPMS security system')
    parser.add_argument('--imgdir', required=True,
                        help='Directory from where images will be picked up')
    parser.add_argument('--clients', type=int, required=False, default=10,
                        help='Number of clients to simulate')
    parser.add_argument('--interval', type=int, required=False, default=30,
                        help='Number of seconds to wait between uploading data')
    args = parser.parse_args()
    simulate_load(args.clients, args.interval, args.imgdir)
