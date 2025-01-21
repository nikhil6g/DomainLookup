import threading
import json
from DNS_Parser.dnsQuery import DNSQuery
from DNS_Parser.dnsResponse import DNSResponse
from packetManager.packetCreation import create_dns_query_packet
from Server.forwardingServer import forward_query_to_google
from packetManager.ipExtraction import extract_ip_from_response

class ClientHandler(threading.Thread):
    """
    Class to handle multiple client DNS requests
    """

    def __init__(self, address, data, sock):
        threading.Thread.__init__(self)
        self.client_address = address
        self.domain = data.decode('utf-8')
        self.sock = sock

    def run(self):
        resolved_ips=[]
        dns_request = create_dns_query_packet(self.domain)
        d = DNSQuery.parse(dns_request)
        resp = DNSResponse.build_from(d)
        resolved_ips = extract_ip_from_response(resp)
        #print(dns_request)
        if not resolved_ips:
            resp = forward_query_to_google(dns_request)
            resolved_ips = extract_ip_from_response(resp)

        serialized_data = json.dumps(resolved_ips)
        self.sock.sendto(serialized_data.encode(), self.client_address)
        print(f"Domain Name: {self.domain}")
        print(f"Resolved IPs: {resolved_ips}")