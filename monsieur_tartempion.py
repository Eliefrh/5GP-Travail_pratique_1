"""
Monsieur Tartempion - Édition horrifique
420-5GP-BB, automne 2023, Collège Bois-de-Boulogne
Travail pratique 1

Ressources sous licences:
  522243__dzedenz__result-10.wav
  par DZeDeNZ, 2020-07-15
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  409282__wertstahl__syserr1v1-in_thy_face_short.wav
  par wertstahl, 2017-11-06
  Licence: https://creativecommons.org/licenses/by-nc/4.0/

  173859__jivatma07__j1game_over_mono.wav
  par jivatma07, 2013-01-11
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav
  par Erokia, 2020-12-26
  Licence: https://creativecommons.org/licenses/by-nc/4.0/
"""
import pickle
import random
import time
import sqlite3 as squirrel
from typing import  Any

import PySimpleGUI as gui
from images import *
from indicateurs import Indicateur
from sons import Son

NB_QUESTIONS = 21
TEMPS_EPREUVE = 60
TITRE = 'Monsieur Tartempion'
type_font = gui.DEFAULT_FONT
police_titre = (type_font, 40, 'italic')
police_etiquettes = (type_font, 20, 'normal')
police_temps = (type_font, 50, 'normal')
police_question = (type_font, 30, 'normal')
police_reponses = (type_font, 20, 'normal')
police_choix = (type_font, 20, 'italic')

ordre_affichage = []
premier_affichage_question = True

"""Crée un fichier pickle contenant les images encodées en base64."""
images_base64 = {
    "equipe": equipe_base64(),
    "echec": echec_base64(),
    "succes": succes_base64(),
    "titre": titre_base64()
}

with open('images.pickle', 'wb') as fichier_pickle:
    pickle.dump(images_base64, fichier_pickle)


def charger_images_de_pickle():
    """Charge les images depuis le fichier pickle."""
    with open('images.pickle', 'rb') as fichier_pickle:
        images_base64 = pickle.load(fichier_pickle)
    return images_base64


def afficher_images(objet: str, temps: int) -> None:
    """Affiche une fenêtre avec une image en fonction de l'objet donné.

    param objet: Une chaîne de caractères représentant l'objet.
    param temps: Le temps d'affichage de la fenêtre en millisecondes.
    """
    images_base64 = charger_images_de_pickle()

    match objet:
        case 'equipe':
            gui.Window("Titre", [[gui.Image(data=images_base64["equipe"])]],
                       transparent_color="maroon2", no_titlebar=True,
                       keep_on_top=True).read(timeout=temps, close=True)
        case 'titre':
            gui.Window("Titre", [[gui.Image(data=images_base64["titre"])]],
                       transparent_color="maroon2", no_titlebar=True,
                       keep_on_top=True).read(timeout=temps, close=True)
        case 'echec':
            gui.Window("Titre", [[gui.Image(data=images_base64["echec"])]],
                       transparent_color="maroon2", no_titlebar=True,
                       keep_on_top=True).read(timeout=temps, close=True)
        case 'succes':
            gui.Window("Titre", [[gui.Image(data=images_base64["succes"])]],
                       transparent_color="maroon2", no_titlebar=True,
                       keep_on_top=True).read(timeout=temps, close=True)


