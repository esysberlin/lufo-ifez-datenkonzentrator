#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from periphery import GPIO, SPI


def main():
  print(_spi_query('thermo_elements', 'get_temperatures'))


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

def _spi_query(slave_name, command):
  """Selects the given SPI slave, sends it the SPI command `command_str` and returns the received
  response as a stripped string.
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
    gpio_out = GPIO(pin, 'out')
    gpio_out.write(output_value)
    gpio_out.close()


if __name__ == '__main__':
  main()
