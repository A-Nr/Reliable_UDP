import socket
from socket import timeout
import sys
#segment size
SEGMENT_SIZE = 100
if __name__ == "__main__":
    #sending & reciving sockets
    # socket.SOCK_DGRAM -> for UDP
    udt_send =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rdt_rcv  =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #causes the port to be released immediately after the socket is closed. 
    #Without this option, if you restart the program right away after a previous exit,
    # then a socket.bind() system call could fail reporting that the port is already in use.
    udt_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rdt_rcv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.bind((hostname, port))
    #taking listening hostname & port from the user
    #Parm hostname:The hostnames to accept connections from, usually ‘’, which will accept from any host. It may also be ‘localhost’ for security reasons.
    #Parm port:The port number to bind to. Must not already be in use.
    listen_addr = sys.argv[1]
    listen_port = int(sys.argv[2])
    #destination address& port number
    dest_addr   = sys.argv[3]
    dest_port   = sys.argv[4]
    #Bind to a particular port in preparation to receive connections on this port.
    rdt_rcv.bind(listen_addr,listen_port)
    # set timeout
    rdt_rcv.settimeout(1)
    offset=0
    seq=0
    content =sys.argv[5]
    #check summ function not implemented
    def ip_checksum(check):
        return 1
    #segmentation
    while offset < len(content):
        if offset + SEGMENT_SIZE > len(content):
            segment = content[offset:]
        else:
            segment = content[offset:offset + SEGMENT_SIZE]
            offset += SEGMENT_SIZE
        
        ack_received = False
        #wait for call 0 from above OR wait for call 1 from above
        while not ack_received:
            #dest port & ip
            #call to send from above occured
            #send packet with(seq-number,checksum,data) to destination
            udt_send.sendto(ip_checksum(segment)+str(seq)+segment,(dest_addr,dest_port))    
            #start timer
            #wait for ACK from right seq_number
            try:
                #receive message from receiver
                message, address = rdt_rcv.recvfrom(4096)
            except timeout:
                #exception if timeout
                    print "Timeout"
                #send again by breaking from while loop
            
            else:
                #extract information from the message
                print message
                checksum = message[:2]
                ack_seq= message[5]
                #check corrupted Or worng seq number
                #ip_checksum function to calculate checksum
                if ip_checksum(message[2:]) == checksum and ack_seq == str(seq):
                    #ready to receive the next segment
                    #go to wait for call from above state
                    ack_received = True
                
        #update sequence                    
        seq = 1 - seq
