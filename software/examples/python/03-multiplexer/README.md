This example configures the multiplexer.

Any of the 16 inputs `IN_A1`, `IN_A2`, ..., `IN_A8`, `IN_B1`, `IN_B2`, ..., `IN_B8` can be connected
to any of the 2 outputs `OUT_A` and `OUT_B`. It's also possible to keep one or all outputs
disconnected from any input.

# How to run it

## Upload it to the device

```bash
$ DEVICE_IP=192.168.0.14
$ cd ../
$ scp -r 03* pi@${DEVICE_IP}:/home/pi/
```

## Run it over SSH

```bash
$ ssh pi@${DEVICE_IP}
password: raspberry
$ cd 03*
$ ./main.py
Current multiplexer state:
OUT_A is not connected.
OUT_B is not connected.

Setting multiplexer to ['B1', 'A6'] ...
Response: ['B1', 'A6']

New state:
OUT_A is connected to B1.
OUT_B is connected to A6.
```

# How it works

This example performs the following steps:

* Select the SPI slave containing the multiplexer.
* As an SPI master query the multiplexer's initial state.
* As an SPI master switch the multiplexer's connections randomly.
* Query the multiplexer's state again.
