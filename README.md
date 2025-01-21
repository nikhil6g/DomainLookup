# DNS Resolver

This project mimics the core functionalities of a recursive DNS resolver. It includes both a backend server implemented in Python and a frontend interface using HTML and CSS.

## Features

1. **Domain Name Resolution**: The backend resolves domain names and sends the results to the frontend via a REST API.
2. **Authoritative DNS Server**: Mimics an authoritative DNS server for specific domains.
3. **Recursive DNS Server**: Uses Google's DNS server to fetch IPs for other domains.
4. **Caching**: Caches already fetched resolutions to improve performance.
5. **Concurrency**: Uses threading to handle multiple users simultaneously.

## Setup and Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python packages:

   ```sh
   pip install flask flask-cors
   ```

3. Run the DNS server and API server:

   ```sh
   python api_server.py
   ```

4. Open [index.html](http://_vscodecontentref_/16) in your web browser to access the frontend interface.

## Usage

1. Enter a domain name in the input field and click "Get IP Addresses".
2. The frontend will send a request to the backend to resolve the domain name.
3. The resolved IP addresses will be displayed on the frontend.

## Files and Directories

- **`api_server.py`**: The main API server using Flask.
- **[Caching/dnsCache.py](http://_vscodecontentref_/17)**: Implements caching for DNS resolutions.
- **[DNS_Parser](http://_vscodecontentref_/18)**: Contains modules for parsing DNS packets.
- **[packetManager](http://_vscodecontentref_/19)**: Contains modules for creating DNS query packets and extracting IPs from responses.
- **[Server](http://_vscodecontentref_/20)**: Contains the DNS server and client handler modules.
- **[Zone_Handler](http://_vscodecontentref_/21)**: Handles zone file data.
- **`Zones/xyz.com.zone`**: Example zone file.
- **`index.html`**: Frontend interface for resolving domain names.
- **`test_dns_generator.py`**: Unit tests for the DNS generator.
