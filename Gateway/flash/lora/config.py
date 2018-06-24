""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.us.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'WIFI'
WIFI_PASS = 'PASS'

'''
known_nets format
key: 'Wifi SSD'
value: {'pass': 'password', wlan_config': ('ip', 'subnet_mask', 'gateway', 'DNS_server')}
'''
known_nets = {
    'Jeremiah': {'pwd': '', 'wlan_config': ('10.0.0.21', '255.255.255.0', '10.0.0.1', '8.8.8.8')},
    'WIFI': {'pwd': ''}
}

# for EU868
# LORA_FREQUENCY = 915100000
# LORA_GW_DR = "SF7BW125" # DR_5
# LORA_NODE_DR = 5

# for US915
LORA_FREQUENCY = 903900000
LORA_GW_DR = "SF7BW125" # DR_3
LORA_NODE_DR = 3
