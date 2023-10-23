from enum import Enum
import simpleaudio as sa


class Son(Enum):
    VICTOIRE = '522243__dzedenz__result-10.wav'
    ERREUR = '409282__wertstahl__syserr1v1-in_thy_face_short.wav'
    FIN_PARTIE = '173859__jivatma07__j1game_over_mono.wav'
    QUESTION = '550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'

    def __init__(self, nom_fichier):
        self.filename = nom_fichier
        self.wave_objet = sa.WaveObject.from_wave_file(nom_fichier)
        self.jouer_sons = None

    def play(self):
        self.jouer_sons = self.wave_objet.play()

    def stop(self):
        if self.jouer_sons:
            self.jouer_sons.stop()
            self.jouer_sons = None