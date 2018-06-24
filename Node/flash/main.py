# main.py -- put your code here!
from lora.abp_node_US915 import setup_node
import gps_setup
from pytrack import Pytrack
import time
from machine import Timer, Pin, PWM
from _thread import start_new_thread
import servo
import rgb
import struct
import gc
from LIS2HH12 import LIS2HH12
from button import Manager, BUTTON
from time import sleep_ms, ticks_ms, ticks_diff
import pycom

gc.enable()

sent = False
pressed = False
last_pressed = 0
pressms = 0
longms = 2000
last_sent = 0
press_counter = 0


def blink_led(color, blink_count, on_time, off_time):
    pycom.heartbeat(False)
    for i in range(blink_count):
        print("blink")
        pycom.rgbled(color)
        time.sleep(on_time)
        pycom.rgbled(0)
        if i + 1 != blink_count:
            time.sleep(off_time)
    pycom.heartbeat(True)


def send_coords_loop(sensor, node, status_alert, manager):
    global pressed
    global last_pressed

    while True:
        pitch = sensor.pitch()
        roll = sensor.roll()
        pitch_data = struct.pack('>f', pitch)
        roll_data = struct.pack('>f', roll)
        while ticks_diff(last_pressed, ticks_ms())/1000 < 10 or pressed:
            time.sleep(ticks_diff(last_pressed, ticks_ms())/1000 + 10 if ticks_diff(last_pressed, ticks_ms())/1000 + 10 < 10 else 10)
        # coords = args[0].coordinates(debug=True)
        # lat = struct.pack('>f', coords[0])
        # long = struct.pack('>f', coords[1])
        status = bytes([status_alert])
        # pkt = lat + long + status
        pkt = pitch_data + roll_data + status
        print("Raw packet data: ", pkt)
        node.send(pkt)
        print("Packet sent via LOOP successfully")
        print("     Free memory: ", gc.mem_free())
        gc.collect()
        print("     Free memory after GC collect: ", gc.mem_free())
        print("----------------------------------------------")
        time.sleep(20)


def send_coords_button(sensor, node, status):
    pitch = sensor.pitch()
    roll = sensor.roll()
    pitch_data = struct.pack('>f', pitch)
    roll_data = struct.pack('>f', roll)
    # coords = args[0].coordinates(debug=True)
    # lat = struct.pack('>f', coords[0])
    # long = struct.pack('>f', coords[1])
    print("Status: {} ".format(status))
    status = bytes([status])
    # pkt = lat + long + status
    pkt = pitch_data + roll_data + status
    print("Raw packet data: ", pkt)
    node.send(pkt)
    print("Packet sent via BUTTON successfully")
    print("     Free memory: ", gc.mem_free())
    gc.collect()
    print("     Free memory after GC collect: ", gc.mem_free())
    print("----------------------------------------------")
    return 0
#
#
# def send_coords_button2(sensor, node, status):
#     pitch = sensor.pitch()
#     roll = sensor.roll()
#     pitch_data = struct.pack('>f', pitch)
#     roll_data = struct.pack('>f', roll)
#     # coords = args[0].coordinates(debug=True)
#     # lat = struct.pack('>f', coords[0])
#     # long = struct.pack('>f', coords[1])
#     status = bytes([status])
#     # pkt = lat + long + status
#     pkt = pitch_data + roll_data + status
#     print("Raw packet data: ", pkt)
#     node.send(pkt)
#     print("Packet sent via BUTTON successfully")
#     print("     Free memory: ", gc.mem_free())
#     gc.collect()
#     print("     Free memory after GC collect: ", gc.mem_free())
#     print("----------------------------------------------")
#     return 0
#
#
# def send_coords_button3(sensor, node, status):
#     pitch = sensor.pitch()
#     roll = sensor.roll()
#     pitch_data = struct.pack('>f', pitch)
#     roll_data = struct.pack('>f', roll)
#     # coords = args[0].coordinates(debug=True)
#     # lat = struct.pack('>f', coords[0])
#     # long = struct.pack('>f', coords[1])
#     status = bytes([status])
#     # pkt = lat + long + status
#     pkt = pitch_data + roll_data + status
#     print("Raw packet data: ", pkt)
#     node.send(pkt)
#     print("Packet sent via BUTTON successfully")
#     print("     Free memory: ", gc.mem_free())
#     gc.collect()
#     print("     Free memory after GC collect: ", gc.mem_free())
#     print("----------------------------------------------")
#     return 0


