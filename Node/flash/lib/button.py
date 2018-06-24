from time import sleep_ms, ticks_ms, ticks_diff, time
from machine import Pin, disable_irq, enable_irq, Timer
from _thread import start_new_thread
import gc
import rgb


class Manager:

    def __init__(self, sensor, node, status, delay=5):
        self.pressed = False
        self.last_pressed = 0
        self.current_status = None
        self.status_time = 0
        self.delay = delay
        self.sensor = sensor
        self.node = node
        self.status = status
        self.alarm = None

    def can_press(self):
        print("last pressed = {}\n delay = {}\ntime = {}\ndiff between = {}".format(self.last_pressed, self.delay,
                                                                                    time(), time() - self.last_pressed))
        print("--------------------------")
        print('\n')
        return time() - self.last_pressed > self.delay and not self.pressed

    def set_alarm(self):
        return Timer.Alarm(self.alarm_func, s=10, arg=[self.sensor, self.node, self.status], periodic=True)

    def alarm_func(self):
        pass

    def button_depressed(self):
        # print("reinitiating alarm")
        self.pressed = False
        self.last_pressed = time()
        # self.alarm = self.set_alarm()
        # print(self.alarm)

    def button_pressed(self):
        # print("cancelling alarm")
        # self.alarm.cancel()
        self.pressed = True
        # print(self.alarm)


class BUTTON:

    def __init__(self, sensor, node, manager, status_alert=0, pid='P10', longms=1000):
        self.manager = manager
        self.pressms = 0
        self.longms = longms
        self.pin = Pin(pid, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.pin.callback(Pin.IRQ_RISING, self.press)
        self.sensor = sensor
        self.node = node
        self.status_alert = status_alert
        self.args = (self.sensor, self.node, self.status_alert)
        print("Button setup!")

    def check_delay(self):
        return self.manager.can_press()

    def long(self):
        pass

    def short(self):
        pass

    def press(self, pin):
        print("{} pressed!".format(pin))
        # state = disable_irq()
        # If never pressed, store press time
        if self.pressms == 0:
            self.pressms = ticks_ms()
        else:
            # If pressed within 500 ms of first press, discard (button bounce)
            if ticks_diff(self.pressms, ticks_ms()) < 500:
                return

        # Wait for value to stabilize for 10 ms
        i = 0
        while i < 10:
            sleep_ms(1)
            if self.pin() == 0:
                i = 0
            else:
                i += 1

        if not self.check_delay():
            self.manager.button_pressed()
            print("CANT PRESS YET! HAHA")
            print("button done")
            print('-------------------')
            print('\n')
            # enable_irq(state)
            rgb.blink_red(1, 1, 1)
            self.manager.button_depressed()
            return

        self.manager.button_pressed()

        # Measure button press duration
        while self.pin() == 1:
            i += 1
            if i > self.longms:
                break
            sleep_ms(1)

        # Trigger short or long press
        if i > self.longms:
            start_new_thread(self.long, self.args)
        else:
            start_new_thread(self.short, self.args)

        # Wait for button release.
        while self.pin() == 1:
            pass
        self.pressms = 0
        # enable_irq(state)
        rgb.blink_green(3)
        self.manager.button_depressed()
        gc.collect()
        print("button done!!")
        return 0
