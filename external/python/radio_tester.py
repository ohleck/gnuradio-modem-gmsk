from queue import Queue
from tcp_receiver import ReceiverThread
from tcp_sender import TransmitThread
from tester.logger_utils import create_main_header, create_section, create_subsection, create_test_section
from tester.test_cases import TestCase
from bitarray import bitarray
from ax25.ax25_packet import AX25Packet
from ax25.rob1c_packet_structures import Ax25Data, TelemetryFrame, ReplyFrame, PlatTCFrame
from ax25.rob1c_packets import AX_PACKET_ACK_TO_SAT, AX_PACKET_TC_TO_RESET_SAT, AX_PACKET_TC_TO_RESET_SAT_WRNG_ADD
from time import sleep
from datetime import datetime
import struct
import sys
import os
import binascii
import math


# ==============================================================
# GLOBAL CONFIGURATION

description = '''
Implementation of Test Cases:
- TEST CASE 0:

'''
test_handler = TestCase('0', description)

rx_queue = Queue(maxsize=5)
rx_thread = ReceiverThread("ReceiverThread", rx_queue) 
rx_thread.setDaemon(True)

tx_queue = Queue(maxsize=5)
tx_thread = TransmitThread("TransmitterThread", tx_queue) 
tx_thread.setDaemon(True)

rx_thread.start()
tx_thread.start()

# ================
# FIRMWARE CONFIGURATION

firmware_info = 'Downlink frequency: {} \n'.format(433)

firmware_subsection = create_subsection('FIRMWARE CONFIGURATION', firmware_info)

test_handler.add_to_log(firmware_subsection)

# ==============================================================
# AUXILIARY FUNCTIONS

def add_summary(test_result, test_dict):
    # Add summary information and results found in tests
    if test_result:
        summary_result = 'PASSED! \n'
    else:
        summary_result = 'FAILED! \n'

    for description, val in test_dict.items():
        summary_result += description.format(val)

    summary_section = create_subsection('TEST RESULTS SUMMARY', summary_result)

    return summary_section

# ==============================================================
# ==============================================================
# ==============================================================
# START TEST

# Create string to store test results
test_result = ''

tc_packets_global_count = 0
tm_packets_global_count = 0
error_global_count = 0

# add test header to log
test_section = create_section('TEST START', '')
test_handler.add_to_log(test_section)

print(test_section)

# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# START TEST CASE 0

# ========================================
# TEST INITIALIZATION

received_packets = 0
test_dict = {}
test_result = False
error_count = 0
timeout = False

MAX_TIME = 20.0
start_time = datetime.now()
# ========================================
# TEST DEFINITION

while(1):
    if not rx_queue.empty():
        received_packets += 1
        packet = rx_queue.get()
        ax25_packet = AX25Packet()
        ax25_packet.parse_bytes(packet)
        ax25_data = Ax25Data()
        ax25_data.parse_bytes(ax25_packet.data)
        if(ax25_data.frame_info == 'BROADCAST FRAME'):
            runtime = datetime.now() - start_time
            test_result = True
            break

    runtime = datetime.now() - start_time
    if runtime.total_seconds() > MAX_TIME:
        timeout = True
        test_result = False
        break


test_section = create_test_section(title='Test Case 0 Results',
                                   description='', content='Checking if beacon received \n')

if not test_result:
    error_count += 1
# ========================================
#  TEST CASE 0 SUMMARY
test_dict = {
    '\nNumber of Packets Received with valid CRC: {} packets': received_packets, 
    '\nTest Case run time: {} ': runtime, 
}

if timeout:
    test_dict['\nFailure Cause: Timeout'] = ''

# Add summary
test_section += add_summary(test_result, test_dict)

# Write test section to log file
test_handler.add_to_log(test_section)

# Print Section to terminal
print(test_section)

# Increment global counters
error_global_count += error_count
tm_packets_global_count += received_packets


# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# START TEST CASE 1

# ========================================
# TEST INITIALIZATION

received_packets = 0
test_dict = {}
test_result = False
error_count = 0
timeout = False
beacon_time = []
beacon_counter = 0

N_BEACON = 3
MAX_TIME = 100.0
BEACON_TIME = 10.0
start_time = datetime.now()
last_beacon_time = datetime.now()
# ========================================
# TEST DEFINITION

while(1):
    if not rx_queue.empty():
        received_packets += 1
        packet = rx_queue.get()
        ax25_packet = AX25Packet()
        ax25_packet.parse_bytes(packet)
        ax25_data = Ax25Data()
        ax25_data.parse_bytes(ax25_packet.data)
        if(ax25_data.frame_info == 'BROADCAST FRAME'):
            beacon_time.append((datetime.now() - last_beacon_time).total_seconds())
            last_beacon_time = datetime.now()
            beacon_counter += 1
            if(beacon_counter >= N_BEACON):
                runtime = datetime.now() - start_time
                break

    runtime = datetime.now() - start_time
    if runtime.total_seconds() > MAX_TIME:
        timeout = True
        test_result = False
        break

beacon_time_avg = sum(beacon_time) / len(beacon_time)

if(0.9*BEACON_TIME < beacon_time_avg < 1.1*BEACON_TIME):
    test_result = True
else:
    test_result = False
    
