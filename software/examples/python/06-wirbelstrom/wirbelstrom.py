
# !/usr/bin/python3
#
# Start Measure mit TX -> "A", wait 1s , dann RX 8 Byte vom Sensor, Sio Timeout 10s wenn no Antwort !
# 1 x Sensor abfragen, ret -> Messwerte oder Fehlermeldung.

import time, math
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BCM)

RE = 23
DE = 24
#port = "/dev/ttyS0"    
port = "/dev/ttyAMA0"

if __name__ == "__main__":

  GPIO.setwarnings(False)
  GPIO.cleanup()
  GPIO.setup(RE, GPIO.OUT)
  GPIO.setup(DE, GPIO.OUT)

  # init max3471
  GPIO.output(RE, GPIO.HIGH) # RX und TX OFF !
  GPIO.output(DE, GPIO.LOW)

  # Init UART
  ser = serial.Serial(port, 115200,8,'N', 1, timeout = 10) # timeout als Notfall :-)

  ser.flushInput()
  ser.flushOutput()

  # Zeichen "A" zum Sensor senden, Measure starten

  # RS 485 auf TX schalten
  GPIO.output(DE, GPIO.HIGH)
  GPIO.output(RE, GPIO.HIGH)
  ser.write(b'A')
  ser.flushOutput()
  # RS 485 auf RX schalten
  GPIO.output(RE, GPIO.LOW)
  GPIO.output(DE, GPIO.LOW)
  time.sleep(5) # Wie schnell antwortet der Sensor ????

  rx_anz = ser.inWaiting()
  if rx_anz > 7: # 8 byte rx !
      data = ser.read(rx_anz)
      #for i in data:
        #print(i)

      byte1 = data[0]
      byte2 = data[1]
      byte3 = data[2]
      byte4 = data[3]
      byte5 = data[4]
      byte6 = data[5]
      byte7 = data[6]
      byte8 = data[7]

      temp = ((byte2 << 8 | byte1 ) - 400.0) / 10.0
      print("Temp: {0:.2f} 'C".format(temp))

      baud = byte6 << 24 | byte5 << 16 | byte4 << 8 | byte3
      print("Baudrate: {0:d} ".format(baud))

      abstand = (byte8 << 8 | byte7) / 100.0
      print("Abstand: {0:.2f} mm".format(abstand))
  else:
      print("Fehler: Keine Antwort vom Sensor !")

  GPIO.cleanup()
  ser.close()



###################################################################################################################



