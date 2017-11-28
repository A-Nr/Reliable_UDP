import socket
import sys
#creating sockets
if __name__ == "__main__":
    
    rdt_rcv =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udt_send=socket.socket(socket.AF_INET, socket.SOCK_DAGRAM)
    #
    listen_addr=sys.argv[1]
    listen_port=sys.argv[2]
    dest_addr = sys.argv[3]
    dest_port = int(sys.argv[4])
    rdt_rcv.bind(listen_addr,listen_port)
    #
    def ip_checksum(check):
        return 1
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
        
        if(ip_checksum(message[2:]) == checksum and ack_seq == str(seq)):
            #send (ACK,seq_number,checksum)
            udt_send.sendto(ip_checksum(data)+"ACK"+str(seq),(dest_addr,dest_port))
            #update sequence
            seq=1-seq;
        else:
            #send(ACK,wrong seq_number,checksum)
            udt_send.sendto(ip_checksum(data)+"ACK"+(1-seq),(dest_addr,dest_port))
        
        
    
    





