import socket
from checksum import udp_checksum
from socket import timeout

class rdtSocket:
    def __init__(self,family,soctype):
        self.sock = socket.socket(family,soctype)
        
    def sendto(self,message,receiveraddr,segmentsize=100):
        
        offset=0
        seq=0
        self.sock.settimeout(10)
        message = message.decode('UTF-8') + "_END_"
        
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
                #send packet with(checksum,seq-number,data) to destination
                packet_send = str(udp_checksum(segment)) + str(seq) + segment
                self.sock.sendto(packet_send.encode('UTF-8'),receiveraddr)    
                #start timer
                #wait for ACK from right seq_number
                try:
                    #receive ackmessage from receiver
                    ackmessage, address = self.sock.recvfrom(2048)
                except timeout:
                    #exception if timeout
                        print("Timeout")
                    #send again by breaking from while loop
                        continue
                
                #extract information from the ackmessage
                ackmessage = ackmessage.decode('UTF-8')
                #print (ackmessage)
                checksum = ackmessage[:4]
                ack_seq= ackmessage[7]
                #check corrupted Or worng seq number
                #ip_checksum function to calculate checksum
                if udp_checksum(segment) == checksum and ack_seq == str(seq):
                    #ready to receive the next segment
                    #go to wait for call from above state
                    ack_received = True
                
            #update sequence                    
            seq = 1 - seq
        self.sock.settimeout(None)
        return len(message)
        
    def recvfrom(self,buffersize):
        seq=0
        received_data = ""
        while True:
            if received_data[-5:None:1] == "_END_":
                return ((received_data[0:len(received_data)-5]).encode('UTF-8'),address)
            #receive message from sender
            message , address = self.sock.recvfrom(buffersize)
            #extract infromation from message
            message = message.decode('UTF-8')
            checksum = message[:4]
            ack_seq = message[4]
            data = message[5:]
            
            if(udp_checksum(data) == checksum and ack_seq == str(seq)):
                #send (ACK,seq_number,checksum)
                ack_send = checksum + "ACK" + str(seq)
                self.sock.sendto(ack_send.encode('UTF-8'),address)
                #update sequence
                seq=1-seq;
                received_data += data 
            else:
                #send(ACK,wrong seq_number,checksum)
                ack_send = str(udp_checksum(data)) + "ACK" + str(1-seq)
                self.sock.sendto(ack_send.encode('UTF-8'),address)

    def close(self):
        self.sock.close()
        
    def bind(self,address):
        self.sock.bind(address)
