import socket
import os
import sys
import subprocess

SIZE_BUFF = 10

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
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
	dataToSend = dataSizeStr + str(data) 

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
	if len(sys.argv)!= 2:
		printBorder()
		print("This progrom requires one argument specifiying the port number.")
		print("To run this program please enter:")
		print("python server.py <port_number>\n")
		print("program exiting...")
		printBorder()
		print("\n")
		exit()

	#test if port number is a number 
	if not sys.argv[1].isdigit():
		printBorder()
		print("This program requires the port number to be entered as a number.")
		print("program exiting...")
		printBorder()
		print("\n")
		exit()

	#get port number 
	portNumber = sys.argv[1]

	# default for testing
	portNumber = 1234
	#end

	#create welcome socket
	welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	welcomeSock.bind(('', portNumber))

	welcomeSock.listen(1)

	print("Waiting for connections...")
	# Accept connections forever
	command = ""
		
	# Accept connections
	controlSock, addr = welcomeSock.accept()
	print("clint address : {}".format(addr[0]))
	clientAddress = str(addr[0])
	print("Control socket initialized from client with address {}\n".format(addr))

	#maintain connect till user sends quit 
	while command != "quit":

		dataSizeBuff = ""

		dataSizeBuff = recvAll(controlSock, SIZE_BUFF)

		DataSize = int(dataSizeBuff)

		inData = recvAll(controlSock, DataSize)

		#split commond from other data 
		dataList = inData.split(" ")

		command = dataList[0]

		if(len(dataList) > 1):
				dataPort = dataList[1]
				print("Data Port Number is {}".format(dataPort))

		if(len(dataList) > 2):
				filename = dataList[2]
				print("File name is {}".format(filename))

		#output command
		print("The command is {}".format(command))

		if command == "quit":
			pass

		else:

			connectionSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			connectionSock.connect((clientAddress, int(dataPort)))

			if command == "put":

				dataSizeBuff = recvAll(connectionSock, SIZE_BUFF)

				DataSize = int(dataSizeBuff)

				inData = recvAll(connectionSock, DataSize)

				#need file validation 
				with open("ServerFile.txt", 'w') as f:
					f.write(inData)
					#need to send success or failure value

			elif command == "get":
				#need file validation 
				with open (filename, 'r') as f:
					outData = f.read()
					numSent = sendData(connectionSock, outData)
				#need to send success or failure value

			elif command == "ls":
				outData = subprocess.check_output(["ls", "-l"])
				numSent = sendData(connectionSock, outData)

				#need to send success or failure value
			else:
				pass

			connectionSock.close()

	controlSock.close()


if __name__ == '__main__':
    main()
