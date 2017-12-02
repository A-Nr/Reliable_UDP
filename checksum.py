def udp_checksum(data):
    size = len(data)
    if (size % 2 != 0):  # If odd...
        size -= 1
        summation = ord(data[size])  # initialize the sum with the odd end byte
    else:
        summation = 0
    for i in range(0, size, 2):
        summation += (ord(data[i + 1]) << 8) + ord(data[i])
    summation = (summation >> 16) + (summation & 0xffff)
    return hex((~summation) & 0x0ffff)[2:]