def afficher_jeu():
    gui.theme('Black')

    message_label = [gui.Text('', key='MESSAGE', font=police_etiquettes, text_color='red', size=(30, 1))]

    bouton_changer_question = gui.Button('Changer Question', key='CHANGER_QUESTION', font=(type_font, 18,
                                                                                           'normal'),
                                         button_color=('white', 'blue'),
                                         border_width=0, disabled=True, visible=True)

    espace_droit = gui.Column([[gui.Text('', key='', size=(125, 1)),
                                bouton_changer_question]], element_justification='center')

    titre = [gui.Text(TITRE, key='TITLE', font=police_titre)]

    temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')],
             [gui.Text(str(60), key='TEMPS', font=police_temps)]]

    boutons_reponse = [gui.Column([
        [gui.Button(key='BOUTON-GAUCHE', font=police_reponses,
                    button_color=('white', gui.theme_background_color()),
                    border_width=0, disabled=True, visible=True),

         gui.Text(' ou ', key='OU', font=police_choix,
                  text_color=gui.theme_background_color()),

         gui.Button(key='BOUTON-DROIT', font=police_reponses,
                    button_color=('white', gui.theme_background_color()),
                    border_width=0, disabled=True, visible=True)]],
        element_justification='center')]

    question = [gui.Text(' ', key='QUESTION', font=police_question)]

    action = [gui.Button(image_data=bouton_jouer_base64(), key='BOUTON-ACTION', border_width=0,
                         button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
              gui.Image(data=bouton_inactif_base64(), key='IMAGE-BOUTON-INACTIF', visible=False, pad=(0, 10))]

    indicateurs = \
        [gui.Image(data=indicateur_vide_base64(), key=f'INDICATEUR-{i}', pad=(4, 10)) for i in range(NB_QUESTIONS)]

    layout = [
        titre,
        temps,
        boutons_reponse,
        question,
        action,
        indicateurs,
        message_label,
        [espace_droit]
    ]

    fenetre = gui.Window(TITRE, layout, keep_on_top=True,
                         element_padding=(0, 0), element_justification='center', resizable=False, finalize=True)
    return fenetre


def charger_questions(fichier_db: str) -> list:
    try:
        connexion = squirrel.connect(fichier_db)

        with connexion:
            resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')

        toutes_questions = [(enregistrement[0], enregistrement[1], enregistrement[2])
                            for enregistrement in resultat_requete]

        return toutes_questions
    finally:
        if connexion:
            connexion.close()


def choisir_questions(nombre_de_questions: int) -> list:
    toutes_les_questions = charger_questions("questions.bd")

    random.shuffle(toutes_les_questions)

    questions_selectionnees = []
    for i in range(min(nombre_de_questions, len(toutes_les_questions))):
        questions_selectionnees.append([toutes_les_questions[i], Indicateur.VIDE])

    question_changement = []
    if len(toutes_les_questions) > nombre_de_questions:
        question_changement = [[toutes_les_questions[nombre_de_questions], Indicateur.VIDE]]

    return questions_selectionnees, question_changement


def melanger_reponses(reponses: tuple) -> tuple:
    """On fait une verification si la question est posée pour la premiere fois
     - on verifie cela par la boolean premiere fois et le numero de la question
     - on stock l'ordre des reponses a partir de leur boolean dans une liste
     - on revient chercher la position dans la liste si ce nest pas la premiere fois pour cette question"""

    # if (numero_question + 1 > len(ordre_affichage)):
    #     premier_affichage_question = True
    # if (premier_affichage_question):
    #     ordre = bool(random.getrandbits(1))
    #
    #     ordre_affichage.append(ordre)
    #     return (reponses[0], reponses[1]) if ordre else (reponses[1], reponses[0])
    # else:
    #     if (ordre_affichage[numero_question] == True):
    #         return (reponses[0], reponses[1])
    #     else:
    #         return (reponses[1], reponses[0])
    return reponses[0], reponses[1]


# Duplication élliminée
def mettre_a_jour_widgets(fenetre: gui.Window, reponses: tuple, bouton_est_actif: bool, couleur_text: str) -> None:
    fenetre['BOUTON-GAUCHE'].update(reponses[0], disabled=bouton_est_actif, visible=True)
    fenetre['OU'].update(text_color=couleur_text)
    fenetre['BOUTON-DROIT'].update(reponses[1], disabled=bouton_est_actif, visible=True)


def afficher(fenetre: gui.Window, question: tuple) -> None:
    fenetre['QUESTION'].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    # reponses = question[1], question[2]
    mettre_a_jour_widgets(fenetre, reponses, False, 'white')


def effacer_question(fenetre: gui.Window) -> None:
    fenetre['QUESTION'].update('')
    mettre_a_jour_widgets(fenetre, ('', '', ''), True, gui.theme_background_color())


def reinitialiser_jeu(fenetre) -> tuple[list[Any], int, bool, bool, int, list[Any], bool, int]:
    reinitialiser_bouton_action(fenetre, False)
    temps_restant = TEMPS_EPREUVE
    fenetre['TEMPS'].update(str(temps_restant))
    fenetre['CHANGER_QUESTION'].update(disabled=True)
    fenetre.un_hide()
    for i in range(NB_QUESTIONS):
        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())

    # questions, question_changee = choisir_questions(NB_QUESTIONS)
    questions = ([])
    question_changee = ([])
    prochaine_question = 0
    compteur = 0
    question_changee_succes = False
    premier_affichage_question = True
    decompte_actif = False
    return (questions, prochaine_question, question_changee_succes,
            premier_affichage_question, compteur, question_changee, decompte_actif, temps_restant)


