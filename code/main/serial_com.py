from logger import LoggerFactory

import threading
import serial
import select
import time
import os

class SerialCommunicator(threading.Thread):
    def __init__(self, port: str, baud_rate: int, timeout: int, log_levels=None):
        super().__init__(daemon=True)
        self.is_connected = False

        self._baud_rate = baud_rate
        self._timeout = timeout
        self._port = port

        self._lock = threading.Lock()
        self._stop_flag = threading.Event()

        self._logger = LoggerFactory.get_logger(self.__class__.__name__, log_levels)

        self.init_serial()

    def init_serial(self):
        self._connector = serial.Serial()
        self._connector.port = self._port
        self._connector.baudrate = self._baud_rate
        self._connector.write_timeout = 0
        self._connector.timeout = 1

    def run(self):
        self._logger.info(f"Start connection loop on port: {self._port}")
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
            self._logger.info(f"Connection established on port: {self._port}")

        except serial.SerialException as e:
            self._logger.warning(f"Connection failed with port: {self._port}, try again in {1} sec")
            self.is_connected = False
        except Exception as e:
            self._logger.error(e)

    def close(self):
        try:
            self._logger.info(f"Closing port: {self._port}")
            with self._lock:
                self._connector.close()
        except serial.SerialException as e:
            self._logger.warning(f"Error closing serial port: {self._port}")
        except Exception as e:
            self._logger.error(e)

    def write(self, data):
        if (not self.is_connected):
            # self._logger.warning("No connection serial")
            return

        with self._lock:
            try:
                self._connector.write((data + '\n').encode())
                if (self._connector.in_waiting > 0):
                    read = self._connector.read_until(b'\n').decode().strip()
                    # print(read)
            except serial.SerialException as e:
                print(e)
                self._logger.warning("Writing to serial failed")
                self.is_connected = False
            except Exception as e:
                self._logger.error(e)

    def stop(self):
        self._logger.info("Stopped reconnecting.")
        self._stop_flag.set()
        with self._lock:
            self._connector.close()
