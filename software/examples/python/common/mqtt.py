#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

import paho.mqtt.client as mqtt

def send_telemetry(mqtt_device_hostname, mqtt_values, mqtt_token):
  """@param mqtt_values: values dict to be sent as telemetry over MQTT, see
  https://thingsboard.io/docs/reference/gateway-mqtt-api/#telemetry-upload-api
  """
  print('Sending {} over MQTT...'.format(json.dumps(mqtt_values, sort_keys=True, indent=2)))

  def on_connect(client, userdata, flags, result_code):
    if result_code != mqtt.MQTT_ERR_SUCCESS:
      print('ERROR: Connection returned {}.'.format(result_code))
    else:
      to_be_sent = {
        mqtt_device_hostname: [{
          'ts': int(time.time() * 1000),
          'values': mqtt_values,
        }],
      }
      result_code = client.publish('v1/gateway/telemetry', json.dumps(to_be_sent)).rc
      if result_code != mqtt.MQTT_ERR_SUCCESS:
        print('ERROR: MQTT publish returned {}.'.format(result_code))

    client.disconnect()

  client = mqtt.Client()
  client.on_connect = on_connect
  client.username_pw_set(mqtt_token)
  client.connect(
    _MQTT_SETTINGS['host'], _MQTT_SETTINGS['port'],
    60 # see https://thingsboard.io/docs/samples/raspberry/gpio/#application-source-code
  )
  client.loop_forever() # will stop on client.disconnect()

  print('')


_MQTT_SETTINGS = {
  'host': 'data.esys.eu',
  'port': 1883,
}
