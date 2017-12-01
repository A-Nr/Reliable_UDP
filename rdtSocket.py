import socket
from checksum import udp_checksum
from socket import timeout

class rdtSocket:
    def __init__(self,family,soctype):
        self.sock = socket.socket(family,soctype)
        
    def sendto(self,message,receiveraddr,segmentsize=100):
        
        offset=0
        seq=0
        
        while offset < len(message):
            if offset + segmentsize > len(message):
                segment = message[offset:]
            else:
                segment = message[offset:offset + segmentsize]
                offset += segmentsize
            
            ack_received = False
            #wait for call 0 from above OR wait for call 1 from above
            while not ack_received:
                #dest port & ip
                #call to send from above occured
                #send packet with(seq-number,checksum,data) to destination
                self.sock.sendto(str(udp_checksum(str(segment)))+str(seq)+segment,receiveraddr)    
                #start timer
                #wait for ACK from right seq_number
                try:
                    #receive message from receiver
                    message, address = self.sock.recvfrom(4096)
                except timeout:
                    #exception if timeout
                        print("Timeout")
                    #send again by breaking from while loop
                
                else:
                    #extract information from the message
                    print (message)
                    checksum = message[:2]
                    ack_seq= message[5]
                    #check corrupted Or worng seq number
                    #ip_checksum function to calculate checksum
                    if udp_checksum(segment) == checksum and ack_seq == str(seq):
                        #ready to receive the next segment
                        #go to wait for call from above state
                        ack_received = True
                    
            #update sequence                    
            seq = 1 - seq
        return len(message)
        
    def recvfrom(self,buffersize):
        seq=0
        received_data = ""
        while True:
            #receive message from sender
            message , address = self.sock.recvfrom(buffersize)
            if not message:
                return (received_data,address)
            #extract infromation from message
            checksum=message[:2]
            ack_seq= message[2]
            data=message[3:]
            
            if(udp_checksum(data) == checksum and ack_seq == str(seq)):
                #send (ACK,seq_number,checksum)
                self.sock.sendto(str(udp_checksum(data))+"ACK"+str(seq),address)
                #update sequence
                seq=1-seq;
                received_data += data 
            else:
                #send(ACK,wrong seq_number,checksum)
                udt_send.sendto(str(udp_checksum(data))+"ACK"+str(1-seq),(dest_addr,dest_port))

    def close(self):
        self.sock.close()
        
    def bind(self,address):
        self.sock.bind(address)
