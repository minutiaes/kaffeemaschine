import network
import usocket as socket
from machine import Pin
from time import sleep

import esp
esp.osdebug(None)

import gc
gc.collect()

AP_ssid = 'KAFFEEMASCHINE'
AP_password = 'abc123456'

led = Pin(2, Pin.OUT)
##sta = network.WLAN(network.STA_IF)
##if not sta.isconnected():
##    print('connecting to network...')
##    sta.active(True)
##    sta.connect('Nudelbox', 'zRfrdznbpae3')
##    while not sta.isconnected():
##        pass
##print('network config:', sta.ifconfig())
ap = network.WLAN(network.AP_IF)
ap.config(essid=AP_ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=AP_password)
ap.active(True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen(5)

def parse_data(data):
    data = data.split(',')
    choice = data[0]
    hour = data[24][12:]
    minute = data[25][7:]
    repetition = data[len(data)-1][:-1]
    return choice, hour, minute, repetition

while True:
    try:
        print('Controlling whether there is an ongoing Socket Connection')
        conn.send('\n')
        print('There is an ongoing Socket Connection')
    except:        
        print('There is NOT any ongoing Socket Connection\nWaiting for Socket Connection')
        conn, addr = s.accept()
        print('Socket Connection is realized \nWaiting for request')
    data = str(conn.recv(1024))
    try:
        data = parse_data(data)
    except:
        print('Error!!!')
    print(data)
    if(data[0] == "b'espresso"):
        led.value(1)
        conn.send('Request is put into process\n\n{} at {}:{}\n\n{}'.format('Espresso', data[1], data[2], data[3]))
        sleep(0.5)
        led.value(0)
    elif(data[0] == "b'doublespresso"):
        led.value(1)
        conn.send('Request is put into process\n{}'.format('doublespresso'))
        sleep(0.5)
        led.value(0)
    else:
        conn.send('Choice not recognized\n')
        continue
    conn.close()
    print('Connection closed')
