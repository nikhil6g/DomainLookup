import struct
from dataclasses import dataclass

@dataclass
class DNSAnswer:
  """
  This section contains answer section of packet.
  The answer section contains a list of RRs (Resource Records), which are answers to the questions asked in the question section.

  Each RR has the following structure:

  Field	                Type	                      Description
  Name	                Label Sequence	            The domain name encoded as a sequence of labels.
  Type	                2-byte Integer	            1 for an A record, 5 for a CNAME record etc., full list here
  Class	                2-byte Integer	            Usually set to 1 (full list here)
  TTL (Time-To-Live)	  4-byte Integer	            The duration in seconds a record can be cached before requerying.
  Length (RDLENGTH)	    2-byte Integer	            Length of the RDATA field in bytes.
  Data (RDATA)	        Variable	                  Data specific to the record type.

  In this stage, we'll only deal with the "A" record type, which maps a domain name to an IPv4 address. The RDATA field for an "A" record type is a 4-byte integer representing the IPv4 address.


  """
  name: str
  type_: int
  class_: int
  ttl: int
  rdlength: int
  rdata: str
  def pack(self):
    parts = self.name.split(".")
    name = b"".join(len(p).to_bytes(1, "big") + p.encode("ascii") for p in parts)
    name += b"\x00"
    rdata = struct.pack("!BBBB", *[int(part) for part in self.rdata.split(".")])
    return (
      name
      + struct.pack("!HHIH", self.type_, self.class_, self.ttl, self.rdlength)
      + rdata
    )