# def send_coords_alarm(args):
#     pitch = args[0].pitch()
#     roll = args[0].roll()
#     pitch_data = struct.pack('>f', pitch)
#     roll_data = struct.pack('>f', roll)
#     # coords = args[0].coordinates(debug=True)
#     # lat = struct.pack('>f', coords[0])
#     # long = struct.pack('>f', coords[1])
#     status = bytes([args[2]])
#     # pkt = lat + long + status
#     pkt = pitch_data + roll_data + status
#     print(pkt)
#     args[1].send(pkt)
#
#
# def get_coords(gps):
#     #print(gps.coordinates(debug=True))
#     print("Alarm func")
#
#
# def test_sleep(time, id):
#     timer = start_new_thread(setup_timer, (print_it, [5, id], time, True))
#     print("{} thread setup".format(id))
#
#
# def setup_timer(func_to_run, arg, time_interval, periodic=False):
#     return Timer.Alarm(func_to_run, s=time_interval, arg=arg, periodic=periodic)
#
#
# def setup_servo(pin, interval=5):
#     pwm = PWM(0, frequency=50)  # create PWM, with a frequency of 50Hz
#     pwm_c = pwm.channel(0, pin=pin, duty_cycle=0.05)  # .05 duty cycle starts servo all the way to the east
#     return setup_timer(servo_loop, time_interval=interval, arg=[pwm_c, 0.05], periodic=True)
#
#
# def servo_loop(arg):
#     print("servo loop running")
#     # read voltages (mV) at each node
#     # LDReast_v = LDR1.voltage()
#     # LDRwest_v = LDR2.voltage()
#     # compare voltages at each LDR node
#     # v_diff = LDReast_v - LDRwest_v
#     threshold = 100  # millivolts
#     # if v_diff > threshold:
#     #     moveservo = 1
#     # elif v_diff < (-1) * threshold:
#     #     moveservo = -1
#     # else:
#     #     moveservo = 0
#
#     # move servo in 1 degree increments every (interval) seconds
#     increment = 10 * 1 / 180  # 1 ms divided by 180 degrees =.0055555 increment
#     arg[1] += increment  # new duty cycle
#
#     # check to make sure d_cycle is within allowable range
#     if arg[1] < 0.05:
#         arg[1] = 0.05
#
#     if arg[1] > 0.1:
#         arg[1] = 0.1
#
#     # move servo to new location (incrementally)
#     arg[0].duty_cycle(arg[1])
#
#     print("servo moved")


def help(type, pin):
    print("Pin {} pressed, running {} func".format(pin.id(), type))


def help_sent(counter, pin):
    global press_counter
    global last_pressed
    global last_sent
    global pressed
    if press_counter >= 3:
        print("Pin {} pressed {} times. Resetting and sending!".format(pin.id(), counter))
        rgb.blink_green(3)
        press_counter = 0
        last_sent = ticks_ms()
        send_coords_button(acc, node, counter)
        print("diff:{}\npress count:{}".format(ticks_diff(last_pressed, ticks_ms()), press_counter))
        return
    sleep_ms(3000)
    if ticks_diff(last_pressed, ticks_ms()) >= 3000 and not pressed:
        print("Pin {} pressed {} times. Resetting and sending!".format(pin.id(), counter))
        rgb.blink_green(3)
        send_coords_button(acc, node, counter)
        press_counter = 0
        last_sent = ticks_ms()
    else:
        print("didnt send yet @ {} presses".format(press_counter))
    print('-----------------------------------------')


def button_pressed():
    global pressed

    pressed = True


