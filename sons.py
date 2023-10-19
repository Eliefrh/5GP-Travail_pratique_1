from enum import Enum
import simpleaudio as sa


class Son(Enum):
    VICTOIRE = '522243__dzedenz__result-10.wav'
    ERREUR = '409282__wertstahl__syserr1v1-in_thy_face_short.wav'
    FIN_PARTIE = '173859__jivatma07__j1game_over_mono.wav'
    QUESTION = '550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'

    def __init__(self, filename):
        self.filename = filename
        self.wave_obj = sa.WaveObject.from_wave_file(filename)
        self.play_obj = None

    def play(self):
        self.play_obj = self.wave_obj.play()

    def stop(self):
        if self.play_obj:
            self.play_obj.stop()
            self.play_obj = None