# Python examples

## Install dependencies

In order to run these examples you need to install the following dependencies.

### python-periphery

[python-periphery](https://github.com/vsergeev/python-periphery) is a library for GPIO and SPI
communication. Install it with:

```bash
$ sudo apt-get install python3-pip
$ sudo pip3 install python-periphery==1.1.1
```

### The MQTT Python library

The
[MQTT Python library](https://thingsboard.io/docs/samples/raspberry/gpio/#mqtt-library-installation)
is for sending data to a service like [ThingsBoard](https://thingsboard.io/). Install it with:

```bash
$ sudo pip3 install paho-mqtt==1.4.0
```

### bluepy

[bluepy](https://github.com/IanHarvey/bluepy) is a library for Bluetooth Low Energy communication.
Install it with:

```bash
$ sudo apt-get install libglib2.0-dev
$ sudo pip3 install bluepy==1.3.0
```

Allow normal users to discover bluetooth devices with bluepy:

```bash
$ sudo setcap 'cap_net_raw,cap_net_admin+eip' /usr/local/lib/python3.5/dist-packages/bluepy/bluepy-helper
```

> **NOTE**: for more details, see:
>
> * https://unix.stackexchange.com/a/182559/36560
> * https://github.com/IanHarvey/bluepy/issues/218#issuecomment-367242647
