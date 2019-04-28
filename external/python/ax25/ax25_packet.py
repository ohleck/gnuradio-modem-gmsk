from bitarray import bitarray
from crccheck.crc import CrcX25, Crc16CcittFalse, Crc16Genibus


class AX25Packet():
    """Class to connect to Cortex via its TCP-IP service ports."""

    class AX25Header():

        def __init__(self):
            self.dest_address = b''
            self.dest_ssid = b''
            self.source_address = b''
            self.source_ssid = b''
            self.control = b''
            self.pid = b''

        def parse(self, header_bytes):
            self.header_bytes = header_bytes
            if not len(header_bytes) == 16:
                return False

            self.dest_address = header_bytes[:6]
            self.dest_ssid = header_bytes[6]
            self.source_address = header_bytes[7:13]
            self.source_ssid = header_bytes[13]
            self.control = header_bytes[14]
            self.pid = header_bytes[15]

            return True
        
        def assemble(self):
            self.header_bytes = self.dest_address + self.dest_ssid + \
                self.source_address + self.source_ssid + self.control + self.pid

    def __init__(self):
        """
        """
        self.header = self.AX25Header()
        self.data = b''

    def parse_bin(self, bin_packet):
        self.bin_packet = bitarray(bin_packet)
        self.byte_packet = self.bin_packet.tobytes()
        self.parse_bytes(self.byte_packet)
    
    def parse_bytes(self, byte_packet):
        self.byte_packet = byte_packet
        self.crc = self.byte_packet[-2:]
        self.valid = self.check_crc()
        self.parse_header()
        self.parse_data()
    
    def parse_header(self):
        if self.valid:
            self.header.parse(self.byte_packet[:16])
        else:
            self.header = None
    
    def parse_data(self):
        if self.valid:
            self.data = self.byte_packet[16:-2]
        else:
            self.data = None

    def assemble(self):
        self.header.assemble()
        self.byte_packet = self.header.header_bytes + self.data
        crc = Crc16Genibus.calc(self.byte_packet)
        self.byte_packet += bytes([(0xFF00 & crc) >> 8])
        self.byte_packet += bytes([0x00FF & crc])


    def check_crc(self):
        '''
        Check CRC according to crc-16-genibus:
        http://crcmod.sourceforge.net/crcmod.predefined.html
        The CRC bytes are assumed to be in the last 16 bit positions of bin_arr.

        Keyword arguments:
        bin_arr -- Binary array [binary string]

        Outputs:
        boolean -- True if CRC valid, False otherwise

        '''
        if self.crc == b'':
            return False

        crc = Crc16Genibus.calc(self.byte_packet[:-2])
        if crc == int.from_bytes(self.crc, byteorder='big', signed=False):
            return True
        else:
            return False


    def __repr__(self):
        return repr(self.byte_packet)


if __name__ == "__main__":
    d_hex = b'\x46\x34\x4B\x4A\x58\x00\xE0\x46\x58\x36\x46\x52\x41\xE1\x03\xF0\xFE\x10' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
            b'\x00\x00\xD8\xDC'

    d_bin = bitarray()
    d_bin.frombytes(d_hex)

    ax_packet1 = AX25Packet()
    ax_packet1.parse_bin(d_bin.to01())

    ax_packet2 = AX25Packet()
    ax_packet2.parse_bytes(d_hex)

    assert(ax_packet1.byte_packet == ax_packet2.byte_packet)
    assert(ax_packet1.header.header_bytes == ax_packet2.header.header_bytes)
    assert(ax_packet1.header.dest_address == ax_packet2.header.dest_address)
    assert(ax_packet1.header.source_address == ax_packet2.header.source_address)

    ax_packet3 = AX25Packet()
    ax_packet3.header.dest_address = b'\x46\x34\x4B\x4A\x58\x00'
    ax_packet3.header.dest_ssid = b'\xE0'
    ax_packet3.header.source_address = b'\x46\x58\x36\x46\x52\x41'
    ax_packet3.header.source_ssid = b'\xE1'
    ax_packet3.header.control = b'\x03'
    ax_packet3.header.pid = b'\xF0'
    ax_packet3.data = b'\xFE\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
                    b'\x00\x00\x00\x00'

    ax_packet3.assemble()
    
    assert(ax_packet1.byte_packet == ax_packet3.byte_packet)
    assert(ax_packet1.header.header_bytes == ax_packet3.header.header_bytes)
    assert(ax_packet1.header.dest_address == ax_packet3.header.dest_address)
    assert(ax_packet1.header.source_address == ax_packet3.header.source_address)



    


