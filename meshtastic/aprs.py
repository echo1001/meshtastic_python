import logging
import platform
import threading
import socket

from pubsub import pub # type: ignore[import-untyped]

from meshtastic.protobuf import portnums_pb2, tracker_pb2
from meshtastic import mt_config
from meshtastic.util import ipstr, readnet_u16

FEND = 0xC0
FESC = 0xDB
TFEND = 0xDC
TFESC = 0xDD

def encapsulate(data: bytes, channel) -> bytes:
    out = bytearray()
    out.append(FEND)
    out.append((channel & 0x0F) << 4)
    for byte in data:
        if byte == FEND:
            out.append(FESC)
            out.append(TFEND)
        elif byte == FESC:
            out.append(FESC)
            out.append(TFESC)
        else:
            out.append(byte)
    out.append(FEND)
    return bytes(out)
    
def ax25(source: str, source_ssid: int, data: str) -> bytes:
    RR_MASK = 0x60
    SSID_H_MASK = 0x80
    SSID_LAST_MASK = 0x01
    AX25_UI_FRAME = 0x03
    AX25_PID_NO_LAYER_3 = 0xF0

    destination = "APRS"
    destination_ssid = 0
    destination_bytes = bytearray([64] * 7) 
    destination_encoded = bytearray(destination.encode('ascii'))
    for i in range(len(destination_encoded)):
        destination_bytes[i] = destination_encoded[i] << 1
    destination_bytes[6] = (destination_ssid & 0xf) << 1
    destination_bytes[6] |= RR_MASK | SSID_H_MASK

    source_bytes = bytearray([64] * 7)
    source_encoded = bytearray(source.encode('ascii'))
    for i in range(len(source_encoded)):
        source_bytes[i] = source_encoded[i] << 1
    source_bytes[6] = (10 & 0xf) << 1
    source_bytes[6] |= RR_MASK
    
    repeater = "WIDE1"
    repeater_bytes = bytearray([64] * 7)
    repeater_encoded = bytearray(repeater.encode('ascii'))
    for i in range(len(repeater_encoded)):
        repeater_bytes[i] = repeater_encoded[i] << 1
    repeater_bytes[6] = (1 & 0xf) << 1
    repeater_bytes[6] |= RR_MASK

    repeater2 = "WIDE2"
    repeater2_bytes = bytearray([64] * 7)
    repeater2_encoded = bytearray(repeater2.encode('ascii'))
    for i in range(len(repeater2_encoded)):
        repeater2_bytes[i] = repeater2_encoded[i] << 1
    repeater2_bytes[6] = (2 & 0xf) << 1
    repeater2_bytes[6] |= RR_MASK | SSID_LAST_MASK

    control_bytes = bytearray([AX25_UI_FRAME, AX25_PID_NO_LAYER_3])

    data_bytes = bytearray(data.encode('ascii'))

    payload = destination_bytes + source_bytes + repeater_bytes + repeater2_bytes + control_bytes + data_bytes
    return bytes(payload)
    
def onReceive(packet, interface):
    mt_config.aprs.onReceive(packet)

class APRS:
    class KISSException(Exception):
        """An exception class for KISS errors"""
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    def __init__(self, host, port, channel) -> None:
        """
        Constructor

        iface is the already open MeshInterface instance
        """
        self.port = port
        self.host = host
        self.channel = channel
        self.sock = None
        self.running = False
        self.reconnect_delay = 5  # seconds
        mt_config.aprs = self
        pub.subscribe(self.onReceive, "meshtastic.receive.data.TRACKER_APP")
        
        # Start connection in a separate thread
        self.running = True
        self.connect_thread = threading.Thread(target=self._connection_handler, daemon=True)
        self.connect_thread.start()
        
    def _connect(self):
        """Establish connection to KISS TNC server"""
        try:
            if self.sock:
                self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.host, self.port))
            logging.info(f"Connected to KISS TNC at {self.host}:{self.port}")
            return True
        except socket.error as e:
            logging.error(f"Failed to connect to KISS TNC at {self.host}:{self.port}: {e}")
            return False
        
    def _connection_handler(self):
        """Handle connection, reconnection, and start send/receive threads"""
        while self.running:
            if self._connect():
                # Start send and receive threads
                receive_thread = threading.Thread(target=self._receive_handler, daemon=True)
                receive_thread.start()
                
                # Wait for connection to fail
                receive_thread.join()
            
            if self.running:
                logging.info(f"Reconnecting in {self.reconnect_delay} seconds...")
                threading.Event().wait(self.reconnect_delay)
        
    def _receive_handler(self):
        """Handle receiving data from KISS TNC"""
        try:
            while self.running and self.sock:
                try:
                    data = self.sock.recv(1024)
                    if not data:
                        break
                except socket.timeout:
                    # print("Socket timeout, continuing to receive...")
                    continue
                except socket.error as e:
                    logging.error(f"Socket error: {e}")
                    break
                    
            # Ignore received data as requested
        except socket.error as e:
            logging.error(f"Receive error: {e}")
        finally:
            if self.sock:
                self.sock.close()
                self.sock = None
        
    def send_data(self, data):
        """Send data to KISS TNC"""
        if self.sock:
            try:
                self.sock.send(data)
            except socket.error as e:
                logging.error(f"Send error: {e}")
        
    def close(self):
        """Close connection and stop threads"""
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        
    def onReceive(self, packet, interface):
        # print(packet)
        
        position = tracker_pb2.Tracker.FromString(packet["decoded"]["payload"])
        # print(position)
        
        
        lat = position.latitude_i * 1e-7
        lon = position.longitude_i * 1e-7

        latdeg = int(lat)
        latmin = (lat - latdeg) * 60

        londeg = int(lon)
        lonmin = (lon - londeg) * 60

        # print(latmin, lonmin)
        # print(position)

        latminB = (abs(latmin) * 1000) % 10
        latminB = int(latminB)
        latminB = f"{latminB:01d}"

        lonminB = (abs(lonmin) * 1000) % 10
        lonminB = int(lonminB)
        lonminB = f"{lonminB:01d}"

        lat_str = f"{abs(latdeg):02d}{abs(latmin):05.2f}{'N' if lat >= 0 else 'S'}"
        lon_str = f"{abs(londeg):03d}{abs(lonmin):05.2f}{'E' if lon >= 0 else 'W'}"
        
        altitude = position.altitude
        # Convert meters to feet 
        altitude = int(altitude * 3.28084)
        # /A=aaaaaa
        altitude_str = f"/A={altitude:06d}"
        
        speed = position.ground_speed
        # speed *= 0
        # Convert speed km/h to knots
        speed_knots = int(speed / 1.852)
        
        heading = position.ground_track
        heading *= 1e-05
        heading = int(heading)
        
        speed_heading_str = f"{heading:03d}/{speed_knots:03d}"
        
        
        voltage = f"V{position.voltage:.3f} "
        utilization = f"U{int(position.channel_utilization)} "
        temperature = f"T{position.temperature:.2f} "
        humidity = f"H{position.relative_humidity:.2f} "
        pressure = f"P{position.barometric_pressure:.2f} "

        aprs_str = f"!{lat_str}/{lon_str}O{speed_heading_str}{altitude_str} {voltage}{utilization}{temperature}{humidity}{pressure}S{position.sats_in_view}!W{latminB}{lonminB}!"

        
        data = ax25(position.call_sign, position.ssid, aprs_str)
        data = encapsulate(data, self.channel)
        self.send_data(data)