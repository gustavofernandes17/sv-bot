import os

ESP32CAM_IP_ADRESS = '192.168.43.144:80'

AUTH_TOKEN = '1vcvjKLwCs5ZNUAYMy4YIMuIFuG_3qqxjdD2EEC5npvwLS56H'

os.execv(os.getcwd() + '/ngrok', ['ngrok', 'tcp', ESP32CAM_IP_ADRESS, '--authtoken', AUTH_TOKEN])