import serial
import threading
import time

import serial.serialutil


# arduino = serial.Serial(port='COM8', baudrate=1000000, timeout=1)


# def write_read(x):
#     arduino.write((x + '\n').encode())
#     response = arduino.read_until(b'\n').decode().strip()
#     return response


class SerialCommunicator(threading.Thread):
    def __init__(self, port: str, baud_rate: int, timeout: int):
        super().__init__(daemon=True)
        self.is_connected = False

        self._baud_rate = baud_rate
        self._timeout = timeout
        self._port = port

        self._lock = threading.Lock()
        self._stop_flag = threading.Event()

        self.init_serial()

    def init_serial(self):
        self._connector = serial.Serial()
        self._connector.port = self._port
        self._connector.baudrate = self._baud_rate
        self._connector.timeout = self._timeout

    def run(self):
        while not self._stop_flag.is_set():
            time.sleep(1)
            if not self.is_connected:
                self._connect()

    def _connect(self):
        try:
            if (self._connector.is_open):
                self.close()

            with self._lock:
                self._connector.open()

            self.is_connected = True
            print("Connection established on port:", self._port)

        except serial.SerialException as e:
            print(e)
            print(f"Connection failed with port: {self._port}, try again in {1} sec")
            self.is_connected = False

    def close(self):
        try:
            print("Closing port: ", self._port)
            with self._lock:
                self._connector.close()
        except serial.SerialException as e:
            print("Error closing serial port: ", self._port)

    def write(self, data):
        if (not self.is_connected):
            print("No connection serial")
            return

        with self._lock:
            try:
                self._connector.write((data + '\n').encode())
            except serial.SerialException as e:
                print("Writing to serial failed")
                self.is_connected = False

    def stop(self):
        print("Stopped reconnecting.")
        self._stop_flag.set()
        with self._lock:
            self._connector.close()


SC = SerialCommunicator("COM8", 1_000_000, 1)
SC.start()


while 1:
    time.sleep(1)
    print(SC.is_connected)

    if (SC.is_connected):
        SC.write("hello")
