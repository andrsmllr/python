#!/bin/python3

import io
import optparse
import os
import struct
import sys

if __name__ == '__main__':
  
  # Options and argument processing.
  parser = optparse.OptionParser()
  parser.add_option("-i", "--input_file", dest="input_file",
    help="Path to a .ts file.")
  parser.add_option("-o", "--output_file", dest="output_file",
    help="Path to output files. Suffix will be appended.")
  
  (options, args) = parser.parse_args()
  
  if options.input_file:
    rd_file = options.input_file
    fdi = None
  else:
    print("No input file specified, reading from stdin.")
    rd_file = None
    fdi = sys.stdin
  
  if options.output_file:
    wr_file = options.output_file
  else:
    if os.path.exists(os.path.join(".", "out")):
      wr_file = os.path.join(".", "out")
    else:
      os.mkdir(os.path.join(".", "out"))
      wr_file = os.path.join(".", "out")
  
  # Init.
  MPEG2TS_PKT_SIZE = 188
  MPEG2TS_SYNC_BYTE = 0x47
  fdo = {}
  n_pkt = {}
  n_sync_err = {}
  pid = None
  pkt = None
  
  # Open input file and process all MPEG2-TS packets.
  if not fdi:
    fdi = open(rd_file, 'rb')
  
  pkt = fdi.read(MPEG2TS_PKT_SIZE)
  
  # Main processing loop.
  while len(pkt) == MPEG2TS_PKT_SIZE:
    pid = struct.unpack("!H",pkt[1:2+1])[0] & 0x1FFF
    
    # Write packet to respective output file. Create new file if necessary.
    if pid in fdo.keys():
      fdo[pid].write(pkt)
    else:
      new_output_file = os.path.join(wr_file, str(pid) + ".ts")
      fdo[pid] = open(new_output_file, 'wb')
      fdo[pid].write(pkt)
      n_pkt[pid] = 0 # Incremented later.
    
    # Check sync byte.
    if pkt[0] != MPEG2TS_SYNC_BYTE:
      if pid in n_sync_err:
        n_sync_err[pid] += 1
      else:
        n_sync_err[pid] = 1
    
    n_pkt[pid] += 1
    pkt = fdi.read(MPEG2TS_PKT_SIZE)
  
  # Close input file.
  if not fdi.closed:
    fdi.close()
  
  # Close output files.
  for v in fdo.values():
    if not v.closed:
      v.close()
  
  # Print some statistics.
  for k in n_pkt:
    print("PID "+str(k)+" #packets: {0}".format(n_pkt[k]))
  for k in n_sync_err:
    print("PID "+str(k)+" #sync byte errors: {0}".format(n_sync_err[k]))
