#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import errno
import json
import socket
import sys
import time

import paho.mqtt.client as mqtt
from periphery import GPIO, GPIOError, SPI

def main(argv):
  if not len(argv) == 2:
    print('Usage: {} <mqtt-token>'.format(argv[0]))
    sys.exit(1)

  mqtt_token = argv[1]

  while True:
    time.sleep(1)
    temperatures = _parse_spi_response(_spi_query('thermo_elements', 'get_temperatures'))
    mqtt_values = _list_to_mqtt_values(temperatures, 'temperature', 2)
    _send_mqtt_telemetry(mqtt_values, mqtt_token)


_KNOWN_SPI_SLAVES = {
  'adc_dac': {
    'gpio': { # GPIO output to talk to this slave
      20: False,
      21: False,
    },
    'commands': { # known SPI commands
    },
  },
  'thermo_elements': {
    'gpio': { # GPIO output to talk to this slave
      20: True,
      21: False,
    },
    'commands': { # known SPI commands
      'get_temperatures': {
        'command': b'GT\r',
        'longest_response_bytes': 160,
      },
    },
  },
  'multiplexer': {
    'gpio': { # GPIO output to talk to this slave
      20: False,
      21: True,
    },
    'commands': { # known SPI commands
    },
  },
  'relays': {
    'gpio': { # GPIO output to talk to this slave
      20: True,
      21: True,
    },
    'commands': { # known SPI commands
    },
  },
}

_SPI_BUS_SETTINGS = {
  'dev':     '/dev/spidev0.0',
  'mode':    1,
  'freq_hz': 3000000,
}

_MQTT_SETTINGS = {
  'host': 'data.esys.eu',
  'port': 1883,
}

def _spi_query(slave_name, command):
  """Selects the given SPI slave, sends it the SPI command and returns the received response as a
  stripped string.
  @param slave_name: _KNOWN_SPI_SLAVES key.
  @param command: _KNOWN_SPI_SLAVES[slave_name]['commands'] key.
  """
  _select_spi_slave(slave_name)

  spi = SPI(_SPI_BUS_SETTINGS['dev'], _SPI_BUS_SETTINGS['mode'], _SPI_BUS_SETTINGS['freq_hz'])
  command_obj = _KNOWN_SPI_SLAVES[slave_name]['commands'][command]
  full_command = command_obj['command'].ljust(command_obj['longest_response_bytes'], b'\xff')
  response = spi.transfer(full_command)
  spi.close()

  printable_chars = ''.join(map(lambda ascii_num: chr(ascii_num),
                                filter(lambda char: char >= 0x20 and char < 0x7f, response)))
  return printable_chars

def _select_spi_slave(name):
  """Sets GPIO output in order to be able to speak with that SPI slave later.
  @param name: _KNOWN_SPI_SLAVES key.
  """
  for pin, output_value in _KNOWN_SPI_SLAVES[name]['gpio'].items():
    for attempt in [1, 0]:
      try:
        gpio_out = GPIO(pin, 'out')
      except GPIOError as e:
        if not attempt or e.errno != errno.EACCES:
          raise
        print('Warning, opening GPIO pin failed, retrying...')
        time.sleep(.5)

    gpio_out.write(output_value)
    gpio_out.close()

def _parse_spi_response(response):
  """Returns the given SPI response as a list of strings. An SPI response typically looks like
  <error-code>,<num-of-values>,<value-1>,<value-2>,...,<value-n>*<crc>
  e.g.:
  0,3,hello,hi,42*<crc> # 0 means success
  0,0*<crc>
  2,0*<crc> # 2 means unknown command

  @param response: Stripped string. Typically the output of _spi_query().
  """
  response_without_crc, crc = response.split('*')
  _check_crc(response_without_crc, crc)
  return response_without_crc.split(',')[2:]

def _check_crc(string, crc):
  """Raises if `crc` isn't the CRC-16/CCITT-FALSE of `string`.
  @param crc: received CRC as string, e.g. 'A1B2'.
  """
  string_crc_int = binascii.crc_hqx(bytes(string, 'utf-8'), 0xffff)
  crc_int = int(crc, 16)
  if string_crc_int != crc_int:
    raise RuntimeError("Message '{}' received together with wrong CRC '{}'.".format(string, crc))

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