def reinitialiser_bouton_action(fenetre, activation_bouton: bool) -> None:
    fenetre['BOUTON-ACTION'].update(disabled=activation_bouton, visible=not activation_bouton)
    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=activation_bouton)


def changer_question(compteur: int, prochaine_question: int, questions: tuple,
                     question_changee: tuple, fenetre: gui.Window) -> bool:
    if compteur == prochaine_question:
        questions.pop(prochaine_question)
        questions.append(question_changee[0])
        afficher(fenetre, questions[prochaine_question][0])
        fenetre['CHANGER_QUESTION'].update(disabled=True)
        fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_vide_base64())
        question_changee_succes = True

        return question_changee_succes

    else:
        fenetre['MESSAGE'].update("Vous avez déjà réussi cette question!")
        question_changee_succes = False
        return question_changee_succes


def bouton_action(fenetre, premier_affichage_question, prochaine_question, question_changee_succes, questions,
                  temps_restant, question_changee):
    if temps_restant != 60:
        premier_affichage_question = False

    if temps_restant == 60:
        prochaine_question = 0
        questions, question_changee = choisir_questions(NB_QUESTIONS)
        fenetre['CHANGER_QUESTION'].update(disabled=False)
        question_changee_succes = False

    if not question_changee_succes:
        fenetre['CHANGER_QUESTION'].update(disabled=False)
    reinitialiser_bouton_action(fenetre, True)
    temps_actuel = round(time.time())
    decompte_actif = True
    afficher(fenetre, questions[prochaine_question][0])
    Son.QUESTION.play()

    return decompte_actif, premier_affichage_question, temps_actuel, questions, question_changee, prochaine_question


def bonne_reponse(fenetre, prochaine_question, questions, compteur, premier_affichage_question,
                  question_changee, decompte_actif, temps_restant, question_changee_succes):
    fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_vert_base64())
    fenetre['MESSAGE'].update("")

    questions[prochaine_question][1] = Indicateur.VERT
    if prochaine_question == compteur:
        compteur += 1

    prochaine_question += 1

    if prochaine_question < NB_QUESTIONS:
        afficher(fenetre, questions[prochaine_question][0])
    elif NB_QUESTIONS <= prochaine_question:

        fenetre.hide()
        effacer_question(fenetre)
        for i in range(NB_QUESTIONS):
            fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
            questions[i][1] = Indicateur.VIDE
        Son.QUESTION.stop()
        Son.VICTOIRE.play()

        afficher_images('succes', 3000)
        (questions, prochaine_question, question_changee_succes,
         premier_affichage_question, compteur, question_changee, decompte_actif, temps_restant) = reinitialiser_jeu(
            fenetre)
        prochaine_question = 0
        compteur = 0
        questions = ([])
        question_changee_succes = False

    return (prochaine_question, questions, compteur, premier_affichage_question, question_changee,
            decompte_actif, temps_restant, question_changee_succes)


