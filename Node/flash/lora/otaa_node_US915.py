""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import LoRa
import socket
import binascii
import struct
import time
from . import config

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTA authentication params
dev_eui = binascii.unhexlify('240AC4FFFE024038'.replace(' ',''))
app_eui = binascii.unhexlify('70B3D57ED000A7F5'.replace(' ',''))
app_key = binascii.unhexlify('68048150FD4364602902B6166BE77698'.replace(' ',''))

# remove all the channels
for channel in range(0, 72):
    lora.remove_channel(channel)

# set all channels to the same frequency (must be before sending the OTAA join request)
for channel in range(0,72):
    lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=4)

# join a network using OTAA
print("Joining network...")
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
join_wait = 0
while True: 
    time.sleep(2.5)
    if not lora.has_joined():
        print('Not joined yet...')
        join_wait += 1
        if join_wait == 5:
            lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
            join_wait = 0
    else:
        break

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# make the socket blocking
s.setblocking(False)

time.sleep(5.0)

for i in range (200):
    pkt = b'PKT #' + bytes([i])
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)
