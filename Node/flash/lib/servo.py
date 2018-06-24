# code for controlling servo
from machine import ADC, PWM, Timer
import time

adc = ADC(0)

# create channels for each LDR
# using attenuation of 11db gives us up to 3.3v to leave at each LDR node
# LDR1 = adc.channel(Pin='P16', attn=ADC.ATTN_11DB)
# LDR2 = adc.channel(Pin='P17', attn=ADC.ATTN_11DB)
# PWM


def test_servo():
    pwm = PWM(0, frequency=50)  # create PWM, with a frequency of 50Hz
    pwm_c = pwm.channel(0, pin='P4', duty_cycle=0.05)  # .05 duty cycle starts servo all the way to the east
    d_cycle = 0.05  # initial duty cycle value
    while True:
        # 0.03 and 0.12-0.16 work, though 0.12 seems to give best results

        print("moving to d cycle 0.03")
        pwm_c.duty_cycle(0.03)
        time.sleep(2)
        print("moving to d cycle 0.12")
        pwm_c.duty_cycle(0.12)
        time.sleep(5)


def start_servo():
    LDR1 = adc.channel(Pin='P16', attn=ADC.ATTN_11DB)
    LDR2 = adc.channel(Pin='P17', attn=ADC.ATTN_11DB)
    pwm = PWM(0, frequency=50)  # create PWM, with a frequency of 50Hz
    pwm_c = pwm.channel(0, pin='P4', duty_cycle=0.05)  # .05 duty cycle starts servo all the way to the east
    d_cycle = 0.05  # initial duty cycle value
    while True:  # run continuosly
        # read voltages (mV) at each node
        LDReast_v = LDR1.voltage()
        LDRwest_v = LDR2.voltage()
        # compare voltages at each LDR node
        v_diff = LDReast_v - LDRwest_v
        threshold = 100  # millivolts
        if v_diff > threshold:
            moveservo = 1
        elif v_diff < (-1) * threshold:
            moveservo = -1
        else:
            moveservo = 0

        # move servo in 1 degree increments every (interval) seconds
        increment = 10 * 1 / 180  # 1 ms divided by 180 degrees =.0055555 increment
        d_cycle += increment  # new duty cycle

        # check to make sure d_cycle is within allowable range
        if d_cycle < 0.05:
            d_cycle = 0.05

        if d_cycle > 0.1:
            d_cycle = 0.1

        # move servo to new location (incrementally)
        pwm_c.duty_cycle(d_cycle)

        print("servo moved")
        time.sleep(5)
