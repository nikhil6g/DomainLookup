import struct

def create_dns_query_packet(domain_name):
    # Convert the domain name into DNS format (e.g., "example.com" -> "\x07example\x03com\x00")
    def encode_domain_name(name):
        parts = name.split('.')
        encoded_name = b''
        for part in parts:
            encoded_name += struct.pack('B', len(part)) + part.encode()
        return encoded_name + b'\x00'
    
    header = b'\x1d\xf1\x01 \x00\x01\x00\x00\x00\x00\x00\x01'
    lastPart = b'\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00'
    # Encode the domain name
    encoded_domain_name = encode_domain_name(domain_name)

    # Define query type and class
    qtype = struct.pack("!H", 1)  # Type A (host address)
    qclass = struct.pack("!H", 1)  # Class IN (Internet)

    # Construct the full DNS query
    query_packet = header + encoded_domain_name + qtype + qclass+lastPart
    return query_packet
