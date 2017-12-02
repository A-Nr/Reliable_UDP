import socket
import rdtSocket


serverName = 'localhost'
serverPort = 12000

clientSocket = rdtSocket.rdtSocket(socket.AF_INET,socket.SOCK_DGRAM)

message = input('Input lowercase sentence: ')

clientSocket.sendto(message.encode('UTF-8'),(serverName, serverPort))

data, serverAddress = clientSocket.recvfrom(2048)

print (data.decode('UTF-8'))

clientSocket.close()

message=input('Press enter to exit')
