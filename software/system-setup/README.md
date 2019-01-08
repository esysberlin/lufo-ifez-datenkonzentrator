# System Setup

This document describes how to install Linux and various libraries on the Raspberry Pi's SD-card.

## Copy the raspbian image to an SD-card

Download the [Raspbian Stretch Lite](https://downloads.raspberrypi.org/raspbian_lite_latest)
image and unzip it.

Before inserting the SD-card into your computer, in order to determine the block device name of the
SD-card, run

```bash
$ watch -dn1 cat /proc/partitions
```

Now insert the SD-card and you should see such lines popping up

```
179        0   31166976 mmcblk1
179        1      44927 mmcblk1p1
179        2   31117824 mmcblk1p2
```

which means that the SD-card is identified as `/dev/mmcblk1` on your system and this is what we'll
use in the next commands:

```bash
$ sudo umount /dev/mmcblk1*
$ sudo dd if=/tmp/2018-11-13-raspbian-stretch-lite.img of=/dev/mmcblk1
$ sudo sync
```

Remove the SD-card from your computer.

## Make the Raspberry Pi accessible via SSH

Insert the SD-card into the Raspberry Pi and plug:

* an HDMI screen,
* an USB keyboard,
* power over Micro-USB.

Log in (user: `pi`, password: `raspberry`).

### Configure WiFi

In `/etc/wpa_supplicant/wpa_supplicant.conf` write:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
  ssid="myssid"
  psk="mypassword"
}
```

### Enable SSH

```bash
$ sudo systemctl enable ssh
$ sudo systemctl start ssh
```

## Change the hostname

In `/etc/hostname` and `/etc/hosts` replace `raspberrypi` by e.g. `dk-0001` and reboot.

## Enable the SPI driver

In `/boot/config.txt` uncomment

```
dtparam=spi=on
```

and reboot.

## Install dependencies

Our [examples](../examples/) require the following dependencies.

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
