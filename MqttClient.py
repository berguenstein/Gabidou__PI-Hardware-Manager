# -*- coding: utf-8 -*-

import json
import logging
import os
import ssl
import sys
import time

import paho.mqtt.client as mqtt
from cloudio.mqtt_helpers import MqttConnectOptions, MqttReconnectClient
from utils import datetime_helpers
from utils import path_helpers

logging.getLogger(__name__).setLevel(logging.INFO)


class MqttClient:

    MQTT_ERR_SUCCESS = mqtt.MQTT_ERR_SUCCESS

    log = logging.getLogger(__name__)

    def __init__(self, configFile):
        self._isConnected = False
        self._useReconnectClient = False             # Chooses the MQTT client / change by myself
        config = self.parseConfigFile(configFile)

        '''client variables'''
        self._qos = int(config['cloudio']['qos'])
        self._endPointName = config['endpoint']['name']
        self._nodeName = config['node']['name']
        self._certificate = config['cloudio']['certificate']    #add by myself
        self._userName = config['cloudio']['username']
        self._password = config['cloudio']['password']
        self._host = config['cloudio']['host']
        self._port = int(config['cloudio']['port'])
        self._subscribe = config['cloudio']['subscribe_topics']
        self.log.info('Starting MQTT client...')

        if not self._useReconnectClient:
            self._client = mqtt.Client()
            self._client.on_connect = self.onConnect
            self._client.on_disconnect = self.onDisconnect
            self._client.on_message = self.onMessage
            self._client.on_subscribe = self.onSubscibe

            self._client.username_pw_set(self._userName, self._password)
            self._client.tls_set(ca_certs=self._certificate, tls_version=ssl.PROTOCOL_TLSv1_2)           #add by myself
            self._client.tls_insecure_set(True)
            self._clientId = self._client.connect(self._host, port=self._port, keepalive=60)
            self._client.loop_start()
        else:
            self.connectOptions = MqttConnectOptions()

            self.connectOptions._username = config['cloudio']['username']
            self.connectOptions._password = config['cloudio']['password']
            self.connectOptions._clientCertFile = config['cloudio']['certificate']      #add by myself
            self._client = MqttReconnectClient(config['cloudio']['host'],
                                               clientId=self._endPointName + '-client-',
                                               clean_session=False,
                                               options=self.connectOptions)

            # Register callback method for connection established
            self._client.setOnConnectedCallback(self.onConnected)
            # Register callback method to be called when receiving a message over MQTT
            self._client.setOnMessageCallback(self.onMessage)

            self._client.start()

    def connect(self, host, port=1883, keepalive=60, bind_address=""):
        """Connect to a remote broker.

        host is the hostname or IP address of the remote broker.
        port is the network port of the server host to connect to. Defaults to
        1883. Note that the default port for MQTT over SSL/TLS is 8883 so if you
        are using tls_set() the port may need providing.
        keepalive: Maximum period in seconds between communications with the
        broker. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        """
        self.connect_async(host, port, keepalive, bind_address)
        return self.reconnect()

    def close(self):
        if not self._useReconnectClient:
            self._client.disconnect()
        else:
            self._client.stop()

    def parseConfigFile(self, configFile):
        global config

        from configobj import ConfigObj

        config = None

        pathConfigFile = path_helpers.prettify(configFile)

        if pathConfigFile and os.path.isfile(pathConfigFile):
            config = ConfigObj(pathConfigFile)

        if config:
            # Check if most important configuration parameters are present
            assert 'cloudio' in config, 'Missing group \'cloudio\' in config file!'
            assert 'endpoint' in config, 'Missing group \'endpoint\' in config file!'
            assert 'node' in config, 'Missing group \'node\' in config file!'

            assert 'host' in config['cloudio'], 'Missing \'host\' parameter in cloudio group!'
            assert 'port' in config['cloudio'], 'Missing \'port\' parameter in cloudio group!'
            assert 'username' in config['cloudio'], 'Missing \'username\' parameter in cloudio group!'
            assert 'password' in config['cloudio'], 'Missing \'password\' parameter in cloudio group!'
            assert 'subscribe_topics' in config['cloudio'], 'Missing \'subscribe_topics\' parameter in cloudio group!'
            assert 'qos' in config['cloudio'], 'Missing \'qos\' parameter in cloudio group!'

            assert 'name' in config['endpoint'], 'Missing \'name\' parameter in endpoint group!'

            assert 'name' in config['node'], 'Missing \'name\' parameter in node group!'
        else:
            sys.exit(u'Error reading config file')

        return config

    def waitTilConnected(self):
        while True:
            time.sleep(0.2)

    def isConnected(self):
        return self._isConnected

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            self._isConnected = True
            print("hello I'm connected")
            self._subscribeToUpdatedCommands()


    def onConnected(self):
        self._isConnected = True
        self._subscribeToUpdatedCommands()

    def onDisconnect(self, client, userdata, rc):
        self.log.info('Disconnect: ' + str(rc))
        print("goodbye I'm disconnected")


    def onMessage(self, client, userdata, msg):
        #I think i must do something here
        print(msg.topic)
        print(str(msg.payload))
        value = json.loads(msg.payload)['value']
        print(value)

    def onSubscibe(client, userdata, mid):
        print('hello')

    def _subscribeToUpdatedCommands(self):
        print("subscribe to : " + self._endPointName)
        (result, mid) = self._client.subscribe(u'@update/' + self._endPointName + '/#', 1)
        return True if result == self.MQTT_ERR_SUCCESS else False


