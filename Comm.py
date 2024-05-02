import serial
import struct
import time
from collections import namedtuple
import json
import queue
from Timer import Timer
import threading

TIMEOUT = 2

START_CODE = "MsgStart"
header_format = "8s16slL"
raw_header_size = struct.calcsize(header_format)
# Header = namedtuple("Header", ("start_code", "dtype", "packet_num", "length") )

class Header():
    def __init__(self, start_code, dtype, packet_num, length):
        self.start_code = start_code
        self.dtype      = dtype
        self.packet_num = packet_num
        self.length     = length

    def __str__(self):
        return f"start_code: {self.start_code}, dtype: {self.dtype}, packet_num: {self.packet_num}, length: {self.length}"



class Comm():
    # _________________________________________________________________________
    def __init__(self, path, baud=9600):
        self.uart = serial.Serial(path,
                                    baud,
                                    # stopbits=serial.STOPBITS_TWO,
                                    )
        # self.uart.parity = serial.PARITY_EVEN
        self.packet_num = 0
        self.queue = queue.Queue()
        # launch transmit thread
        self.thread = threading.Thread(target=self.__transmit_thread, daemon=True).start()

    # _________________________________________________________________________
    def flush(self):
        self.uart.reset_input_buffer()

    # _________________________________________________________________________
    def in_waiting(self):
        return self.uart.in_waiting

    # _________________________________________________________________________
    def read(self):
        # return nothing we don't have enough to populate a header
        if self.in_waiting() < raw_header_size:
            return Header(START_CODE,"none",-1,0), bytes(0)

        raw_header =  self.uart.read(raw_header_size)
        hdr = Header( *struct.unpack(header_format, raw_header) )

        if hdr.start_code != START_CODE:
            self.error("unable to decode header!!! Flushing input buffer!")
            # self.flush()


        timer = Timer()
        timer.countdown = TIMEOUT

        timeout = False
        while True:
            # check if paylaod is in the receive buffer
            data_ready = (self.in_waiting() >= hdr.length)
            if data_ready:
                break

            # update the timeout check
            timeout = (timer.countdown == 0)
            if timeout:
                break
            
            time.sleep(0.01)
        
        payload = self.uart.read(hdr.length)

        if data_ready:
            self.acknowledge(hdr.packet_num)
        else:
            self.error(f"payload data not received for packet num {hdr.packet_num} with type {hdr.dtype} and length {hdr.length}")

        return hdr, payload
    
    # _________________________________________________________________________
    def __transmit_thread(self):
        timer = Timer()
        while True:
            msg = self.queue.get()
            self.uart.write(msg)
            print("got message!")

            # Wait until we get a response
            # timer.countdown = TIMEOUT
            # while timer.countdown:
            packet = self.read()
            # print
            # if (packet[0].dtype.decode('utf-8').strip() == "acknowledged") and (packet[0].packet_num == self.packet_num):
            #     print("msg acknowledged")
            # else:
            #     print(f"uncertain response: {packet[0]}, {packet[1]}")

            self.packet_num += 1
            self.queue.task_done()

    # _________________________________________________________________________
    def transmit(self, bin_data, dtype='generic'):
        # print(START_CODE)
        # print(START_CODE.encode('utf-8'))
        hdr = struct.pack(header_format, START_CODE.encode('utf-8'), dtype.encode('utf-8'), self.packet_num, len(bin_data))
        print("queuing")
        self.queue.put( hdr + bin_data)

    # _________________________________________________________________________
    def transmit_text(self, msg, dtype):
        bin_data = msg.lower().encode('utf-8')
        self.transmit(bin_data, dtype)

    # _________________________________________________________________________
    def acknowledge(self, packet_num):
        pass
        # self.transmit_text(str(packet_num), "acknowledged")

    # _________________________________________________________________________
    def error(self, msg):
        pass
        # self.transmit_text(msg, dtype="error")
