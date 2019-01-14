#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from common import spi


def main():
  input_values = spi.parse_response(spi.query('adc_dac', 'get_analog'))
  print("Current input from ADC:")
  _print_values(input_values, _INPUTS)
  print('')

  output_values = spi.parse_response(spi.query('adc_dac', 'get_digital'))
  print("Current output to DAC:")
  _print_values(output_values, _OUTPUTS)
  print('')

  for i in range(len(output_values)):
    output_values[i] = _random_potential()

  print('Setting output to {} ...'.format(output_values))
  print('Response: {}'.format(spi.parse_response(spi.query('adc_dac', 'set_digital',
                                                           output_values))))
  print('')

  output_values = spi.parse_response(spi.query('adc_dac', 'get_digital'))
  print("New output:")
  _print_values(output_values, _OUTPUTS)


_INPUTS = {
  0: {
    'name': 'V1',
    'unit': 'V',
  },
  1: {
    'name': 'V2',
    'unit': 'V',
  },
  2: {
    'name': 'V3',
    'unit': 'V',
  },
  3: {
    'name': 'V4',
    'unit': 'V',
  },
  4: {
    'name': 'V5',
    'unit': 'V',
  },
  5: {
    'name': 'V6',
    'unit': 'V',
  },
  6: {
    'name': 'V7',
    'unit': 'V',
  },
  7: {
    'name': 'V8',
    'unit': 'V',
  },
  8: {
    'name': 'I1',
    'unit': 'mA',
  },
  9: {
    'name': 'I2',
    'unit': 'mA',
  },
}

_OUTPUTS = {
  0: {
    'name': 'V1',
    'unit': 'V',
  },
  1: {
    'name': 'V2',
    'unit': 'V',
  },
  2: {
    'name': 'V3',
    'unit': 'V',
  },
  3: {
    'name': 'V4',
    'unit': 'V',
  },
}

_MAX_POTENTIAL = 10 # volts

def _print_values(spi_response, descriptors):
  for i in range(len(spi_response)):
    input_descr = descriptors[i]
    print('{} = {}{}'.format(input_descr['name'], spi_response[i], input_descr['unit']))

def _random_potential():
  """Returns a random potential between 0 and 10V as a string that can be understood by the SPI
  slave (4 decimals).
  """
  return "%.4f" % (random.random() * _MAX_POTENTIAL)


if __name__ == '__main__':
  main()
