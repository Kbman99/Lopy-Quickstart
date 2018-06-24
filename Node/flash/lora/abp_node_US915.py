from network import LoRa
import socket
import binascii
import struct
import time
from . import config
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack


# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
def setup_node():
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

    # create an ABP authentication params
    dev_addr = struct.unpack(">l", binascii.unhexlify('260210B3'.replace(' ','')))[0]
    nwk_swkey = binascii.unhexlify('EC6368A1D013E22B7B4BAF96645DCF48'.replace(' ',''))
    app_swkey = binascii.unhexlify('5A60972B94850CA94141ED76FAC0DEDD'.replace(' ',''))

    # remove all the channels
    for channel in range(0, 72):
        lora.remove_channel(channel)

    # set all channels to the same frequency (must be before sending the OTAA join request)
    for channel in range(0, 72):
        lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=4)

    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

    # make the socket blocking
    s.setblocking(False)

    return s


def test():
    s = setup_node()
    py = Pytrack()
    acc = LIS2HH12()

    for i in range(200):
        pitch = acc.pitch()
        roll = acc.roll()
        pitch_data = struct.pack('>f', pitch)
        roll_data = struct.pack('>f', roll)
        print("Pitch data: ", pitch_data)
        print("Roll data: ", roll_data)
        pkt = pitch_data + roll_data
        # pkt = b'PKT #' + bytes([i])
        print('Sending:', pkt)
        s.send(pkt)
        time.sleep(4)
        # rx, port = s.recvfrom(256)
        rx = s.recv(256)
        print(rx)
        if rx:
            # print('Received: {}, on port: {}'.format(rx, port))
            print('Received: {}, on port:'.format(rx))
        time.sleep(6)


# while True:
#     #s.send(b'Hola LORAWAN')
#     s.send(bytes([0xFF,0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))#Send some sample Bytes
#     print("packet send")
#     time.sleep(4)
#     time.sleep(4)
#     time.sleep(4)
#     time.sleep(4)