def button_pressed_sent():
    global pressed
    global press_counter
    global last_pressed

    last_pressed = ticks_ms()

    press_counter += 1
    if press_counter == 1:
        rgb.blink_red(2, 0.8, 0.4)
    elif press_counter == 2:
        rgb.blink_orange(2, 0.8, 0.4)
    else:
        rgb.blink_green(2, 0.8, 0.4)


def button_depressed():
    global pressed
    global last_pressed

    pressed = False
    # last_pressed = ticks_ms()


def can_send(delay):
    global last_sent

    return ticks_ms() - last_sent > 6000


def can_press_sent(delay):
    global last_sent

    return ticks_diff(last_sent, ticks_ms()) > delay


def can_press(delay):
    global last_pressed
    global pressed
    # print("last pressed = {}\n delay = {}\ntime = {}\ndiff between = {}".format(last_pressed, delay,
    #                                                                             time.time(), time.time() - last_pressed))
    # print("--------------------------")
    # print('\n')
    return time.time() - last_pressed > delay and not pressed


def press(pin):
    global pressms
    global longms
    global press_counter
    global pressed

    print("{} pressed!".format(pin))
    # state = disable_irq()
    # If never pressed, store press time
    if pressms == 0:
        pressms = ticks_ms()
    else:
        # If pressed within 500 ms of first press, discard (button bounce)
        if ticks_diff(pressms, ticks_ms()) < 400:
            return

    # Wait for value to stabilize for 10 ms
    i = 0
    while i < 10:
        sleep_ms(1)
        if pin() == 0:
            i = 0
        else:
            i += 1

    if not can_press_sent(5000):
        # button_pressed()
        # print("CANT PRESS YET! HAHA")
        # print("button done")
        # print('-------------------')
        # print('\n')
        # enable_irq(state)
        rgb.blink_red(1, 1, 1)
        # button_depressed()
        return

    # button_pressed_sent()

    # Measure button press duration.
    pressed = True
    while pin() == 1:
        i += 1
        if i > longms:
            break
        sleep_ms(1)
    print(i)
    button_depressed()
    # Trigger short or long press
    if i > longms:
        button_pressed_sent()
        start_new_thread(help_sent, (press_counter, pin))
    # else:
        # start_new_thread(help, ('long', pin))

    # Wait for button release.
    while pin() == 1:
        pass
    pressms = 0
    #button_depressed()
    gc.collect()
    return 0


node = setup_node()
py = Pytrack()
acc = LIS2HH12()
gps = gps_setup.setup_gps()

manager = Manager(acc, node, 1)
# manager.alarm_func = send_coords_alarm
# manager.alarm = manager.set_alarm()
# manager.alarm.cancel()
p1 = Pin('P8', mode=Pin.IN, pull=Pin.PULL_DOWN)
p1.callback(Pin.IRQ_RISING, press)
# p2 = Pin('P11', mode=Pin.IN, pull=Pin.PULL_DOWN)
# p2.callback(Pin.IRQ_RISING, press)
# p3 = Pin('P9', mode=Pin.IN, pull=Pin.PULL_DOWN)
# p3.callback(Pin.IRQ_RISING, press)

# button_1 = BUTTON(acc, node, manager, pid='P8', status_alert=1)
# print("Button_1 value is " + str(button_1.pin()))
# button_1.short = send_coords_button1
# button_1.long = send_coords_button1
#
# button_2 = BUTTON(acc, node, manager, pid='P11', status_alert=2)
# print("Button_2 value is " + str(button_2.pin()))
# button_2.short = send_coords_button2
# button_2.long = send_coords_button2
#
# button_3 = BUTTON(acc, node, manager, pid='P9', status_alert=3)
# print("Button_3 value is " + str(button_3.pin()))
# button_3.short = send_coords_button3
# button_3.long = send_coords_button3

# pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
# pin.callback(Pin.IRQ_FALLING, get_coords_button, arg=(acc, node, 0))

try:
    start_new_thread(send_coords_loop, (acc, node, 0, manager))
    #timer = setup_timer(get_coords, gps, 5, True)
    #timer_send = setup_timer(send_coords_alarm, [acc, node, 1], 10, True)
except Exception as e:
    print(e)
print("Setup complete!")
