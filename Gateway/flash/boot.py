# boot.py -- run on boot-up
import os
from machine import UART
import machine
import time
from lora import config
uart = UART(0, 115200)
os.dupterm(uart)

known_nets = {
    'Jeremiah': {'pwd': '7546664988', 'wlan_config':  ('10.0.0.21', '255.255.255.0', '10.0.0.1', '8.8.8.8')}, # (ip, subnet_mask, gateway, DNS_server)
    'linksys': {}
}

if machine.reset_cause() != machine.SOFT_RESET:
    from network import WLAN
    wl = WLAN()
    wl.mode(WLAN.STA)
    original_ssid = wl.ssid()
    original_auth = wl.auth()

    print("Scanning for known wifi nets")
    available_nets = wl.scan()
    nets = frozenset([e.ssid for e in available_nets])

    known_nets_names = frozenset([key for key in config.known_nets])
    net_to_use = list(nets & known_nets_names)


    try:
        net_to_use = net_to_use[0]
        net_properties = config.known_nets[net_to_use]
        if 'wlan_config' in net_properties:
            wl.ifconfig(config=net_properties['wlan_config'])
        if 'pwd' in net_properties:
            pwd = net_properties['pwd']
            sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
            print("Attempting to connect to {}...".format(net_to_use))
            wl.connect(net_to_use, (sec, pwd), timeout=10001)
        else:
            print("Attempting to connect to {}...".format(net_to_use))
            wl.connect(net_to_use, timeout=10000)
        while not wl.isconnected():
            machine.idle() # save power while waiting
        print("Connected to " + net_to_use + " with an IP address: " + wl.ifconfig()[0])

    except Exception as e:
        print("Failed to connect to any known network, going into AP mode")
        wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
# import machine
# from network import WLAN
# wlan = WLAN() # get current object, without changing the mode
#
# if machine.reset_cause() != machine.SOFT_RESET:
#     wlan.init(mode=WLAN.STA)
#     # configuration below MUST match your home router settings!!
#     wlan.ifconfig(config=('10.0.0.20', '255.255.255.0', '10.0.0.1', '8.8.8.8'))
#
# if not wlan.isconnected():
#     # change the line below to match your network ssid, security and password
#     wlan.connect('Jeremiah', auth=(WLAN.WPA2, '7546664988'), timeout=5000)
#     while not wlan.isconnected():
#         machine.idle() # save power while waiting

# # boot.py -- run on boot-up
# import os
# import machine
# from machine import UART
# uart = UART(0, 115200)
# os.dupterm(uart)
#
# known_nets = {
#     'Jeremiah': {'pwd': '7546664988', 'wlan_config':  ('10.0.0.20', '255.255.255.0', '10.0.0.1', '8.8.8.8')}, # (ip, subnet_mask, gateway, DNS_server)
# }
#
# if machine.reset_cause() != machine.SOFT_RESET:
#     from network import WLAN
#     wl = WLAN()
#     wl.mode(WLAN.STA)
#     original_ssid = wl.ssid()
#     original_auth = wl.auth()
#
#     print("Scanning for known wifi nets")
#     available_nets = wl.scan()
#     nets = frozenset([e.ssid for e in available_nets])
#
#     known_nets_names = frozenset([key for key in known_nets])
#     net_to_use = list(nets & known_nets_names)
#     try:
#         net_to_use = net_to_use[0]
#         net_properties = known_nets[net_to_use]
#         pwd = net_properties['pwd']
#         sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
#         if 'wlan_config' in net_properties:
#             wl.ifconfig(config=net_properties['wlan_config'])
#         wl.connect(net_to_use, (sec, pwd), timeout=10000)
#         while not wl.isconnected():
#             machine.idle() # save power while waiting
#         print("Connected to "+net_to_use+" with IP address:" + wl.ifconfig()[0])
#
#     except Exception as e:
#         print("Failed to connect to any known network, going into AP mode")
#         wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)