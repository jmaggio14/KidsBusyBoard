import board
import busio
import digitalio
import displayio
import terminalio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon

import time
import json
import struct
import struct
from collections import namedtuple


from Timer import Timer

HEIGHT = 32
WIDTH  = 32
N_PIX              = HEIGHT*WIDTH
BITDEPTH = 2
N_SHADES_PER_COLOR = 2**BITDEPTH # 4 shaders per channel
N_COLORS = N_SHADES_PER_COLOR ** 3 # total color combos are shades^(number of color channels)
MAX_VAL = 0xFF
TIMEOUT = 2

RED   = 0xFF0000
GREEN = 0x00FF00
Blue  = 0x0000FF

TX_RX_LED = digitalio.DigitalInOut(board.LED)
TX_RX_LED.direction = digitalio.Direction.OUTPUT




# #############################################################################

# --- Display setup ---
bitmap = displayio.Bitmap(WIDTH, HEIGHT, N_COLORS)

# build all possible colors in the palette
color_multiplier = (MAX_VAL / N_SHADES_PER_COLOR)
palette = displayio.Palette(N_COLORS)
for r in range(N_SHADES_PER_COLOR):
    red   = int(r * color_multiplier) << 16

    for g in range(N_SHADES_PER_COLOR):
        green = int(g * color_multiplier) << 8

        for b in range(N_SHADES_PER_COLOR):
            blue  = int(b * color_multiplier)
            palette[r*g*b] = red & green & blue


matrix = Matrix(width=WIDTH, height=HEIGHT)
display = matrix.display

# tile_grid = displayio(bitmap, pixel_shader=palette)
# group.append(tile_grid)

class DisplayLocation():
    def __init__(self, display_objs):
        assert(len(display_objs) >= 2)
        self.display_objs = display_objs
        self.color_times = {"red":time.time(),
                            "green":time.time(),
                            "blue":time.time(),
                            }

        self.shutoff_time = time.time()
        self.default_color = 0xFFFFFF
        self.current_color = 0
        default_active_shape_name = sorted(self.display_objs.keys())[0]
        self.active_shape = self.display_objs[default_active_shape_name]
        self.inactive_shapes = [self.display_objs[d] for d in (set(self.display_objs) - set(default_active_shape_name))]


    def set_color(self, color, duration):
        # print(f"setting color to {color}")
        self.color_times[color.lower()] = time.time() + duration

    def set_shape(self, shape_name):
        # print(f"setting shape_name to {shape_name}")
        self.active_shape = self.display_objs[shape_name]
        undesired_objects = [self.display_objs[d] for d in set(self.display_objs).remove(shape_name)]

    def turn_on(self, duration):
        self.shutoff_time = time.time() + duration
    
    def turn_off(self):
        # set turn off time for one second in the past for clarity
        self.shutoff_time = time.time() - 1 
        
    def update(self):
        now = time.time()
        color = 0
        if now < self.color_times['red']:
            color += RED
        if now < self.color_times['green']:
            color += GREEN
        if now < self.color_times['blue']:
            color += BLUE

        if color == 0:
            color = self.default_color

        self.current_color = color if (now < self.shutoff_time) else None

        self.active_shape.fill = self.current_color
        for shape in self.inactive_shapes:
            shape.fill = None

# centers for each portion
# top left: 8,8
# top right: 8,24
# bottom right: 24,24
# bottom right: 24,8

# Triangle:
#  top left
#    A: 3,12
#    B: 7,3
#    C: 12,12
#  top right
#    A: 3+16,12
#    B: 7+16,3
#    C: 12+16,12


all_locations = {}
all_locations['top-left'] = DisplayLocation({'circle' : Circle(7, 7, 4, fill=None),
                                          'rect'   : Rect(4, 3, 8, 8, fill=None),
                                          'tri'    : Triangle(3, 12, 7, 3, 12, 12, fill=None),
                                            })

all_locations['top-right'] = DisplayLocation({'circle' : Circle(7+16, 7, 4, fill=None),
                                           'rect'   : Rect(4+16, 3, 8, 8, fill=None),
                                           'tri'    : Triangle(3+16, 12, 7+16, 3, 12+16, 12, fill=None),
                                            })

all_locations['bottom-right'] = DisplayLocation({'circle' : Circle(7+16, 7+16, 4, fill=None),
                                              'rect'   : Rect(4+16, 3+16, 8, 8, fill=None),
                                              'tri'    : Triangle(3+16, 12+16, 7+16, 3+16, 12+16, 12+16, fill=None),
                                                })

all_locations['bottom-left'] = DisplayLocation({'circle' : Circle(7, 7+16,  4, fill=None),
                                             'rect'   : Rect(4, 3+16, 8, 8, fill=None),
                                             'tri'    : Triangle(3, 12+16, 7, 3+16, 12, 12+16, fill=None),
                                                })



