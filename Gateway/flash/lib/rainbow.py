import pycom
import time


def to_hex(r, g, b):
    h = int(r * 255)
    h = h * 256 + int(g * 255)
    return h * 256 + int(b * 255)


def hsv_to_rgb(h, s, v):  # Taken from colorsys.py on github
    if s == 0.0: return [v, v, v]
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0: return [v, t, p]
    if i == 1: return [q, v, p]
    if i == 2: return [p, v, t]
    if i == 3: return [p, q, v]
    if i == 4: return [t, p, v]
    if i == 5: return [v, p, q]


# Note - hsv_to_rgb returns floating point fractional values (0-1.0)

# Disable heartbeat (otherwise setting the LED colour will fail).
pycom.heartbeat(False)

n = 360  # Colour range  # (0-360 degrees)
s = 1.0  # Saturation    # (0-1.0)
v = 0.5  # Vibrance      # (0-1.0)

while True:  # Loop for ever.
    for j in range(0, n, 1):
        r, g, b = hsv_to_rgb(j * 1.0 / n, s, v)
        pycom.rgbled(to_hex(r, g, b))
        time.sleep(0.02)