test_section = create_test_section(title='Test Case 1 Results',
                                   description='', content='Checking beacon timing \n')

if not test_result:
    error_count += 1
# ========================================
#  TEST CASE 1 SUMMARY
test_dict = {
    '\nNumber of Packets Received with valid CRC: {} packets': received_packets, 
    '\nAverage beacon time interval: {} seconds': beacon_time_avg,    
    '\nTest Case run time: {} ': runtime,
}

if timeout:
    test_dict['\nFailure Cause: Timeout'] = ''

# Add summary
test_section += add_summary(test_result, test_dict)

# Write test section to log file
test_handler.add_to_log(test_section)

# Print Section to terminal
print(test_section)

# Increment global counters
error_global_count += error_count
tm_packets_global_count += received_packets


# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# START TEST CASE 2

# ========================================
# TEST INITIALIZATION

received_packets = 0
sent_packets = 0
test_dict = {}
test_result = False
error_count = 0
timeout = False

MAX_TIME = 30.0
start_time = datetime.now()
# ========================================
# TEST DEFINITION

tx_queue.put(AX_PACKET_TC_TO_RESET_SAT.byte_packet)
sent_packets += 1

while(1):
    if not rx_queue.empty():
        received_packets += 1
        packet = rx_queue.get()
        ax25_packet = AX25Packet()
        ax25_packet.parse_bytes(packet)
        ax25_data = Ax25Data()
        ax25_data.parse_bytes(ax25_packet.data)
        if(ax25_data.frame_info == 'REPLY FRAME'):
            if ax25_data.frame.is_ack:
                runtime = datetime.now() - start_time
                test_result = True
                break

    runtime = datetime.now() - start_time
    if runtime.total_seconds() > MAX_TIME:
        timeout = True
        test_result = False
        break
    
test_section = create_test_section(title='Test Case 2 Results',
                                   description='', content='Check if ACK after TC \n')

if not test_result:
    error_count += 1
# ========================================
#  TEST CASE 2 SUMMARY
test_dict = {
    '\nNumber of Packets Received with valid CRC: {} packets': received_packets, 
    '\nNumber of Packets Sent: {} packets': sent_packets, 
    '\nTest Case run time: {} ': runtime,
}

if timeout:
    test_dict['\nFailure Cause: Timeout'] = ''

# Add summary
test_section += add_summary(test_result, test_dict)

# Write test section to log file
test_handler.add_to_log(test_section)

# Print Section to terminal
print(test_section)

# Increment global counters
error_global_count += error_count
tm_packets_global_count += received_packets
tc_packets_global_count += sent_packets


# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# ******************************************************************************************************************************************************************************
# START TEST CASE 3

# ========================================
# TEST INITIALIZATION

received_packets = 0
sent_packets = 0
test_dict = {}
test_result = False
error_count = 0
timeout = False
got_ack = False

MAX_TIME = 30.0
start_time = datetime.now()
# ========================================
# TEST DEFINITION

tx_queue.put(AX_PACKET_TC_TO_RESET_SAT_WRNG_ADD.byte_packet)
sent_packets += 1

while(1):
    if not rx_queue.empty():
        received_packets += 1
        packet = rx_queue.get()
        ax25_packet = AX25Packet()
        ax25_packet.parse_bytes(packet)
        ax25_data = Ax25Data()
        ax25_data.parse_bytes(ax25_packet.data)
        if(ax25_data.frame_info == 'REPLY FRAME'):
            if not ax25_data.frame.is_ack:
                runtime = datetime.now() - start_time
                test_result = True
                break
            else:
                runtime = datetime.now() - start_time
                test_result = False
                got_ack = True
                break

    runtime = datetime.now() - start_time
    if runtime.total_seconds() > MAX_TIME:
        timeout = True
        test_result = False
        break
    
test_section = create_test_section(title='Test Case 3 Results',
                                   description='', content='Check if NACK after TC with wrong DEST address \n')

if not test_result:
    error_count += 1
# ========================================
#  TEST CASE 3 SUMMARY
test_dict = {
    '\nNumber of Packets Received with valid CRC: {} packets': received_packets, 
    '\nNumber of Packets Sent: {} packets': sent_packets, 
    '\nTest Case run time: {} ': runtime,
}

if got_ack:
    test_dict['\nFailure Cause: Got ACK instead of NACK'] = ''

if timeout:
    test_dict['\nFailure Cause: Timeout'] = ''

# Add summary
test_section += add_summary(test_result, test_dict)

# Write test section to log file
test_handler.add_to_log(test_section)

# Print Section to terminal
print(test_section)

# Increment global counters
error_global_count += error_count
tm_packets_global_count += received_packets
tc_packets_global_count += sent_packets

# ========================================
#  GLOBAL TEST SUMMARY

# # Add summary information and results found in tests

end_time = datetime.now()
summary_data = 'Total time duration of the test {} \n'.format(end_time - test_handler.start_time)
# summary_data += 'Received {} CCSDS telemetry packets from CORTEX \n'.format(total_received)
summary_data += 'Detected {} errors in response \n'.format(error_global_count)
summary_section = create_section('TEST RESULTS SUMMARY', summary_data)

# Write summary section to log file
print(summary_section)
test_handler.add_to_log(summary_section)

rx_thread.stop()


