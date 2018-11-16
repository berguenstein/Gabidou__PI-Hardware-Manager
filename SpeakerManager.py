from espeak import espeak

from espeakng import ESpeakNG

#esng = ESpeakNG()
#esng.say('Hello World!')

while True:
    phrase = raw_input("What do you want to say?")
    espeak.synth(phrase)