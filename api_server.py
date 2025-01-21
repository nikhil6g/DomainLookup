from flask import Flask, request, jsonify
import json
import threading
from flask_cors import CORS
import socket
from Server.dnsServer import main as dns_main
from Caching.dnsCache import DNSCache

DNS_SERVER_IP = "127.0.0.1"
DNS_SERVER_PORT = 53
app = Flask(__name__)
CORS(app) 


zone_data = {}
dns_cache = DNSCache()

@app.route('/cache', methods=['GET'])
def get_cache():
    """Retrieve cache data."""
    return jsonify(dns_cache.get_all())

@app.route('/zones', methods=['GET'])
def get_zone_data():
    """Retrieve zone file data."""
    return jsonify(zone_data)

@app.route('/resolve', methods=['POST'])
def resolve_domain():
    """Resolve a domain name using the DNS server."""
    domain_name = request.json.get('domain')
    query_type = request.json.get('type', 1)
    #print(domain_name)
    if not domain_name:
        return jsonify({'error': 'Domain name is required'}), 400

     # Check the cache
    cached_result = dns_cache.get(domain_name, query_type)
    if cached_result:
        print(f"Cache HIT for domain: {domain_name} : {cached_result}")
        return jsonify({
            'domain': domain_name,
            'resolved_ips': cached_result,
            'cached': True  # Indicate that this result is from the cache
        })

    # Example resolution logic
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(domain_name.encode(), (DNS_SERVER_IP, DNS_SERVER_PORT))
    resp, _ = sock.recvfrom(650)
    resolved_ips = json.loads(resp.decode())

    if resolved_ips:
            print(f"Cache MISS. Storing result for domain: {domain_name}")
            dns_cache.set(domain_name, query_type, resolved_ips, ttl=300)  # Use default TTL
    else :
        return jsonify({'error': 'Failed to resolve domain'}), 500
    
    return jsonify({
        'domain': domain_name,
        'resolved_ips': resolved_ips,
        'cached': False  # Indicate this result is not cached
    })

    
    #Parse response as necessary (assuming it's a list of IPs here)
    #resolved_ips = resp.decode().split(",")  # Adjust parsing as per response format
    # return jsonify({'domain': domain_name, 'resolved_ips': resolved_ips})

def run_dns_server():
    """Run the DNS server in a separate thread."""
    threading.Thread(target=dns_main).start()

if __name__ == "__main__":
    run_dns_server()
    app.run(host="0.0.0.0", port=5000)
