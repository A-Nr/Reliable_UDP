import socket
import sys
from checksum import udp_checksum
#creating sockets
#sending & reciving sockets
# socket.SOCK_DGRAM -> for UDP
rdt_rcv =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udt_send=socket.socket(socket.AF_INET, socket.SOCK_DAGRAM)
#taking listening hostname & port from the user
listen_addr=sys.argv[1]
listen_port=sys.argv[2]
#destination address& port number
dest_addr = sys.argv[3]
dest_port = int(sys.argv[4])
#Parm hostname:The hostnames to accept connections from, usually ‘’, which will accept from any host. It may also be ‘localhost’ for security reasons.
#Parm port:The port number to bind to. Must not already be in use.
##sock.bind((hostname, port))
rdt_rcv.bind((listen_addr,listen_port))

#check
seq=0
#wait from below
while True:
    #receive message from sender
    message , address = rdt_rcv.recvfrom(4096)
    #extract infromation from message
    checksum=message[:2]
    ack_seq= message[2]
    data=message[3:]
    
    if(udp_checksum(message[2:]) == checksum and ack_seq == str(seq)):
        #send (ACK,seq_number,checksum)
        udt_send.sendto(ip_checksum(data)+"ACK"+str(seq),(dest_addr,dest_port))
        #update sequence
        seq=1-seq;
    else:
        #send(ACK,wrong seq_number,checksum)
        udt_send.sendto(ip_checksum(data)+"ACK"+(1-seq),(dest_addr,dest_port))
        
        
    
    





