

AX25_FLAG = b'\x7E'
AX25_CONTROL = b'\x03'
AX25_PID = b'\xF0'
AX25_DEST_SSID = b'\xE0'
AX25_SOURCE_SSID = b'\xE1'
AX25_SAT_ADDR = bytes([ord(b'F') << 1, ord(b'X') << 1, ord(b'6') << 1, ord(b'F') << 1, ord(b'R') << 1, ord(b'A') << 1])
AX25_GS_ADDR = bytes([ord(b'F') << 1, ord(b'4') << 1, ord(b'K') << 1, ord(b'J') << 1, ord(b'X') << 1, ord(b' ') << 1])

FRAME_TYPE_TM = b'\x07'
FRAME_TYPE_PLAT_TC = b'\x1C'
FRAME_TYPE_INT_TC = b'\x01'
FRAME_TYPE_PLD_TC = b'\x1F'
FRAME_TYPE_REPLY = b'\x0B'
FRAME_TYPE_BROADCAST = b'\x10'
FRAME_TYPE_TM_SEND_RQ = b'\x15'

TTC_DUMP_MODE_ALL = b'\x11'
TTC_DUMP_MODE_PF = b'\x22'
TTC_DUMP_MODE_PL = b'\x33'
TTC_DUMP_MODE_EPS = b'\x44'
TTC_DUMP_MODE_LOG = b'\x55'
TTC_DUMP_MODE_TTC = b'\x66'
TTC_DUMP_MODE_OBDH = b'\x77'
TTC_DUMP_MODE_LIST = b'\x88'

TC_CODE_SAT_MODE = b'\x06'
TC_CODE_RESET_MAIN = b'\xFD'
TC_CODE_RESET_SPARE = b'\xFE'

INT_TC_CODE_RESET = b'\x11'
INT_TC_CODE_CHANGE_MODE = b'\x22'

REPLY_TYPE_ACK = b'\x11'
REPLY_TYPE_NACK = b'\x22'
