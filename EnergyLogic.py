from SpeakerManager import textSpeaker


class EnergyLogic:

    def __init__(self, mqttClient):
        self._client = mqttClient
        self._TTS = textSpeaker()

    def logic(self):
        print("solar : " + str(self._client.getPM3()))
        print("boiler of Heating : " + str(self._client.getPM2()))
        self._TTS.say("hello")