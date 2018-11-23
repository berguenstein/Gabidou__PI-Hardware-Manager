from espeak import espeak

class textSpeaker:

    def __init__(self):
        espeak.set_voice("french+f5")
        espeak.set_parameter(espeak.Parameter.Wordgap, 1)
        espeak.set_parameter(espeak.Parameter.Rate, 50)
        espeak.set_parameter(espeak.Parameter.Pitch, 50)

    def say(self, phrase):
        espeak.synth(phrase)
