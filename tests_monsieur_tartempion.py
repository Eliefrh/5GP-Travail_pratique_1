import unittest
from monsieur_tartempion import *


class TestsMonsieurTartempion(unittest.TestCase):

    def test_afficher_jeu(self):
        """Vérifier si la fonction afficher_jeu crée correctement la fenêtre de jeu."""
        fenetre = afficher_jeu()

        # Vérifiez si la fenêtre a été créée avec les éléments attendus
        self.assertIsInstance(fenetre, gui.Window)
        self.assertIsNotNone(fenetre.find_element('TITLE'))
        self.assertIsNotNone(fenetre.find_element('MESSAGE'))
        self.assertIsNotNone(fenetre.find_element('CHANGER_QUESTION'))
        self.assertIsNotNone(fenetre.find_element('TEMPS'))
        self.assertIsNotNone(fenetre.find_element('BOUTON-GAUCHE'))
        self.assertIsNotNone(fenetre.find_element('BOUTON-DROIT'))
        self.assertIsNotNone(fenetre.find_element('QUESTION'))
        self.assertIsNotNone(fenetre.find_element('BOUTON-ACTION'))
        self.assertIsNotNone(fenetre.find_element('IMAGE-BOUTON-INACTIF'))

    def test_choisir_questions_nombre_questions_retournees(self):
        """Teste si la fonction choisir_questions retourne le nombre de questions désirées."""
        nombre_de_questions = 10
        questions, _ = choisir_questions(nombre_de_questions)
        self.assertEqual(len(questions), nombre_de_questions)

    def test_choisir_questions_uniques(self):
        """Teste que la fonction choisir_questions ne retourne pas la même question deux fois."""
        nombre_de_questions = 21
        questions_selectionnees, _ = choisir_questions(nombre_de_questions)

        # Éliminer doublons avec un tuple , car une tuple n'accepte pas les doublons
        questions_tuple = tuple(question for question, _ in questions_selectionnees)

        # Vérifiez si la longueur du tuple est égale au nombre de questions sélectionnées.
        self.assertEqual(len(questions_tuple), len(questions_selectionnees))

    def test_melanger_reponses(self):
        """Vérifie que la méthode melanger_reponses renvoie un tuple avec des réponses mélangées."""
        reponses = ('Réponse A', 'Réponse B')
        reponses_melangees = melanger_reponses(reponses,premier_affichage_question,0)

        # Résultat contient les deux réponses mélangées
        self.assertTrue(reponses_melangees in [(reponses[0], reponses[1]), (reponses[1], reponses[0])])

    def test_afficher_images_temps_precis(self):
        """Vérifie que la fonction afficher_images affiche une image pour un temps déterminé."""
        objet = 'equipe'
        # test affichage 3 secondes
        temps = 3000
        self.assertIsNone(afficher_images(objet, temps))

    def test_changer_question(self):
        """Vérifie que la fonction change la question affichée par une autre question"""
        compteur = 1
        prochaine_question = 1
        questions, question_changement = choisir_questions(21)
        fenetre = afficher_jeu()

        changement_reussit = changer_question(compteur, prochaine_question, questions,
                                              question_changement, fenetre,premier_affichage_question)

        self.assertTrue(changement_reussit)

    def test_indicateur_jaune(self):
        """S'assurer que si la question etait bien réussi (indicateur jaune), l'indicateur restera jaune apres avoir
        mal repondu la meme question dans une autre essaie """

        fenetre = afficher_jeu()
        prochaine_question = 0
        questions, _ = choisir_questions(21)
        questions[prochaine_question][1] = Indicateur.JAUNE
        mauvaise_reponse(fenetre, prochaine_question, questions)

        self.assertEqual(questions[0][1], Indicateur.JAUNE)

    def test_ajout_nouvelle_question(self):
        """Vérifier que la fontion changer_question() me retournee un bool qui me dit que la question a été
        bien modifiée"""

        compteur = 0
        prochaine_question = 0
        fenetre = afficher_jeu()
        questions, question_changement = choisir_questions(21)
        nouvelles_questions_ajoutee = changer_question(compteur, prochaine_question,
                                                       questions, question_changement, fenetre,premier_affichage_question)

        self.assertTrue(nouvelles_questions_ajoutee)

    def test_mauvaise_reponse_indicateur_rouge(self):
        """Teste si la fonction mauvaise_reponse modifie correctement l'indicateur."""
        fenetre = afficher_jeu()
        prochaine_question = 0
        questions, _ = choisir_questions(21)
        mauvaise_reponse(fenetre, prochaine_question, questions)
        self.assertEqual(questions[0][1], Indicateur.ROUGE)

    def test_bonne_reponse_indicateur_vert(self):
        """Teste si la fonction bonne_reponse modifie correctement l'indicateur."""
        compteur = 0
        decompte_actif = True
        fenetre = afficher_jeu()
        prochaine_question = 0
        question_changee = False
        temps_restant = 40
        questions, _ = choisir_questions(21)
        question_changee_succes = False
        premier_affichage_question = True
        (_, questions, _, _, _, _, _, _) = bonne_reponse(fenetre, prochaine_question, questions,
                                                         compteur, premier_affichage_question, question_changee,
                                                         decompte_actif, temps_restant, question_changee_succes
                                                         )

        self.assertEqual(questions[0][1], Indicateur.VERT)

    def test_bouton_action(self):
        """Vérifie que la fonction bouton_action gère correctement le décompte."""
        fenetre = afficher_jeu()
        premier_affichage_question = True
        prochaine_question = 0
        questions, question_changee = choisir_questions(NB_QUESTIONS)
        temps_restant = 60
        question_changee_succes = False
        decompte_actif, _, _, _, _, _ = \
            bouton_action(fenetre, premier_affichage_question, prochaine_question, question_changee_succes, questions,
                          temps_restant, question_changee)

        # Le décompte doit s'activer
        self.assertTrue(decompte_actif)

    def test_initialiser_temps(self):
        """Vérifier la réinitialisation du temps à chaque nouvelle partie"""
        fenetre = afficher_jeu()
        temps = 60
        _, _, _, _, _, _, _, temps_restant = reinitialiser_jeu(fenetre)

        # le temps_restant doit etre egale a temps=60
        self.assertEqual(temps, temps_restant)


if __name__ == "__main__":
    unittest.main()
