""" LoPy LoRaWAN Nano Gateway example usage """

from . import config
from .nanogateway import NanoGateway
import pycom
import time


def start_lora():
    pycom.heartbeat(False)
    pycom.rgbled(0x7f7f00)
    nanogw = NanoGateway(
        id=config.GATEWAY_ID,
        frequency=config.LORA_FREQUENCY,
        datarate=config.LORA_GW_DR,
        ssid=config.WIFI_SSID,
        password=config.WIFI_PASS,
        server=config.SERVER,
        port=config.PORT,
        ntp_server=config.NTP,
        ntp_period=config.NTP_PERIOD_S
        )
    pycom.heartbeat(False)
    nanogw.start()
    for i in range(5):
        pycom.rgbled(0x007f00)
        time.sleep(0.5)
        pycom.rgbled(0xfff)
        time.sleep(0.5)
    nanogw._log('You may now press ENTER to use the REPL')
    input()
