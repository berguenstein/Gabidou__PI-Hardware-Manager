from SpeakerManager import textSpeaker

useTTS = textSpeaker()

while True:
    useTTS.say(raw_input("ecris qqch"))