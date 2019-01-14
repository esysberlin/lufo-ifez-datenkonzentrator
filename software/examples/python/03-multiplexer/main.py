#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from common import spi


def main():
  multiplexer_state = spi.parse_response(spi.query('multiplexer', 'get_outputs'))
  print("Current multiplexer state:")
  _print_state(multiplexer_state)
  print('')

  for i in range(len(multiplexer_state)):
    multiplexer_state[i] = _random_input()

  print('Setting multiplexer to {} ...'.format(multiplexer_state))
  print('Response: {}'.format(spi.parse_response(spi.query('multiplexer', 'set_outputs',
                                                           multiplexer_state))))
  print('')

  multiplexer_state = spi.parse_response(spi.query('multiplexer', 'get_outputs'))
  print("New state:")
  _print_state(multiplexer_state)


_MULTIPLEXER_INPUTS = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                       'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
_MULTIPLEXER_OUTPUTS = ['OUT_A', 'OUT_B']

def _print_state(spi_response):
  def print_output_state(name, state):
    if state == 'NC':
      print('{} is not connected.'.format(name))
    else:
      print('{} is connected to {}.'.format(name, state))

  for i in range(len(spi_response)):
    print_output_state(_MULTIPLEXER_OUTPUTS[i], spi_response[i])

def _random_input():
  return _MULTIPLEXER_INPUTS[int(random.random() * len(_MULTIPLEXER_INPUTS))]


if __name__ == '__main__':
  main()
