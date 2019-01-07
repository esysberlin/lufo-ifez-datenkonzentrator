#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from periphery import GPIO


def main():
  _select_spi_slave('thermo_elements')


_KNOWN_SPI_SLAVES = {
  'adc_dac': {
    'gpio': { # GPIO output to talk to this slave
      20: False,
      21: False,
    },
  },
  'thermo_elements': {
    'gpio': { # GPIO output to talk to this slave
      20: True,
      21: False,
    },
  },
  'multiplexer': {
    'gpio': { # GPIO output to talk to this slave
      20: False,
      21: True,
    },
  },
  'relays': {
    'gpio': { # GPIO output to talk to this slave
      20: True,
      21: True,
    },
  },
}

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
