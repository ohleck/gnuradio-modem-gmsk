import struct
from tcp_utils import TCPClient
import threading
from time import sleep, time
from queue import Queue
from ax25.ax25_packet import AX25Packet
from ax25.rob1c_packet_structures import Ax25Data, TelemetryFrame
from ax25.rob1c_packets import AX_PACKET_ACK_TO_SAT, AX_PACKET_TC_TO_RESET_SAT, AX_PACKET_TC_TO_RESET_SAT_WRNG_ADD
from ax25.rob1c_packet_structures import Ax25Data, TelemetryFrame, ReplyFrame
from ax25.rob1c_parameters import *

IP = 'localhost'
PORT = 5000

CC1020_ISR_STATE_INIT = 1
CC1020_ISR_STATE_TX_PREAMBLE = 5
CC1020_ISR_STATE_TX_FLAG = 6
CC1020_ISR_STATE_TX_DATA = 7
CC1020_ISR_STATE_TX_STUF = 8

BAUD_RATE = 9600

class TransmitThread(threading.Thread):

    def __init__(self, name, tx_queue):
        threading.Thread.__init__(self)
        self.taskState = CC1020_ISR_STATE_INIT
        self.ax_counter = 0
        self.frameIndex = 0
        self.tx_buffer = None
        self.bit_counter = 0
        self.byte = 0 
        self._last_bit = 1
        self._bit_in_byte_counter = 0
        self._out_byte = 0
        self._flag_counter = 0
        self._preamble_byte = 0x7E

        self.tx_queue = tx_queue

        # Scrambler variables
        self.d_shift_register = 0
        self.d_taps = [0] * 32
        self.d_tap_count = 0

        self.frame = []

        self.client = TCPClient(IP, PORT)
        # Connect to TCP server
        connected = self.client.connect()
        if connected:
            print('Connection Successful')
        else:
            print('Failed to connect')

    def run(self):
        while(1):
            if not self.tx_queue.empty():
                self.tx_buffer = self.tx_queue.get()
                print("Sending Data")
                self.transmit_preamble()
                self._last_bit = 1
                while not self.transmit_packet(): pass
                self.transmit_preamble()                
                self.transmit_frame()

    def transmit_frame(self):
        sent = self.client.send_data(bytes(self.frame))
        self.frame = []
        return sent

    def transmit_byte(self):
        self.frame.append(self._out_byte)
        self._out_byte = 0

    def transmit_bit_nrzi(self, out_bit):        
        if(out_bit == self._last_bit):
            self._out_byte = self._out_byte | (0x80 >> self._bit_in_byte_counter)
            self._last_bit = 1
        else:
            self._out_byte = self._out_byte & ~((0x80 >> self._bit_in_byte_counter) & 0xFF)
            self._last_bit = 0

        self._bit_in_byte_counter += 1
        if self._bit_in_byte_counter == 8:
            self._bit_in_byte_counter = 0
            self.transmit_byte()

    def transmit_bit(self, bit):
        if bit:
            self._out_byte = self._out_byte | (0x80 >> self._bit_in_byte_counter)
        else:
            self._out_byte = self._out_byte & ~((0x80 >> self._bit_in_byte_counter) & 0xFF)

        self._bit_in_byte_counter += 1
        if self._bit_in_byte_counter == 8:
            self._bit_in_byte_counter = 0
            self.transmit_byte()

    def transmit_preamble(self):
        count = 0
        while count < 50:
            self._out_byte = 0x55            
            self.transmit_byte()
            count += 1

    def transmit_packet(self):
       
        if self.taskState == CC1020_ISR_STATE_INIT:
            self.frameIndex = 0
            self.taskState = CC1020_ISR_STATE_TX_FLAG
            self.byte = 0x7E #Preamble value
            self.bit_counter = 0
            self._bit_in_byte_counter = 0

        elif self.taskState == CC1020_ISR_STATE_TX_FLAG:
            if (self.byte & 0x80):
                self.transmit_bit_nrzi(1)
            else:
                self.transmit_bit_nrzi(0)
            self.bit_counter += 1
            if (self.bit_counter == 8):
                self._flag_counter += 1
                self.bit_counter = 0
                self.byte = 0x7E #Preamble value
                if self._flag_counter >= 2:
                    if (self.frameIndex):
                        self.taskState = CC1020_ISR_STATE_INIT
                        return self.frameIndex

                    self.byte = self.tx_buffer[self.frameIndex] # Load first element
                    self.taskState = CC1020_ISR_STATE_TX_DATA
                    return 0
            else:
                self.byte <<= 1
            return 0

        elif self.taskState == CC1020_ISR_STATE_TX_DATA:
            if (self.byte & 0x80):
                self.ax_counter += 1
                self.transmit_bit_nrzi(1)
            else:
                self.ax_counter = 0
                self.transmit_bit_nrzi(0)

            self.bit_counter += 1
            if (self.ax_counter == 5):
                self.ax_counter = 0
                self.taskState = CC1020_ISR_STATE_TX_STUF

            if (self.bit_counter == 8):
                self.bit_counter = 0
                if (self.frameIndex == len(self.tx_buffer)-1):
                    self.byte = 0x7E # Flag
                    self.tx_buffer = None
                    self.taskState = CC1020_ISR_STATE_TX_FLAG
                    return 0

                self.frameIndex += 1
                self.byte = self.tx_buffer[self.frameIndex] # Load next element

                return 0
            else:
                self.byte <<= 1
            
            return 0

        elif self.taskState == CC1020_ISR_STATE_TX_STUF:
            self.transmit_bit_nrzi(0)
            self.taskState = CC1020_ISR_STATE_TX_DATA
            return 0

        else:
            self.taskState = CC1020_ISR_STATE_INIT
            return 0


