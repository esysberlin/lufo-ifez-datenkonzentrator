#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import time

from common import mqtt, spi

def main(argv):
  if not len(argv) == 2:
    print('Usage: {} <mqtt-token>'.format(argv[0]))
    sys.exit(1)

  mqtt_token = argv[1]

  while True:
    time.sleep(1)
    temperatures = spi.parse_response(spi.query('thermo_elements', 'get_temperatures'))
    mqtt_values = _list_to_mqtt_values(temperatures, 'temperature', 2)
    mqtt.send_telemetry(socket.gethostname(), mqtt_values, mqtt_token)


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


if __name__ == '__main__':
  main(sys.argv)
