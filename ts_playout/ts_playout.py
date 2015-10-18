##############################################################################
# \file ts_playout.py
#
# \date 2015-03-17
#
# \author Andreas
#
# \brief Play out a transport stream from a file over IPv4.
#
# \details
#
##############################################################################

import getopt; # getopt.parse().
import io; # file.open(), file.read(), file.close().
import os; # os.exit().
import signal; # signal.signal(), signal.SIGINT.
import socket; # socket.socket(), socket.send().
import struct; # struct.pack().
import sys; # sys.stderr.write().
import time; # time.sleep().

##############################################################################
# Global variable definitions.
##############################################################################

#FILENAME = '/home/andreas/Videos/football.ts';
FILENAME = '/home/andreas/Videos/bigbuckbunny.ts';
HOST_IPV4 = '239.0.0.0';
HOST_PORT = 1234;
SRC_PORT = 1234;
MPEG2TS_PER_IP = 7;
MPEG2TS_PKTLENGTH = 188;
MPEG2TS_BITRATE = 10e6;
MPEG2TS_PKTRATE = MPEG2TS_BITRATE/(MPEG2TS_PKTLENGTH*8);
MPEG2TS_PKTINTRVL = 1/MPEG2TS_PKTRATE;
MPEG2TS_DRPRATE = 0.0
UDP_PKTRATE = MPEG2TS_PKTRATE/MPEG2TS_PER_IP;
UDP_PKTINTRVL = 1/UDP_PKTRATE;
UDP_DRPRATE = 0.01;
RTP_ENABLE = True;
RTP_SN = 0;
LOOP_FILE = True;

##############################################################################
# Class definitions.
##############################################################################

class TsPlayoutError(Exception):
    def __init__(self):
        super.__init__();
    def __str__(self):
        return super.__str__(self);

##############################################################################
# Function definitions.
##############################################################################

def open_ts_file(filename):
    """
    Open a TS file for bytewise reading.
    """
    FP = None;
    try:
        FP = open(filename, 'rb');
    except Exception as e:
        sys.stderr.write("Error opening file.");
        raise;
    finally:
        return FP;

def sync_ts_file(FP):
    """
    Synchronize to MPEG2 transport stream sync byte.
    E.g. in case of meta header on *.ts file.
    """
    try:
        while (not(struct.unpack('B', FP.read(1))) == struct.unpack('B', b'\x47')):
            pass;
        FP.seek(-1, io.SEEK_CUR);
    except:
        sys.stderr.write("Error synchronizing TS file.");
        raise;
    finally:
        return FP;

# Function to handle exit by Ctrl-C.
def interrupt_handler(signal, frame):
    print("\nAborted due to user request.")
    sys.exit(0)

##############################################################################
# Main.
##############################################################################

if (__name__ == "__main__"):
    
    # Set interrupt handler for graceful exit on Ctrl-C.
    signal.signal(signal.SIGINT, interrupt_handler)

    print("Starting.")
    
    TsFile = open_ts_file(FILENAME);
    
    try:
        TsSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    except Exception as e:
        sys.stderr.write("Error opening socket.");
        raise;
    
    try:
        TsSocket.connect((HOST_IPV4, HOST_PORT));
    except Exception as e:
        sys.stderr.write("Error connecting socket.");
        raise;
    
    sync_ts_file(TsFile);
    
    while (True):
        mpeg2ts_data = b'';
        udp_data = b'';
        
        try:
            mpeg2ts_data = TsFile.read(MPEG2TS_PKTLENGTH*MPEG2TS_PER_IP);
            if (len(mpeg2ts_data) < MPEG2TS_PKTLENGTH*MPEG2TS_PER_IP):
                ## \todo: handle wrap around case, i.e. N packets from end of
                # file and M packets from beginning of file.
                print("End of file reached.");
                if LOOP_FILE:
                    print("Looping file.");
                    TsFile.close();
                    TsFile = open_ts_file(FILENAME);
                    sync_ts_file(TsFile);
                    mpeg2ts_data += TsFile.read(MPEG2TS_PKTLENGTH*MPEG2TS_PER_IP-len(mpeg2ts_data));
                    continue;
                else:
                    break;
            mpeg2ts_data = b''.join([bytes(mpeg2ts_data)]);
        except Exception as e:
            print("Error reading from file.");
            sys.stderr.write(e);
            break;
        
        if RTP_ENABLE:
            udp_data += b'\x80\x21';
            udp_data += struct.pack('!H', (RTP_SN & 0xFFFF));
            udp_data += b'\x00\x00\x00\x00\x00\x00\x00\x00';
            RTP_SN += 1;
        
        udp_data += mpeg2ts_data;
        
        try:
            TsSocket.send(udp_data);
        except Exception as e:
            sys.stderr.write("Error sending over socket.");
            break;
        
        try:
            time.sleep(UDP_PKTINTRVL);
        except Exception as e:
            sys.stderr.write("Failed to sleep.");
            break;
    
    if TsSocket:
        TsSocket.close();
    
    if TsFile:
        TsFile.close();
    
    print("Done.")
    
    exit(0);
