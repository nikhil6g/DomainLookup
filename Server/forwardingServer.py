import socket

def forward_query_to_google(query_data):
    # Google's Public DNS server address and port
    GOOGLE_DNS_IP = '8.8.8.8'
    DNS_PORT = 53
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send the query to Google's DNS server
        sock.sendto(query_data, (GOOGLE_DNS_IP, DNS_PORT))
        
        # Receive the response from Google's DNS server
        response_data, _ = sock.recvfrom(512)  # DNS responses are typically 512 bytes
        return response_data
    except Exception as e:
        print(f"Error forwarding query: {e}")
        return None
    finally:
        sock.close()
