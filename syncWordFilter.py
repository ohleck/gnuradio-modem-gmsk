#!/usr/bin/python2.7
import socket, argparse, datetime, sys

# Purpose: connects to a TCP port streaming binary data (usually from a GNURadio decode flow),
# and search for a given pattern (syncWord) in the bit level. After matching a sync word, 
# forwards to the standard output a slice of N bytes (patcket_length), in ASCII coded format (regular text processing).

# Use with -display_compact to supress extra messages and be able to pipe directly to another module.

# Usage:
# ./syncWordStreamFilter.py -ip localhost -port 7000 -syncWord 0x7E8CB0 -packet_length 10 -display_time
# ./syncWordStreamFilter.py -ip localhost -port 7000 -syncWord 0x7E8CB0 -packet_length 280 -display_compact > sampleTTC.bin


# Optional: -verbose -display_time -display_compact
# use '| more' to control the verbose output
# 
# Simulation environment: 
# The command bellow creates and TCP server providing the binary file as content and restarting the operation after the client disconnects.
# while true; do nc -l 127.0.0.1 7000 < samples/sampleBitstream_syncWord_0x5370.bin; done

parser = argparse.ArgumentParser()
parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-port', type=long, required =True) # Port number
parser.add_argument ('-syncWord',required=True) #Entry to the sync word
parser.add_argument ('-packet_length', type=int, required=True) #Payload size
parser.add_argument ('-verbose', action='store_true')
parser.add_argument ('-display_time', action='store_true')
parser.add_argument ('-display_compact', action='store_true')
args = parser.parse_args() 

# Check if sync word is in appropriated ascii hexadecimal representation
if args.syncWord[:2] != '0x':
  print "-syncWord should be in the format hexadecimal format. Ex: '0x5B53575D'"
  print "Exiting..."
  exit()
if (len(args.syncWord)%2) != 0:
  print "-syncWord length should be even! Two ascii chars representing each byte. Ex: '0x5B53575D'"
  print "Exiting..."
  exit()

# Store the sync word as a decimal value
syncWord = int(args.syncWord,16)
syncWord_len = (len(args.syncWord)/2)-1
# syncWord_bin = bin(syncWord)
syncWord_bin = "{0:#0{1}b}".format(syncWord, 2+syncWord_len*8)
if args.verbose: print 'Seeking input stream for sync word:', hex(syncWord) ,'(syncWord length:',syncWord_len,'B)', 'Binary:', syncWord_bin, 'Decimal:', syncWord


if args.verbose: print 'Connecting to', args.ip, args.port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket
client_socket.connect((args.ip, args.port)) #Connects the client to the server


def readNextByte():
  inputByte_str = client_socket.recv(1)
  if not inputByte_str:
    if args.verbose: print 'Connection Lost!'
    client_socket.close()
    exit()
  else:
    return ord(inputByte_str)

def readByteChunk(length):
  readBuffer = []
  # loop through N single reads instead of socket buffer to avoid network dellays / buffer sizes mismatches issues
  for n in range(length):
    inputByte_str = client_socket.recv(1) 
    if not inputByte_str:
      if args.verbose: print 'Connection Lost!'
      client_socket.close()
      exit()
    readBuffer.append(inputByte_str)  
  return readBuffer

def debugPrintBuffers():
  print '\033[94m'+'bit:', (streamBytePosition*8)+localBitPosition,'Byte:', streamBytePosition, 
  print '\033[92m'+'Analyzing:', "{0:#0{1}x}".format(comparisonBuffer,2+syncWord_len*2), "{0:#0{1}b}".format(comparisonBuffer, 2+syncWord_len*8)[2:],
  print '\033[93m'+'<', bin(nextBit)[2],'<'+'\033[95m',
  binStr = str("{0:#0{1}b}".format(inputBuffer, 10))[2:]
  print binStr[:localBitPosition]+'\033[7m'+binStr[localBitPosition]+'\033[27m'+binStr[localBitPosition+1:],
  print "{0:#0{1}x}".format(inputBuffer,4),
  print '\033[91m'+'Matches:', matchesCount,
  if now:
    print 'Last:', now.strftime("%H:%M:%S"),
  print ''


# fill the comparison buffer with the syncWord size
matchesCount = 0
now = False
comparisonBuffer = 0
for n in range(syncWord_len):
  inputBuffer = (readNextByte() & 0b11111111 )
  comparisonBuffer = (comparisonBuffer<<8 ) | inputBuffer
  if args.verbose: print 'inputBuffer:\t', "  {0:#0{1}b}".format(inputBuffer, 2+syncWord_len*8), "{0:#0{1}x}".format(inputBuffer,2+syncWord_len*2) 
  if args.verbose: print 'comparisonBuffer:', "{0:#0{1}b}".format(comparisonBuffer, 2+syncWord_len*8), "{0:#0{1}x}".format(comparisonBuffer,2+syncWord_len*2) 


streamBytePosition = 0
nextBit = 0
while True: 
  # Reads the TCP source byte per byte, but analyzes locally in bit steps, 
  # because syncWord is not necessarely aligned in the incoming byte sequence

  # comparisonBuffer was already filled in the previous step and is ready for comparison,
  # but still read one subsequent byte, for the following bitwise insertions in the comparison buffer
  inputBuffer = (readNextByte() & 0b11111111 ) 
  
  for localBitPosition in range(8):

    inputBuffer_str = "{0:#0{1}b}".format(inputBuffer, 10)
    nextBit = int(inputBuffer_str[localBitPosition+2], 2)
    if args.verbose: debugPrintBuffers()

    if comparisonBuffer == syncWord:
      matchesCount = matchesCount + 1
      if args.verbose: print '\033[91m'+">>>", hex(syncWord), 'SYNC WORD FOUND processing byte:',streamBytePosition, '- Input bit count:', (streamBytePosition*8)+localBitPosition
      packet = readByteChunk(args.packet_length)

      if args.display_compact: 
        sys.stdout.write( "{:02X}".format( syncWord ) )
        sys.stdout.write( "{:02X}".format( inputBuffer ) )
        sys.stdout.flush() 
      else:
        print "{0:#0{1}x}".format( syncWord ,4),
        print "{0:#0{1}x}".format( inputBuffer ,4), # merge with the next byte after syncWord (inputBuffer), pre-fetched from memory 
      
      for i in range(len(packet)):
        if args.display_compact: 
          sys.stdout.write( "{:02X}".format( ord(packet[i]) ) )
          sys.stdout.flush() 
        else:
          print "{0:#0{1}x}".format( ord(packet[i]) ,4),
      
      now = datetime.datetime.now()
      if args.display_time: print "\tReceived at:", now,
      if not args.display_compact: print ""
      streamBytePosition = streamBytePosition + syncWord_len + args.packet_length

    # Moving comparisonBuffer to the next bit:  
    comparisonBuffer = ( (comparisonBuffer<<1) & int('1'*8*syncWord_len,2) ) | nextBit
    
  streamBytePosition = streamBytePosition + 1
  sys.stdout.flush()


if args.verbose: print "syncWordStreamFilter.py end! Closing TCP connection..."
client_socket.close()
