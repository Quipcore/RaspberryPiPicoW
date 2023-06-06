import socket
from time import sleep

import network
from machine import reset
from picozero import pico_temp_sensor, pico_led

ssid = 'lido'
password = 'Theyokertma'


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip_connect = wlan.ifconfig()[0]
    print(f'Connected on {ip_connect}')
    return ip_connect


def open_socket(ip_open):
    # Open a socket
    port = 80
    address = (ip_open, port)
    connection_socket = socket.socket()
    connection_socket.bind(address)
    connection_socket.listen(1)
    print(f'Port: {port}, Connection: {connection_socket}')
    return connection_socket


def webpage(temperature, state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Board temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)


def serve(connection_server):
    # Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection_server.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request == '/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)

except KeyboardInterrupt:
    reset()
