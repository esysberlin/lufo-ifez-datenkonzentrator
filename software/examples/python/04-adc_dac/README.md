This example reads the Analog-to-Digital Converter and configures the Digital-to-Analog Converter.

The Analog-to-Digital Converter has 10 inputs:

* 8 potentials `IN_V1`, `IN_V2`, ..., `IN_V8`,
* 2 currents `IN_I1` and `IN_I2`.

The Digital-to-Analog Converter has 4 output potentials `OUT_V1`, `OUT_V2`, `OUT_V3` and `OUT_V4`.

# How to run it

## Upload it to the device

```bash
$ DEVICE_IP=192.168.0.14
$ cd ../
$ scp -r 04* pi@${DEVICE_IP}:/home/pi/
```

## Run it over SSH

```bash
$ ssh pi@${DEVICE_IP}
password: raspberry
$ cd 04*
$ ./main.py
Current input from ADC:
V1 = 0.0459V
V2 = 0.0428V
V3 = 0.0444V
V4 = 0.0447V
V5 = 0.0444V
V6 = 0.0441V
V7 = 0.0422V
V8 = 0.0431V
I1 = 0.0254mA
I2 = 0.0000mA

Current output to DAC:
V1 = 0.0000V
V2 = 0.0000V
V3 = 0.0000V
V4 = 0.0000V

Setting output to ['2.9245', '7.2429', '5.6007', '9.3789'] ...
Response: ['2.9245', '7.2429', '5.6007', '9.3789']

New output:
V1 = 2.9245V
V2 = 7.2429V
V3 = 5.6007V
V4 = 9.3789V
```

# How it works

This example performs the following steps:

* Select the SPI slave containing the converters.
* As an SPI master query the input.
* As an SPI master change the output randomly.
