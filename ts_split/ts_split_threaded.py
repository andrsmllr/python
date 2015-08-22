#!/bin/python

import io
from multiprocessing.dummy import Pool as ThreadPool
import os
import struct

# RD_FILE = "./test.ts"
RD_FILE = "D:/workspace/Test/GT42/gt42_descrambling_brakes_if_gt31_muxes/parallel_streams/Polsat_GT42_out_08062015.ts"
WR_FILE = "./out/pid_"
MPEG2TS_PKT_SIZE = 188
MPEG2TS_SYNC_BYTE = 0x47

if __name__ == '__main__':
  pkt = None
  fdo = {}
  writer_pool = ThreadPool(4)
  
  # Check sync bytes.
  with open(RD_FILE, 'rb') as fdi:
    # Init.
    n_pkt = {}
    n_sync_err = {}
    pid = None
    
    pkt = fdi.read(MPEG2TS_PKT_SIZE)
    while len(pkt) == MPEG2TS_PKT_SIZE:
      
      pid = struct.unpack("!H",pkt[1:2+1])[0] & 0x1FFF
      
      # Write packet to respective output file.
      if pid in fdo.keys():
        fdo[pid].write(pkt)
      else:
        new_output_file = os.path.join(WR_FILE, str(pid), ".ts")
        fdo[pid] = open(new_output_file, 'wb')
        fdo[pid].write(pkt)
        n_pkt[pid] = 0
      
      # Check sync byte.
      if pkt[0] != MPEG2TS_SYNC_BYTE:
        n_sync_err[pid] = n_sync_err[pid]+1
      
      n_pkt[pid] = n_pkt[pid]+1
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
