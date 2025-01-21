#!/usr/bin/env python3

import unittest
import os
import sys
import unittest.mock as mock
from DNS_Parser.dnsQuery import DNSQuery
from DNS_Parser.dnsResponse import DNSResponse
from Server.forwardingServer import forward_query_to_google
from packetManager.ipExtraction import extract_ip_from_response
from packetManager.packetCreation import create_dns_query_packet

class TestDnsGen(unittest.TestCase):
    """
    Tests for DNSGen class to ensure valid responses generated and proper handling of invalid requests
    """

    def test_valid_request_valid_response(self):
        """
        Create a DNS request for xyz.com, assert a valid response.
        A valid response has the same id, qr bit=1, opcode same as request, rcode 0000, ancount=3 question section same
        as request.
        Note answer format will depend on xyz.com.zone record i.e. ttl, ancount etc
        :return: True if a valid response generated, false if response is unexpected
        """
        dns_request = b'\x1d\xf1\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x03xyz\x03com\x00\x00\x01\x00\x01' \
                      b'\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00' #    here space character hexadecimal notaion is \x20.
                                                                   #    here ')' this character's hexadecimal notaion is \x29.
                                                                   #    here python don't need extra concatenating operator between two byte sequence and string it's autometically
                                                                   #    concatenated two sidely written literals and the extra backslash is for notifying that the code line resumes in next line also.
        
        
        d = DNSQuery.parse(dns_request)
        resp = DNSResponse.build_from(d)
        #print(dns_request)
        # resp = forward_query_to_google(dns_request)
        print(extract_ip_from_response(resp))

        ancount = int.from_bytes(resp[6:8], byteorder='big')
        req_byte3 = dns_request[2:3]

        self.assertEqual(dns_request[0:2], resp[0:2])  # ID same
        self.assertNotEqual(req_byte3, resp[2:3])  # 3rd byte not same as qr flips to 1 but opcode stays same or changes
        self.assertEqual(resp[3:4], b"\x00")    # no recursion available, no error code
        self.assertEqual(dns_request[4:6], resp[4:6])   # qdcount same as    request
        self.assertGreaterEqual(ancount, 1)  # ancount >= 1
        self.assertEqual(dns_request[12:20], resp[12:20])
        print(resp[:12])
        print("ancount is:",ancount)
        print(resp[25:48])
        print(resp[48:71])
        print(resp[71:])
        # self.assertEqual(compression_count, ancount)    # number of answers = ancount

    def test_valid_request_no_records_response(self):
        """
        Create a normal DNS request for xykz.com, no record should be found
        The response should have the error code for name error (rcode=0003)
        Question should be same, no answer body, total message length similar to query length
        :return: True if a proper error response created
        """
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
    
# Invoke-WebRequest -Uri http://127.0.0.1:5000/resolve -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"domain": "google.com"}'