class TCThread(threading.Thread):

    def __init__(self, name, tx_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.n_packets = 0
        self.tx_queue = tx_queue

    def run(self):
        while(1):
            self.n_packets += 1
            # sleep(1)
            cmd = input()
            # cmd = 'wtc'
            if cmd == 'tc':
                self.tx_queue.put(AX_PACKET_TC_TO_RESET_SAT.byte_packet)
            elif cmd == 'wtc':
                self.tx_queue.put(AX_PACKET_TC_TO_RESET_SAT_WRNG_ADD.byte_packet)
            elif cmd == 'ack':
                self.tx_queue.put(AX_PACKET_ACK_TO_SAT.byte_packet)

            print("Adding data N#: ", self.n_packets)




if __name__ == "__main__":

    tx_queue = Queue(maxsize=3)
    # ax_packet = AX25Packet()
    # ax_packet.header.dest_address = b'FX6FRA'
    # ax_packet.header.dest_ssid = b'\xE0'
    # ax_packet.header.source_address = b'F4KJX' + b'\x00'
    # ax_packet.header.source_ssid = b'\xE1'
    # ax_packet.header.control = b'\x03'
    # ax_packet.header.pid = b'\xF0'

    # frame = ReplyFrame()
    # frame.timestamp = b'\x67\x45\x23\x01'
    # frame.reply_type = REPLY_TYPE_ACK
    # frame.assemble()

    # ax_data = Ax25Data()
    # ax_data.frame_type = FRAME_TYPE_REPLY
    # ax_data.frame = frame
    # ax_data.assemble()

    # ax_packet.data = ax_data.bytes

    # ax_packet.assemble()

    # AX_PACKET_ACK_TO_SAT = ax_packet

    tx_thread = TransmitThread("TransmitThread", tx_queue) 
    tx_thread.start()
    tc_thread = TCThread("TelecommandThread", tx_queue) 
    tc_thread.start()
    # print()
    ## Tests
    # data = [0x00, 0x00, 0x00, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x00, 0x01, 0x02, 0x03]
    # tx_thread.scrambler_init(0x21000)
    # s_data = tx_thread.scramble_frame(data)
    # for d in s_data:
    #     print(hex(d))
    # # print(hex(s_data))

    # print('Received Packets found:', tx_thread.received_packets)
    # print('Valid Packets found:', tx_thread.valid_packets