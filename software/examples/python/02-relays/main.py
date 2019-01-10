#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from common import spi


def main():
  relays_states = spi.parse_response(spi.query('relays', 'get_relays'))
  print("Current relays' states: {}".format(relays_states))

  for i in range(len(relays_states)):
    relays_states[i] = str(round(random.random()))

  print('Setting relays to {} ...'.format(relays_states))
  print('Response: {}'.format(spi.parse_response(spi.query('relays', 'set_relays', relays_states))))

  relays_states = spi.parse_response(spi.query('relays', 'get_relays'))
  print("New states: {}".format(relays_states))


if __name__ == '__main__':
  main()
