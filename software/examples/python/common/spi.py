#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import errno
import time

from periphery import GPIO, GPIOError, SPI

def query(slave_name, command, args=[]):
  """Selects the given SPI slave, sends it the SPI command and returns the received response as a
  stripped string.
  @param slave_name: _KNOWN_SPI_SLAVES key.
  @param command: _KNOWN_SPI_SLAVES[slave_name]['commands'] key.
  @param args: list of strings to be sent as command arguments.
  """
  _select_spi_slave(slave_name)

  spi = SPI(_SPI_BUS_SETTINGS['dev'], _SPI_BUS_SETTINGS['mode'], _SPI_BUS_SETTINGS['freq_hz'])

  full_command = _KNOWN_SPI_SLAVES[slave_name]['commands'][command]
  if args:
    full_command += ' ' + ','.join(args)
    full_command += '*' + int_to_hex_string(_crc(full_command))
  full_command = (bytes(full_command, 'ascii') + _SPI_MESSAGE_SEPARATOR).ljust(_SPI_COMMAND_LENGTH,
                                                                               b'\x00')

  response = spi.transfer(full_command)
  response = response.split(_SPI_MESSAGE_SEPARATOR)[0]

  spi.close()

  printable_response = ''.join(map(lambda ascii_num: chr(ascii_num),
                                   filter(lambda char: char >= 0x20 and char < 0x7f, response)))
  return printable_response

def parse_response(response):
  """Returns the given SPI response as a list of strings. An SPI response typically looks like
  <error-code>,<num-of-values>,<value-1>,<value-2>,...,<value-n>*<crc>
  e.g.:
  0,3,hello,hi,42*<crc> # 0 means success
  0,0*<crc>
  2,0*<crc> # 2 means unknown command

  Raises if the response isn't a success response.

  @param response: Stripped string. Typically the output of query().
  """
  try:
    response_without_crc, crc = response.split('*')
  except ValueError:
    raise RuntimeError('"{}" has no CRC.'.format(response))
  _check_crc(response_without_crc, crc)

  fields = response_without_crc.split(',')
  response_code = _SPI_RESPONSE_CODES[int(fields[0])]
  if response_code != 'success':
    raise RuntimeError('SPI slave answered "{}".'.format(response_code))

  return fields[2:]


_KNOWN_SPI_SLAVES = {
  'adc_dac': {
    'gpio': { # GPIO output to talk to this slave
      20: False,
      21: False,
    },
    'commands': { # known SPI commands
      'get_analog': 'GA',
      'set_digital': 'SD',
      'get_digital': 'GD',
    },
  },
  'thermo_elements': {
    'gpio': { # GPIO output to talk to this slave
      20: True,
      21: False,
    },
    'commands': { # known SPI commands
      'get_temperatures': 'GT',
    },
  },
  'multiplexer': {
    'gpio': { # GPIO output to talk to this slave
      20: False,
      21: True,
    },
    'commands': { # known SPI commands
      'get_outputs': 'GO',
      'set_outputs': 'SO',
    },
  },
  'relays': {
    'gpio': { # GPIO output to talk to this slave
      20: True,
      21: True,
    },
    'commands': { # known SPI commands
      'get_relays': 'GR',
      'set_relays': 'SR',
    },
  },
}

_SPI_BUS_SETTINGS = {
  'dev':     '/dev/spidev0.0',
  'mode':    1,
  'freq_hz': 3000000,
}

_SPI_COMMAND_LENGTH = 400 # Needs to be long enough so the slave has time to answer
_SPI_MESSAGE_SEPARATOR = b'\r'

_SPI_RESPONSE_CODES = {
  0: 'success',
  1: 'bad CRC',
  2: 'unknown command',
}

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

def _check_crc(received_string, received_crc):
  """Raises if `received_crc` isn't the CRC-16/CCITT-FALSE of `received_string`.
  @param received_crc: received CRC as string, e.g. 'A1B2'.
  """
  expected_crc_int = _crc(received_string)
  received_crc_int = int(received_crc, 16)
  if expected_crc_int != received_crc_int:
    raise RuntimeError("Message '{}' received together with wrong CRC '{}'.".format(
      received_string, received_crc))

def _crc(string):
  """Returns the CRC-16/CCITT-FALSE of `string` as integer.
  """
  return binascii.crc_hqx(bytes(string, 'utf-8'), 0xffff)

def int_to_hex_string(integer):
  """Converts e.g. 255 to 'FF'.
  """
  return hex(integer)[2:].upper().zfill(4)
