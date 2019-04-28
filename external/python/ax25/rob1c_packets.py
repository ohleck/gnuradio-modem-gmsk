from .ax25_packet import AX25Packet
from .rob1c_packet_structures import Ax25Data, TelemetryFrame, ReplyFrame, PlatTCFrame
from .rob1c_parameters import *

# ===========================================================
# Generic telemetry packet
ax_packet = AX25Packet()
ax_packet.header.dest_address = AX25_GS_ADDR
ax_packet.header.dest_ssid = AX25_DEST_SSID
ax_packet.header.source_address = AX25_SAT_ADDR
ax_packet.header.source_ssid = AX25_SOURCE_SSID
ax_packet.header.control = AX25_CONTROL
ax_packet.header.pid = AX25_PID

frame = TelemetryFrame()
frame.timestamp = b'\x67\x45\x23\x01'
frame.nb_frames = b'\xBB\xAA'
frame.current_frame_number = b'\x01\x00'
frame.dump_mode = TTC_DUMP_MODE_ALL
frame.data = b'\xFE\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
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
frame.assemble()

ax_data = Ax25Data()
ax_data.frame_type = FRAME_TYPE_TM
ax_data.frame = frame
ax_data.assemble()

ax_packet.data = ax_data.bytes

ax_packet.assemble()

AX_PACKET_TM = ax_packet

# ===========================================================
# ===========================================================
# ===========================================================
# ACK PACKET TO GROUNDSTATION
ax_packet = AX25Packet()
ax_packet.header.dest_address = AX25_GS_ADDR
ax_packet.header.dest_ssid = AX25_DEST_SSID
ax_packet.header.source_address = AX25_SAT_ADDR
ax_packet.header.source_ssid = AX25_SOURCE_SSID
ax_packet.header.control = AX25_CONTROL
ax_packet.header.pid = AX25_PID

frame = ReplyFrame()
frame.timestamp = b'\x67\x45\x23\x01'
frame.reply_type = REPLY_TYPE_ACK 
frame.assemble()

ax_data = Ax25Data()
ax_data.frame_type = FRAME_TYPE_REPLY
ax_data.frame = frame
ax_data.assemble()

ax_packet.data = ax_data.bytes

ax_packet.assemble()

AX_PACKET_ACK_TO_GS = ax_packet

# ===========================================================
# ===========================================================
# ===========================================================
# ACK PACKET TO SAT
ax_packet = AX25Packet()
ax_packet.header.dest_address = AX25_SAT_ADDR
ax_packet.header.dest_ssid = AX25_DEST_SSID
ax_packet.header.source_address = AX25_GS_ADDR
ax_packet.header.source_ssid = AX25_SOURCE_SSID
ax_packet.header.control = AX25_CONTROL
ax_packet.header.pid = AX25_PID

frame = ReplyFrame()
frame.timestamp = b'\x67\x45\x23\x01'
frame.reply_type = REPLY_TYPE_ACK 
frame.assemble()

ax_data = Ax25Data()
ax_data.frame_type = FRAME_TYPE_REPLY
ax_data.frame = frame
ax_data.assemble()

ax_packet.data = ax_data.bytes

ax_packet.assemble()

AX_PACKET_ACK_TO_SAT = ax_packet

# ===========================================================
# ===========================================================
# ===========================================================
# PLATFORM TC PACKET TO SAT

ax_packet = AX25Packet()
ax_packet.header.dest_address = AX25_SAT_ADDR
ax_packet.header.dest_ssid = AX25_DEST_SSID
ax_packet.header.source_address = AX25_GS_ADDR
ax_packet.header.source_ssid = AX25_SOURCE_SSID
ax_packet.header.control = AX25_CONTROL
ax_packet.header.pid = AX25_PID

frame = PlatTCFrame()
frame.tc_code = TC_CODE_RESET_MAIN
frame.timestamp = b'\x67\x45\x23\x01'
frame.nb_of_frame = b'\x00'
frame.parameter = b'\x00'
frame.assemble()

ax_data = Ax25Data()
ax_data.frame_type = FRAME_TYPE_PLAT_TC
ax_data.frame = frame
ax_data.assemble()

ax_packet.data = ax_data.bytes

ax_packet.assemble()

AX_PACKET_TC_TO_RESET_SAT = ax_packet


# ===========================================================
# ===========================================================
# ===========================================================
# PLATFORM TC PACKET TO SAT WITH WRONG DEST ADDRESS

ax_packet = AX25Packet()
ax_packet.header.dest_address = bytes([ord(b'U') << 1, ord(b'X') << 1, ord(b'6') << 1, ord(b'F') << 1, ord(b'R') << 1, ord(b'A') << 1])
ax_packet.header.dest_ssid = AX25_DEST_SSID
ax_packet.header.source_address = AX25_GS_ADDR
ax_packet.header.source_ssid = AX25_SOURCE_SSID
ax_packet.header.control = AX25_CONTROL
ax_packet.header.pid = AX25_PID

frame = PlatTCFrame()
frame.tc_code = TC_CODE_RESET_MAIN
frame.timestamp = b'\x67\x45\x23\x01'
frame.nb_of_frame = b'\x00'
frame.parameter = b'\x00'
frame.assemble()

ax_data = Ax25Data()
ax_data.frame_type = FRAME_TYPE_PLAT_TC
ax_data.frame = frame
ax_data.assemble()

ax_packet.data = ax_data.bytes

ax_packet.assemble()

AX_PACKET_TC_TO_RESET_SAT_WRNG_ADD = ax_packet