group = displayio.Group() 

# tile_grid = displayio.TileGrid(bitmap)
# group.append(tile_grid)

for loc in all_locations.values():
    for display_shape in loc.display_objs.values():
            group.append(display_shape)


display.root_group = group

START_CODE = "MsgStart"
header_format = "8s16slL"
raw_header_size = struct.calcsize(header_format)
# Header = namedtuple("Header", ("start_code", "dtype", "packet_num", "length") )

class Header():
    def __init__(self, start_code, dtype, packet_num, length):
        self.start_code = start_code.decode('utf-8')
        self.dtype      = dtype.decode('utf-8')
        self.packet_num = packet_num
        self.length     = length

    def __str__(self):
        return f"start_code: {self.start_code}, dtype: {self.dtype}, packet_num: {self.packet_num}, length: {self.length}"


class Comm():
    # _________________________________________________________________________
    def __init__(self, baud=9600):
        self.uart = busio.UART(board.TX,
                                 board.RX,
                                 baudrate=baud,
                                #  parity=busio.UART.Parity.EVEN,
                                #  stop=2,
                                 receiver_buffer_size=1024,
                                 )
        self.packet_num = 0
        self.flush()

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
            time.sleep(0.1)
            return None,None
            # print(self.in_waiting())
            # print("waiting for header...")
            # return Header(START_CODE,"none",-1,0), bytes(0)

        TX_RX_LED.value = True
        raw_header =  self.uart.read(raw_header_size)
        unpacked = struct.unpack(header_format, raw_header)
        # print(unpacked)
        try:
            if unpacked[0] == START_CODE.encode('utf-8'):
                hdr = Header( *unpacked )
            else:
                msg = "unable to decode header!!! Flushing input buffer!"
                print(hdr)
                self.flush()
                TX_RX_LED.value = False
                return None,None
        except Exception:
            print(f"error attempting to decode {unpacked[0]}. Flushing!")
            self.flush()
            return None,None

        timer = Timer()
        timer.countdown = TIMEOUT

        timeout = False
        while True:
            # check if paylaod is in the receive buffer
            data_ready = (self.in_waiting() >= hdr.length)
            if data_ready:
                print(f"data is ready (ready={self.in_waiting()} Bytes, min = {hdr.length}Bytes)")
                break

            # update the timeout check
            timeout = (timer.countdown == 0)
            if timeout:
                print("breakout condition!!!!!")
                break
            
            time.sleep(0.01)
        
        if data_ready:
            payload = self.uart.read(hdr.length)
            self.acknowledge(hdr.packet_num)
            TX_RX_LED.value = False
        else:
            self.error(f"payload data not received for packet num {hdr.packet_num} with type {hdr.dtype} and length {hdr.length}")
            TX_RX_LED.value = False
            return None,None

        # self.transmit(payload, dtype=hdr.dtype)
        # print(payload)
        # print(f"received header {hdr}")
        return hdr, payload
            
    # _________________________________________________________________________
    def transmit(self, bin_data, dtype='generic'):
        hdr = struct.pack(header_format, START_CODE, dtype, self.packet_num, len(bin_data))
        self.uart.write( hdr + bin_data)
        # print(hdr, bin_data)
        self.packet_num += 1

    # _________________________________________________________________________
    def transmit_text(self, msg, dtype):
        bin_data = msg.lower().encode('utf-8')
        # print(bin_data)
        self.transmit(bin_data, dtype)

    # _________________________________________________________________________
    def acknowledge(self, packet_num):
        self.transmit_text(str(packet_num), "acknowledged")

    # _________________________________________________________________________
    def error(self, msg):
        pass
        # self.transmit_text(msg, dtype="error")


matrix = Matrix()
display = matrix.display

comm = Comm()
index = 0
while True:
    
    # .........................................................................
    header,payload = comm.read()
    # print( f"Received Header of size{raw_header_size}: ", str(header) )
    # print( f"Received Payload: ", str(payload) )
    print(f"received {header} with payload {payload}")
    

    # .........................................................................
    if header is not None:
        if header.dtype == "SetShape":
            for ds in all_locations:
                ds.set_shape( payload['shape'] )

        elif header.dtype == "SetColor":
            for ds in all_locations:
                ds.set_color(payload['color'], payload['duration'])

        elif header.dtype == "LightOn":
            loc = all_locations[ payload['location'] ]
            loc.turn_on( payload['duration'] )

        elif header.dtype == "LightOff":
            loc = all_locations[ payload['location'] ]
            loc.turn_off()

        else:
            comm.error(f"unknown packet type: {header.dtype}. Flushing input buffer!")
        # comm.flush()


    # print("heartbeat")
    # update all the shapes in a loop
    for loc in all_locations.values():
        loc.update()

    time.sleep(0.2)
        # reas


    




