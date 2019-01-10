This example switches relays on and off.

# How to run it

## Upload it to the device

```bash
$ DEVICE_IP=192.168.0.14
$ cd ../
$ scp -r 02* pi@${DEVICE_IP}:/home/pi/
```

## Run it over SSH

```bash
$ ssh pi@${DEVICE_IP}
password: raspberry
$ cd 02*
$ ./main.py
Current relays' states: ['1', '1', '1', '0', '1', '0', '1', '1']
Setting relays to ['1', '0', '0', '1', '1', '1', '0', '0'] ...
Response: ['1', '0', '0', '1', '1', '1', '0', '0']
New states: ['1', '0', '0', '1', '1', '1', '0', '0']
```

# How it works

This example performs the following steps:

* Select the SPI slave containing the relays.
* As an SPI master query the relays' initial states.
* As an SPI master switch the relays randomly.
* Query the relays' states again.
