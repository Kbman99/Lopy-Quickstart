import pycom
import time


def blink_led(color, blink_count, on_time, off_time):
    pycom.heartbeat(0)
    for i in range(blink_count):
        print("blink")
        pycom.rgbled(color)
        time.sleep(on_time)
        pycom.rgbled(0)
        time.sleep(off_time)
    pycom.heartbeat(True)


def blink_red(blink_count, on=0.5, off=0.2):
    blink_led(0x7f0000, blink_count, on, off)


def blink_green(blink_count, on=0.5, off=0.2):
    blink_led(0x007f00, blink_count, on, off)


def blink_yellow(blink_count, on=0.5, off=0.2):
    blink_led(0x7f7f00, blink_count, on, off)


def blink_orange(blink_count, on=0.5, off=0.2):
    blink_led(0xff8c00, blink_count, on, off)
