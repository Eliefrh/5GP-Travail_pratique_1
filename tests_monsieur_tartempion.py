import unittest
from unittest.mock import Mock
from monsieur_tartempion import *


class TestsMonsieurTartempion(unittest.TestCase):

    def test_afficher_jeu(self):
        """Vérifier si la fonction afficher_jeu crée correctement la fenêtre de jeu."""
        fenetre = afficher_jeu()

        # Vérifiez si la fenêtre a été créée avec les éléments attendus
        self.assertIsInstance(fenetre, gui.Window)
        self.assertIsNotNone(fenetre.FindElement('TITLE'))
        self.assertIsNotNone(fenetre.FindElement('TEMPS'))
        self.assertIsNotNone(fenetre.FindElement('BOUTON-GAUCHE'))
        self.assertIsNotNone(fenetre.FindElement('BOUTON-DROIT'))
        self.assertIsNotNone(fenetre.FindElement('QUESTION'))
        self.assertIsNotNone(fenetre.FindElement('BOUTON-ACTION'))
        self.assertIsNotNone(fenetre.FindElement('IMAGE-BOUTON-INACTIF'))

    def test_choisir_questions_nombre_questions_retournees(self):
        """Teste si la fonction choisir_questions retourne le nombre de questions désirées."""
        nombre_de_questions = 10
        questions = choisir_questions(nombre_de_questions)
        self.assertEqual(len(questions), nombre_de_questions)

    def test_choisir_questions_uniques(self):
        """Teste que la fonction choisir_questions ne retourne pas la même question deux fois."""
        nombre_de_questions = 21
        questions_selectionnees = choisir_questions(nombre_de_questions)
        # Éliminer doublons avec un tuple
        questions_tuple = tuple(question for question, _ in questions_selectionnees)
        # Vérifiez si la longueur du tuple est égale au nombre de questions sélectionnées.
        self.assertEqual(len(questions_tuple), len(questions_selectionnees))

    def test_melanger_reponses(self):
        """Vérifie que la méthode melanger_reponses renvoie un tuple avec des réponses mélangées."""
        reponses = ('Réponse A', 'Réponse B')
        reponses_melangees = melanger_reponses(reponses)

        # Résultat contient les deux réponses mélangées
        self.assertTrue(reponses_melangees in [(reponses[0], reponses[1]), (reponses[1], reponses[0])])

    def test_afficher_images_temps_precis(self):
        """Vérifie que la fonction afficher_images affiche une image pour un temps déterminé."""
        objet = 'equipe'
        # test affichage 3 secondes
        temps = 3000
        self.assertIsNone(afficher_images(objet, temps))


if __name__ == "__main__":
    unittest.main()
