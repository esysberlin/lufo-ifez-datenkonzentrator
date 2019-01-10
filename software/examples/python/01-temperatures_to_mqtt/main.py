#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import socket
import sys
import time

import paho.mqtt.client as mqtt

from common import spi

def main(argv):
  if not len(argv) == 2:
    print('Usage: {} <mqtt-token>'.format(argv[0]))
    sys.exit(1)

  mqtt_token = argv[1]

  while True:
    time.sleep(1)
    temperatures = spi.parse_response(spi.query('thermo_elements', 'get_temperatures'))
    mqtt_values = _list_to_mqtt_values(temperatures, 'temperature', 2)
    _send_mqtt_telemetry(mqtt_values, mqtt_token)


_MQTT_SETTINGS = {
  'host': 'data.esys.eu',
  'port': 1883,
}

def _list_to_mqtt_values(values, prefix, num_digits):
  """Transforms a values=['a', 'b', 'c'], prefix='myval', num_digits=4 into a dict
  {
    'myval0000': 'a',
    'myval0001': 'b',
    'myval0002': 'c',
  }
  so it can be sent as telemetry over MQTT, see
  https://thingsboard.io/docs/reference/gateway-mqtt-api/#telemetry-upload-api
  """
  return dict(('temperature{index:0>{width}}'.format(index=i, width=num_digits), values[i])
              for i in range(len(values)))

def _send_mqtt_telemetry(mqtt_values, mqtt_token):
  """@param mqtt_values: values dict. Typically the output of _list_to_mqtt_values().
  """
  print('Sending {} over MQTT...'.format(json.dumps(mqtt_values, sort_keys=True, indent=2)))

  def on_connect(client, userdata, flags, result_code):
    if result_code != mqtt.MQTT_ERR_SUCCESS:
      print('ERROR: Connection returned {}.'.format(result_code))
    else:
      to_be_sent = {
        socket.gethostname(): [{
          'ts': int(time.time() * 1000),
          'values': mqtt_values,
        }],
      }
      result_code = client.publish('v1/gateway/telemetry', json.dumps(to_be_sent)).rc
      if result_code != mqtt.MQTT_ERR_SUCCESS:
        print('ERROR: MQTT publish returned {}.'.format(result_code))

    client.disconnect()

  client = mqtt.Client()
  client.on_connect = on_connect
  client.username_pw_set(mqtt_token)
  client.connect(
    _MQTT_SETTINGS['host'], _MQTT_SETTINGS['port'],
    60 # see https://thingsboard.io/docs/samples/raspberry/gpio/#application-source-code
  )
  client.loop_forever() # will stop on client.disconnect()

  print('')


if __name__ == '__main__':
  main(sys.argv)
