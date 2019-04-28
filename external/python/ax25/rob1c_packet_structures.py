from bitarray import bitarray
from .rob1c_parameters import *

class Ax25Data():
    """Class to connect to Cortex via its TCP-IP service ports."""

    def __init__(self):
        """
        """
        self.frame_length = b''
        self.frame_type = b''
        self.frame = None
        self.frame_info = ''

    def parse_bin(self, bin_packet):
        self.bin_packet = bitarray(bin_packet)
        self.bytes = self.bin_packet.tobytes()
        self.parse_bytes(self.bytes)
    
    def parse_bytes(self, byte_packet):
        self.bytes = byte_packet
        self.frame_length = self.bytes[0]
        self.frame_type = self.bytes[1]
        
        if self.frame_type == ord(FRAME_TYPE_TM):
            self.frame = TelemetryFrame()
            self.frame.parse(self.bytes[2:])
            self.frame_info += 'TELEMETRY FRAME'

        if self.frame_type == ord(FRAME_TYPE_REPLY):
            self.frame = ReplyFrame()
            self.frame.parse(self.bytes[2:])
            self.frame_info += 'REPLY FRAME'

        if self.frame_type == ord(FRAME_TYPE_BROADCAST):
            self.frame = BeaconFrame()
            self.frame.parse(self.bytes[2:])
            self.frame_info += 'BROADCAST FRAME'

    def assemble(self):
        self.frame_length = bytes([len(self.frame.bytes)])
        self.bytes =  self.frame_length + self.frame_type + self.frame.bytes

    def __repr__(self):
        return repr(self.bytes)


class TelemetryFrame():

    def __init__(self):
        self.timestamp = b''
        self.nb_frames = b''
        self.current_frame_number = b''
        self.dump_mode = b''
        self.data = b''

    def parse(self, frame_bytes):
        self.bytes = frame_bytes
        self.timestamp = self.bytes[0:4]
        self.nb_frames = self.bytes[4]
        self.current_frame_number = self.bytes[5]
        self.dump_mode = self.bytes[6]
        self.data = self.bytes[7:]

    def assemble(self):
        self.bytes = self.timestamp + self.nb_frames + self.current_frame_number + \
            self.dump_mode + self.data


class BeaconFrame():

    def __init__(self):
        self.timestamp = b''
        self.data = b''

    def parse(self, frame_bytes):
        self.bytes = frame_bytes
        self.timestamp = self.bytes[0:4]
        self.data = self.bytes[4:]

    def assemble(self):
        self.bytes = self.timestamp + self.data


class ReplyFrame():

    def __init__(self):
        self.timestamp = b''
        self.reply_type = b''
        self.is_ack = False

    def parse(self, frame_bytes):
        self.bytes = frame_bytes
        self.timestamp = self.bytes[0:4]
        self.reply_type = self.bytes[4]
        if self.reply_type == 0x11:
            self.is_ack = True

    def assemble(self):
        self.bytes = self.timestamp + self.reply_type


class PlatTCFrame():

    def __init__(self):
        self.tc_code = b''
        self.timestamp = b''
        self.nb_of_frame = b''
        self.parameter = False

    def parse(self, frame_bytes):
        self.bytes = frame_bytes
        self.tc_code = self.bytes[0]
        self.timestamp = self.bytes[1:5]
        self.nb_of_frame = self.bytes[5]
        self.parameter = self.bytes[5]

    def assemble(self):
        self.bytes =  self.tc_code + self.timestamp + self.nb_of_frame + self.parameter


if __name__ == "__main__":

    # Telemetry Data
    ax_data_tm = Ax25Data()
    data = b'\x0C\x07\x67\x45\x23\x01\xBB\xAA\x01\x00\xA2\x03\xA6\x56'
    ax_data_tm.parse_bytes(data)
    assert(ax_data_tm.frame_type == ord(FRAME_TYPE_TM))

    ax_data_tm_2 = Ax25Data()
    ax_data_tm_2.frame_type = FRAME_TYPE_TM
    tm_frame = TelemetryFrame()
    tm_frame.timestamp = b'\x67\x45\x23\x01'
    tm_frame.nb_frames = b'\xBB\xAA'
    tm_frame.current_frame_number = b'\x01\x00'
    tm_frame.dump_mode = b'\xA2'
    tm_frame.data = b'\x03\xA6\x56'
    tm_frame.assemble()
    
    ax_data_tm_2.frame = tm_frame
    ax_data_tm_2.assemble()

    assert(ax_data_tm.bytes == ax_data_tm_2.bytes)
    # Reply Packet - ACK
    ax_data_ack = Ax25Data()
    data = b'\x05\x0B\x0A\x07\x67\x45\x11\x93\xF1'
    ax_data_ack.parse_bytes(data)
    assert(ax_data_ack.frame_type == ord(FRAME_TYPE_REPLY))
    assert(ax_data_ack.frame.reply_type == ord(REPLY_TYPE_ACK))
    assert(ax_data_ack.frame.is_ack)