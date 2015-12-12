#!/bin/python3
##############################################################################
# cap2ts.py:
# cap2ts extracts the MPEG2-TS packet from a Wireshark capture file and stores
# them in a .ts file.
# An IP destination address and UDP destination port can be specified to store
# only the MPEG2-TS packets of a specific stream.
#
# TODO /  known issues:
# - add filtering by Eth. MAC address (low prio since this is seldomly used).
# - no VLAN support, but this shouldn't be a problem anyway since most NICs
#   strip the VLAN tag before handing a frame to the OS (or s/t like that).
# - only .cap files supported so far, all other file extensions are treated
#   as is they were pcap(ng) files.
##############################################################################

import io # Read and write from/to files.
from optparse import OptionParser # Parse command line arguments.
import os # Path handling.
import struct # Unpacking of binary data.
import sys # Exit program in a clean way.

if __name__ == '__main__':
  
  HOST_ANY = '0.0.0.0'
  HOST_IP_ANY = [0, 0, 0, 0]
  PORT_ANY = 0
  MPEG2TS_PKT_LEN = 188
  
  # Parse command line arguments.
  # Set up command line argument parser.
  parser = OptionParser(epilog="Example: pcap2ts -o out.ts -d 227.1.2.3 -p 1234 in.cap")
  # parser.add_option("-i", "--input_file", dest="input_file",
    # help="Path to .cap or .pcap input file.")
  parser.add_option("-o", "--output_file", dest="output_file",
    help="Path to .ts output file. If file exists it will be replaced.")
  parser.add_option("-d", "--dst_host", dest="dst_host",
    help="Destination host IPv4 address. Defaults to any.")
  parser.add_option("-p", "--port", dest="port",
    help="Destination UDP port. Defaults to any.")
  # parser.add_option("-h", "--help", dest="help",
    # help="Usage: pcap2ts -o out.ts -d 227.1.2.3 -p 1234 in.cap.")
  
  # Parse command line arguments.
  (options, args) = parser.parse_args()
  
  # Store command line arguments in variables.
  if len(args) > 0:
    file_rd = args[0]
    # Split file name into base name and extension.
    # File extension is used to conclude which capture file format is used.
    file_rd_name, file_rd_ext = os.path.splitext(file_rd)
  else:
    print("No input file specified, reading from stdin assuming a .cap file.")
    file_rd_name, file_rd_ext = ('cap2ts', '.cap')
    # To read binary data from stdin the underlying buffer must be used.
    fdrd = sys.stdin.buffer
  # if options.input_file:
    # file_rd = options.input_file
  # else:
    # print("No input file specified, exiting.")
    # sys.exit(2)
  if options.output_file:
    file_wr = options.output_file
  else:
    print("No output file specified, assuming <in file>.ts.")
    file_wr = "./{0}.ts".format(file_rd_name)
  if options.dst_host:
    host = options.dst_host
    host_ip = str.split(host.strip(), ".")
    if len(host_ip) == 4:
      for i in range(0, len(host_ip)):
        host_ip[i] = int(host_ip[i])
        if host_ip[i] < 0 or host_ip[i] > 255:
          print("Invalid destination host address.")
          sys.exit(2)
    else:
      print("Invalid destination host address.")
      sys.exit(2)
  else:
    print("No destination host specified, assuming any.")
    host = HOST_ANY
    host_ip = HOST_IP_ANY
  if options.port:
    port = int(options.port)
    if port < 0 or port > 65535:
      print("Invalid port.")
      sys.exit(2)
  else:
    print("No port specified, assuming any.")
    port = PORT_ANY
  
  # Open input file.
  if not fdrd:
    try: fdrd = open(file_rd, 'rb')
    except Exception as e:
      print("Could not open input file.")
      sys.exit(1)
  
  # Open output file.
  try: fdwr = open(file_wr, 'wb')
  except Exception as e:
    print("Could not open output file.")
    print(e)
    sys.exit(1)
  
  # Read global header depending on file extension.
  if (file_rd_ext == ".cap"):
    # .cap global header.
    pcap_gh_magic_number = struct.unpack("<I", fdrd.read(4))[0]
    pcap_gh_version_major = struct.unpack("H", fdrd.read(2))[0]
    pcap_gh_version_minor = struct.unpack("H", fdrd.read(2))[0]
    pcap_gh_thiszone = struct.unpack("i", fdrd.read(4))[0]
    pcap_gh_sigfigs = struct.unpack("I", fdrd.read(4))[0]
    pcap_gh_snaplen = struct.unpack("I", fdrd.read(4))[0]
    pcap_gh_network = struct.unpack("I", fdrd.read(4))[0]
  elif (file_rd_ext == ".pcap"):
    # .pcap header.
    fdrd.seek(fdrd.tell() + 306)
  else:
    print("Unsupported file format (wrong file extension).")
    sys.exit(1)
  
  n_frame = 1
  
  # Main loop.
  while (fdrd.peek(1) != b''):
    # Initialize current file position and read count.
    pcap_rh_start = fdrd.tell()
    cnt = 0
    
    # Read record header.
    if (file_rd_ext == ".cap"):
      pcap_rh_ts_sec = struct.unpack("I", fdrd.read(4))[0]
      pcap_rh_ts_usec = struct.unpack("I", fdrd.read(4))[0]
      pcap_rh_ts_incl_len = struct.unpack("I", fdrd.read(4))[0]
      pcap_rh_ts_orig_len = struct.unpack("I", fdrd.read(4))[0]
    else:
      # TODO: The static skip of 18 is no clean solution.
      # The pcapng file format should be parsed correctly.
      fdrd.read(18)
      pcap_rh_ts_sec = struct.unpack("I", fdrd.read(4))[0]
      pcap_rh_ts_usec = struct.unpack("I", fdrd.read(4))[0]
      pcap_rh_ts_incl_len = struct.unpack("I", fdrd.read(4))[0]
      pcap_rh_ts_orig_len = struct.unpack("I", fdrd.read(4))[0]
    
    # Read Ethernet and IP header (no VLAN assumed).
    eth_mac_dst = fdrd.read(6)
    eth_mac_src = fdrd.read(6)
    eth_ethertype = fdrd.read(2)
    ip_header = fdrd.read(12)
    ip_protocol = ip_header[9]
    ip_src = fdrd.read(4)
    ip_dst = fdrd.read(4)
    cnt += 34
    
    # Filter by IP destination address.
    if not (ip_dst == bytes(host_ip) or host_ip == HOST_IP_ANY):
      # Skip this frame by skipping the frame length plus the record header.
      if (file_rd_ext == ".cap"):
        fdrd.seek(pcap_rh_start + pcap_rh_ts_incl_len + 16)
      else:
        fdrd.seek(pcap_rh_start + pcap_rh_ts_incl_len + 34)
      continue
      
    # Read UDP header.
    udp_header = fdrd.read(8)
    udp_dst_port = udp_header[0:2]
    udp_src_port = udp_header[2:4]
    cnt += 8
    protocol = "UDP"
    
    # Filter by UDP destination port.
    if not (struct.unpack("!H", udp_dst_port) == port or port == PORT_ANY):
      # Skip this frame by skipping the frame length plus the record header.
      if (file_rd_ext == ".cap"):
        fdrd.seek(pcap_rh_start + pcap_rh_ts_incl_len + 16)
      else:
        fdrd.seek(pcap_rh_start + pcap_rh_ts_incl_len + 34)
      continue
    
    # Skip RTP header if necessary.
    if (fdrd.peek(2)[0:2] == b'\x80\x21'):
      rtp_header = fdrd.read(12)
      cnt += 12
      protocol = "RTP"
    
    # Read MPEG2-TS packets and dump them to output file.
    while (cnt < pcap_rh_ts_incl_len):
      ts_pkt = fdrd.read(MPEG2TS_PKT_LEN)
      # Do not store partial MPEG2-TS packets.
      if len(ts_pkt) == MPEG2TS_PKT_LEN:
        fdwr.write(ts_pkt)
      cnt += MPEG2TS_PKT_LEN
    
    n_frame += 1
    
  # Clean up and exit.
  if not fdrd.closed:
    fdrd.close()
  if not fdwr.closed:
    fdwr.close()
  
  print("Done.")
  