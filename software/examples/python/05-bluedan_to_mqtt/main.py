#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import re
import sys
import time

from bluepy.btle import Scanner, Peripheral, ADDR_TYPE_RANDOM, BTLEDisconnectError

from common import mqtt

def main(argv):
  if not len(argv) == 2:
    print('Usage: {} <mqtt-token>'.format(argv[0]))
    sys.exit(1)

  mqtt_token = argv[1]

  def send_to_mqtt(mqtt_values):
    """Sends mqtt_values as telemetry over MQTT, see
    https://thingsboard.io/docs/reference/gateway-mqtt-api/#telemetry-upload-api
    """
    mqtt.send_telemetry('bd-clima-{}'.format(bluedan_id), mqtt_values, mqtt_token)

  while True:
    try:
      bluedan_mac_addr, bluedan_id = _discover_bluedan()
      print('Found blueDAN clima device {} / {}'.format(bluedan_mac_addr, bluedan_id))
      _query_bluedan(bluedan_mac_addr, bluedan_id, send_to_mqtt)
    except BTLEDisconnectError:
      print('Connection lost, trying again with any device...')


def _discover_bluedan():
  """Scans for a Bluetooth blueDAN clima and returns a pair of strings (mac_addr, bluedan_id) for
  the first device discovered.
  Raises if no device is found.
  """
  SCAN_DURATION_SEC = 2.0
  DEVICE_NAME_PREFIX = 'BD Clima '

  print('Scanning for blueDAN clima devices...')
  devices = Scanner().scan(SCAN_DURATION_SEC)

  mac_addr = None
  device_name = None
  for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
      if desc == 'Complete Local Name' and value.startswith(DEVICE_NAME_PREFIX):
        mac_addr = dev.addr
        device_name = value
        break
    if mac_addr:
      break

  if not mac_addr:
    raise RuntimeError('No blueDAN clima Bluetooth device found.')

  return (mac_addr, device_name[len(DEVICE_NAME_PREFIX):])

def _query_bluedan(mac_addr, bluedan_id, callback):
  """Connects to the given device and query its data periodically.
  @param callback: function taking exactly one dict as argument which looks like {
                     'humidity': '34.1',
                     'temperature': '22.7',
                   }
  """
  print('Connecting...')
  for i in range(3)[::-1]:
    try:
      server = Peripheral(mac_addr, ADDR_TYPE_RANDOM)
      break
    except BTLEDisconnectError as e:
      if not i:
        raise
      print('{}, trying again...'.format(e))
  print('Connected.')

  while True:
    _request_new_measurements(server, bluedan_id)
    time.sleep(1)
    callback(_read_measurements(server))

def _request_new_measurements(peripheral, bluedan_id):
  """Write Bluetooth command in order to get new measurements.
  @param peripheral: connected instance of Peripheral.
  """
  WRITE_HANDLE = 17
  GET_NEW_MEASUREMENTS_COMMAND_ID = 'B7'

  command = bytes.fromhex(bluedan_id + GET_NEW_MEASUREMENTS_COMMAND_ID)
  command += _crc(command)
  peripheral.writeCharacteristic(WRITE_HANDLE, command)

def _read_measurements(peripheral):
  """Reads Bluetooth characteristic in order to get measurements and returns them as a dict that
  looks like {
    'humidity': '34.1',
    'temperature': '22.7',
  }

  @param peripheral: connected instance of Peripheral.
  """
  READ_HANDLE = 14
  try:
    data = peripheral.readCharacteristic(READ_HANDLE)
  except BrokenPipeError:
    # Might happen on disconnection because of https://github.com/IanHarvey/bluepy/issues/305
    # Just convert to the right exception type:
    raise BTLEDisconnectError('connection lost while reading')

  # data looks like: b'$MWO;37.9\t%;24.8\t\xf8C\n'
  match = re.search(r';(.*)\t.*;(.*)\t', data.decode('ascii', 'ignore'))
  return {
    'humidity': match.group(1),
    'temperature': match.group(2),
  }

def _crc(byte_array):
  """Returns as bytes the CRC-16/XMODEM of the provided bytes.
  """
  return binascii.crc_hqx(byte_array, 0x0000).to_bytes(2, byteorder='big')


if __name__ == '__main__':
  main(sys.argv)