def mauvaise_reponse(fenetre, prochaine_question, questions):
    decompte_actif = False
    effacer_question(fenetre)
    fenetre['CHANGER_QUESTION'].update(disabled=True)
    fenetre['MESSAGE'].update("")
    for i in range(prochaine_question):
        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_jaune_base64())
        questions[i][1] = Indicateur.JAUNE
    if questions[prochaine_question][1] != Indicateur.JAUNE:
        fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_rouge_base64())
        questions[prochaine_question][1] = Indicateur.ROUGE
    prochaine_question = 0
    reinitialiser_bouton_action(fenetre, False)
    Son.ERREUR.play()
    Son.QUESTION.stop()

    return decompte_actif, prochaine_question


def gerer_fermeture_fenetre():
    decompte_actif = False
    quitter = True
    return decompte_actif, quitter


def gestion_temps(temps_actuel, temps_restant, prochaine_question, decompte_actif, fenetre, question_changee_succes):
    dernier_temps = temps_actuel
    temps_actuel = round(time.time())

    if dernier_temps != temps_actuel:
        temps_restant -= 1
        fenetre['TEMPS'].update(str(temps_restant))

        if temps_restant == 0:
            fenetre.hide()
            effacer_question(fenetre)
            Son.FIN_PARTIE.play()
            Son.QUESTION.stop()

            afficher_images('echec', 3000)

            (questions, prochaine_question, question_changee_succes,
             premier_affichage_question, compteur, question_changee, decompte_actif, temps_restant) = reinitialiser_jeu(
                fenetre)
            question_changee_succes = False

    return temps_actuel, temps_restant, prochaine_question, decompte_actif, question_changee_succes


def programme_principal() -> None:
    temps_restant = 60
    prochaine_question = 0
    compteur = 0
    decompte_actif = False
    temps_actuel = round(time.time())
    question_changee_succes = False

    # Appel des fonctions
    afficher_images('equipe', 1500)
    afficher_images('titre', 2000)
    questions, question_changee = choisir_questions(NB_QUESTIONS)
    fenetre = afficher_jeu()
    premier_affichage_question = True
    quitter = False

    while not quitter:
        event, valeurs = fenetre.read(timeout=10)

        if decompte_actif:
            temps_actuel, temps_restant, prochaine_question, decompte_actif, question_changee_succes = (
                gestion_temps(temps_actuel, temps_restant, prochaine_question, decompte_actif,
                              fenetre, question_changee_succes))

        if event == 'CHANGER_QUESTION':
            question_changee_succes = changer_question(compteur, prochaine_question,
                                                       questions, question_changee, fenetre)

        elif event == 'BOUTON-ACTION':
            (decompte_actif, premier_affichage_question, temps_actuel, questions, question_changee,
             prochaine_question) = (bouton_action(fenetre, premier_affichage_question,
                                                  prochaine_question, question_changee_succes, questions, temps_restant,
                                                  question_changee))

        elif event == 'BOUTON-GAUCHE' or event == 'BOUTON-DROIT':
            if (event == 'BOUTON-GAUCHE' and fenetre['BOUTON-GAUCHE'].get_text() != questions[prochaine_question][0][
                1]) or \
                    (event == 'BOUTON-DROIT' and fenetre['BOUTON-DROIT'].get_text() != questions[prochaine_question][0][
                        1]):

                # le joueur a choisi la bonne réponse
                (prochaine_question, questions, compteur, premier_affichage_question, question_changee,
                 decompte_actif, temps_restant, question_changee_succes) = bonne_reponse(fenetre, prochaine_question,
                                                                                         questions, compteur,
                                                                                         premier_affichage_question,
                                                                                         question_changee,
                                                                                         decompte_actif, temps_restant,
                                                                                         question_changee_succes)
                continue
            else:
                # le joueur a choisi la mauvais réponse
                decompte_actif, prochaine_question = mauvaise_reponse(fenetre, prochaine_question,
                                                                      questions)

        elif event == gui.WIN_CLOSED:
            decompte_actif, quitter = gerer_fermeture_fenetre()

    fenetre.close()
    del fenetre


if __name__ == '__main__':
    try:
        programme_principal()
    except KeyboardInterrupt:
        print("Le programme a été arrêté par l'utilisateur.")
