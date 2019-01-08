# lufo-ifez-datenkonzentrator

The Datenkonzentrator is made of:

* a Raspberry Pi 3, communicating via SPI with
* a board, connected to
* several boards with various sensors.

This repository shows:

* [how to setup the operating system](software/system-setup/) on the Raspberry Pi, and
* [examples](software/examples/) querying the sensor data via
  [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) and publishing them as
  [MQTT](https://en.wikipedia.org/wiki/MQTT) messages.
