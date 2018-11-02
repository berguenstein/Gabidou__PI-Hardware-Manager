from MqttClient import MqttClient

houseClient = MqttClient("HouseClientConf.config")
houseClient.waitTilConnected()

