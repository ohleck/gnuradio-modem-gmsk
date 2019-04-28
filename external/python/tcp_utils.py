# -------------------------------------------------------------------------------
# -- Description: Generic class to connect to cortex as a TCP client
# -------------------------------------------------------------------------------

import socket
import struct

class TCPClient(object):
    """Class to connect to TCP SERVER via TCP-IP service ports."""

    def __init__(self, ip, port):
        """Initialize tcp client.

        Keyword arguments:
        ip -- ip address of cortex in LAN [str] [ex: '192.168.0.100']
        port -- tcp port of service [int] [ex: 3000 for monitor service]
        """
        self.ip = ip
        self.port = port
        self.s = None  # Socket instance

    def connect(self):
        """Connect to the TCP port.

        Outputs:
        True if connected
        False if not connected
        """
        # Repeat the connect process 10 times before give up
        for attempt in range(10):
            try:
                # Try to create the socket
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Try to connect the socket to the IP/TCP port provided
                self.s.connect((self.ip, self.port))
                print('Connected to Server')
                # if no errors, return True
                return True
            except:
                # if errors found, print message and recursevely call the connect function with +1 attempts
                print(('Attempt {}: Failed to connect to Server').format(attempt))

        # if still not connected after all attempts, return False
        return False

    def disconnect(self):
        """Disconnect from the Cortex TCP port."""
        self.s.close()

    def send_data(self, data):
        r"""Send data to the connected TCP port.

        Keyword arguments:
        data -- array of bytes which will be sent to the tcp port [bytes] [ex: b'\x00']

        Outputs:
        True if successful
        False if failed
        """
        sent = self.s.send(data)
        return (sent != 0)

    def receive_data(self, len=4096):
        r"""Receive data to the connected TCP port.

        Outputs:
        data -- array of bytes which received from the tcp port [bytes] [ex: b'\x00']

        """
        # Receive data in a len-bytes buffer
        data = self.s.recv(len)
        return data


if __name__ == '__main__':
    # Create object with localhost as ip
    client = TCPClient('localhost', 7001)
    # Connect to TCP server
    connected = client.connect()
    # Check if connected
    if connected:
        print('Connection Successful')
        # Create a dummy message with two integers (ii) and pack them as bytes
        msg = struct.pack('>ii', 10, 100)
        # Send bytes to TCP server
        sent = client.send_data(msg)
        # Print if sent
        print(sent)
        # Get server response
        # resp = client.receive_data()
        # Print server response
        # print(resp)
    else:
        print('Connection NOT Successful')

    client.disconnect()