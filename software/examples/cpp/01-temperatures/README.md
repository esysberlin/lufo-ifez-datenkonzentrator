This example queries many times the values of the temperature sensors as fast as possible and prints
statistics.

# How to run it

## Upload it to the device

```bash
$ DEVICE_IP=192.168.0.14
$ cd ../
$ scp -r 01* pi@${DEVICE_IP}:/home/pi/
```

## Build it over SSH

```bash
$ ssh pi@${DEVICE_IP}
password: raspberry
$ cd 01*
$ make
```

## Run it

```bash
$ ./main
It took 792ms to query the temperature sensors 1000 times.
Last response: 0,12,21.02,22.45,19.56,20.67,21.12,21.32,19.54,18.01,14.11,25.58,21.66,21.98*1234
```

# How it works

This example performs the following steps:

* Select the SPI slave containing the temperature sensors.
* Many times: as an SPI master query all temperatures.
