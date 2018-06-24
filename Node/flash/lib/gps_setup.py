import machine
import math
import network
import os
import time
import utime
from machine import RTC
from machine import SD
from machine import Timer
from L76GNSS import L76GNSS
from pytrack import Pytrack
# setup as a station

import gc


def setup_gps():
    time.sleep(2)
    gc.enable()

    rtc = RTC()
    rtc.ntp_sync("pool.ntp.org")
    utime.sleep_ms(750)
    print('\nRTC Set from NTP to UTC:', rtc.now())
    utime.timezone(7200)
    print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')
    if rtc.now()[0] == 1970:
        print("Datetime could not be automatically set")
        date_str = (input('Enter datetime as list separated by commas (y, m, d, h, min, s): ')).split(',')
        date_str = tuple([int(item) for item in date_str])
        try:
            rtc.init(date_str)
            print('Time successfully set to ', rtc.now(), '\n')
        except Exception:
            print("Failed to set time...")
    py = Pytrack()
    l76 = L76GNSS(py, timeout=30)
    print("GPS Timeout is {} seconds".format(30))
    chrono = Timer.Chrono()
    chrono.start()

    # while (True):
    #     coord = l76.coordinates(debug=True)
    #     print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
    return l76
