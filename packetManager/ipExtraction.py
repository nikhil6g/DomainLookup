import struct

def extract_ip_from_response(response_data):
    # Extract the header
    header = response_data[:12]
    _, _, _, ancount, _, _ = struct.unpack("!6H", header)  # Unpack to get Answer Count
    print(f"Number of Answers: {ancount}")

    # Skip the Question Section
    idx = 12
    while response_data[idx] != 0:  # Skip QNAME (domain name)
        idx += 1
    idx += 5  # Skip null byte, QTYPE, and QCLASS
    
    # Parse the Answer Section to extract IP addresses
    ip_addresses = []
    for _ in range(ancount):
        # Skip the Name field (could be a pointer or full domain name)
        if response_data[idx] & 0xC0 == 0xC0:  # Pointer (compressed name)
            idx += 2
        else:
            while response_data[idx] != 0:
                idx += 1
            idx += 1

        # Extract TYPE, CLASS, TTL, and RDLENGTH
        rtype, rclass, ttl, rdlength = struct.unpack("!2H1I1H", response_data[idx:idx+10])
        idx += 10

        # Extract the RDATA if it's an A record (IPv4 address)
        if rtype == 1:  # Type 1 corresponds to an A record
            ip = struct.unpack("!4B", response_data[idx:idx+4])
            ip_addresses.append('.'.join(map(str, ip)))
            idx += rdlength
        else:
            idx += rdlength

    return ip_addresses
