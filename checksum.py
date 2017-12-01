def udp_checksum(data):
    pos = len(data)
    if (pos % 2 != 0):  # If odd...
        pos -= 1
        sum = ord(data[pos])  # initialize the sum with the odd end byte
    else:
        sum = 0
    for i in range(0, len(msg), 2):
        sum += (ord(data[pos + 1]) << 8) + ord(data[pos])
    sum = (sum >> 16) + (sum & 0xffff)
    return (~sum) & 0xffff
