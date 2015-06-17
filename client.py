import socket
import os
import sys
import subprocess

SIZE_BUFF = 10

def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += str(tmpBuff, 'UTF-8')
	
	return recvBuff

def sendData(sendSocket, data):
	#create header value for size of data being sent
	dataSizeStr = str(len(data))

	#append '0' in order to make header 10 bytes
	while len(dataSizeStr) < SIZE_BUFF:
		dataSizeStr = "0" + dataSizeStr

	#append header to data
	dataToSend = dataSizeStr + data 

	print("data to send is {}".format(dataToSend))

	numSent = 0

	#send data 
	dataToSend = bytes(dataToSend, 'UTF-8')
	while len(dataToSend) > numSent:
		numSent += sendSocket.send(dataToSend[numSent:])

	return numSent


def printBorder():
	print("***********************************************************************")

	return

def main():
	#test for number of arguments
	if len(sys.argv)!= 3:
		printBorder()
		print("This progrom requires two arguments:.")
		print("To run this program please enter:")
		print("python client.py <server_machine> <server_port>\n")
		print("program exiting...")
		printBorder()
		print("\n")
		exit()
	#test if port number is a number 
	if not sys.argv[2].isdigit():
		printBorder()
		print("This program requires the port number to be entered as a number.")
		print("program exiting...")
		printBorder()
		print("\n")
		exit()

	#assign address and port number 
	serverAddress = sys.argv[1]
	serverPort = sys.argv[2]

	#for testing 
	serverAddress = "localhost"
	serverPort = 1234
	#end

	connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#connect to server 
	connSock.connect((serverAddress, serverPort))

	command = ""

	#continute to prompt for input till user enters quit
	while command != "quit":

		filename = None
		
		#prompt for user
		data = input("ftp> ")

		#validate data was entered
		if len(data) > 1:

			#seperate commands from other input	
			dataList = data.split(" ")

			command = dataList[0]
			
			if(len(dataList) > 1):
				filename = dataList[1]

			commandForSend = ["get", "put", "ls", "quit"]
			commandToRecev = ["get", "put", "ls"]

			if command in commandForSend:

				if command in commandToRecev:

					#initialize Data Socket
					dataListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					dataListen.bind(('', 0))
					dataPort = dataListen.getsockname()[1]

					print("Data port is {}".format(dataPort))

					data = command + " " + str(dataPort)
					
					if filename:
						data += " "
						data += filename
					
					numSent = sendData(connSock, data)

					dataListen.listen(1)

					print("Waiting for connections...")

					dataSock, addr = dataListen.accept()
					
					data = ""
					dataSizeBuff = ""
					inData = " "

					if command == "put":

						with open (filename, 'r') as f:
							data = f.read()
							numSent = sendData(dataSock, data)

					elif command == "get":

						dataSizeBuff = recvAll(dataSock, SIZE_BUFF)

						DataSize = int(dataSizeBuff)

						inData = recvAll(dataSock, DataSize)

						with open("incoming_file", 'w') as f:
							f.write(inData)

					else:

						dataSizeBuff = recvAll(dataSock, SIZE_BUFF)

						DataSize = int(dataSizeBuff)

						inData = recvAll(dataSock, DataSize)

						print(str(inData))

					dataSock.close()

				else:
					numSent = sendData(connSock, data)

				print("Number of bytes sent : {}".format(numSent))


			elif command == "lls":
				subprocess.call(["ls", "-l"])
			elif command == "":
				pass

			else:
				print("Command not found")
				print("Commands are: get, put, ls, lls, quit")

	connSock.close()

if __name__ == '__main__':
    main()