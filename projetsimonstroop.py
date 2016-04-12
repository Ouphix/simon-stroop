# -*- encoding: utf-8 -*-
# recruter 10 sujets

# générateur de liste pour chaque tache pour eviter essai[0] sui n'est pas transparent en créant dictionnaire

import pygame, sys
from pygame.locals import *
import random

#probleme gauche position = chiffre, pas transparent
# S taille de la fenetre
S= 600
GAUCHE = S/4
CENTRE= S/2
DROITE = 3*S/4
COTES = (GAUCHE, CENTRE, DROITE)
TEXTE_COTES= ("GAUCHE", "CENTRE", "DROITE")

# Nombres essais en phase d'essai
nombre_essais_NiNi=5
nombre_essais_Simon=5
nombre_essais_Stroop=5
nombre_essais_Sisi=5
# Nombres essais en phase évaluation
nombre_de_blocs_complets_sisi=6

#Couleurs essais
BLEU = (0, 125, 255)
ORANGE = (255, 125, 0)
COULEURS = (BLEU, ORANGE)
# Couleur feedback et insctructions
NOIR = (0, 0, 0)
#Couleur fond d'écran
FOND = (211,211,211)

def creation_fichier():
# demande le nom et crée un fichier avec,
# renvoie dans la console la création du fichier et le nom dans les instructions
    print "Quel est votre prénom ?"
    nom = raw_input()
    f = open((nom +'.txt'), 'a')
# Rappel : entete de colonne "NOM", "TACHE", "COULEUR", "REPONSE", "CORRECTE", "COTE", "TEXTE", "TEMPS"
    print >>f, "NOM", "TACHE", "COULEUR", "TOUCHE", "REPONSE", "TEMPS", "COTE", "SIMON", "TEXTE", "STROOP"
    print "le fichier " + nom + ".txt a ete créé"
    return f, nom

def instructions(fenetre, nom):
# affiche les instructions, ligne par ligne
    pygame.font.init
    fenetre.fill(FOND)
    font = pygame.font.Font(None, 30)
### ligne à couper
    text = ("Bienvenue dans ce super test " + nom + " !",
            u"Merci de regarder le point de fixation en début d'essai",
            u"",
            u"Dès que vous appuyez sur espace, vous verrez apparaître",
            u"un cercle ou un mot qui sera orange ou bleu.",
            u"Votre tâche, si vous l\'acceptez, est de taper sur",
            u"la touche \'Droite\' si la couleur du stimulus est bleu",
            u"et \'Gauche\' si la couleur du stimulus est orange.",
            u"Merci pour votre coopération.", "",
            u"Appuyez sur la touche \'Espace\' pour démarrer",
            u"un essai dès que vous êtes prêt",
            u"A tout moment, appuyez sur \'Esc\' pour quitter")

    for i, txt in enumerate(text):
        ordonnee_ligne= 20 + 40*i
        MY_TEXT= font.render(txt, 1, NOIR)
        fenetre.blit(MY_TEXT, [20, ordonnee_ligne])
        pygame.time.wait(200)
        pygame.display.flip()
    attente()

def attente():
# attend que le sujet appuie sur la touche espace avant de débuter un essai,
# si le sujet appuie sur esc, le programme se quitte
    start = False
    pygame.event.get()
    while not start:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    start = True
                elif e.key == K_ESCAPE:
                    raise Exception

def point_fixation(fenetre):
# cree un point de fixation centré, appelle attente, nettoie l'écran
    fenetre.fill(FOND)
    pygame.draw.circle(fenetre, NOIR, (S/2, S/2), 3, 0)
    pygame.display.flip()
    attente()
    fenetre.fill(FOND)
    pygame.display.flip()

def melange_couleur_cote_texte(tache):
# creation de liste comprenant un essai comprenant chacun des listes [couleur, cote, texte]
    color_cote_texte_list_trial=[]
    for texte in TEXTE_COTES:
        for color in COULEURS:
            for cote in COTES:
                if tache == "Simon-Stroop-evaluation":
                    for i in range(nombre_de_blocs_complets_sisi):
#liste de 1800 essais maximum
                        color_cote_texte_list_trial.append([color, cote, texte])
                else:
                     color_cote_texte_list_trial.append([color, cote, texte])
    random.shuffle(color_cote_texte_list_trial)
    return color_cote_texte_list_trial

def nini_et_simon(fenetre, tache, liste_essais, f, nom):
# string pour inscription dans fichier f
#essai à partir de la liste générée pour chaque tache d'ordre [couleur, cote, texte]
    for essai in liste_essais:
        # changer nombre essai, être systématique pas aléatoire
        point_fixation(fenetre)
        if tache == "NiNi":
            position=S/2
        elif tache == "Simon":
            position= essai[1]
        pygame.draw.circle(fenetre, essai[0], (position, S/2), 30, 0)
        pygame.display.flip()
        t0 = pygame.time.get_ticks()
        collecte(fenetre, tache, essai, t0, f, nom)
        pygame.time.wait(500)
    return(tache, essai, t0)

def stroop_et_sisi(fenetre, tache, liste_essais, f, nom):
# string pour inscription dans fichier f
# tache stroop ou Simon-Stroop
    font = pygame.font.Font(None, 50)
#essai à partir de la liste générée pour chaque tache d'ordre [couleur, cote, texte]
    nombre_essai = 0
    for essai in liste_essais:
        point_fixation(fenetre)
        if tache == "Stroop":
            position=S/2
        elif tache == "Simon-Stroop test" or "Simon-Stroop-evaluation":
            position= essai[1]
        MY_TEXT = font.render(essai[2], 1, essai[0])
        MY_TEXT_POSITION = MY_TEXT.get_rect()
        MY_TEXT_POSITION.center = fenetre.get_rect().center
        fenetre.blit(MY_TEXT, [position-70, S/2-15])
        pygame.display.flip()
        t0 = pygame.time.get_ticks()
        collecte(fenetre, tache, essai, t0, f, nom)
        pygame.time.wait(500)
    return (tache, essai, t0)

def collecte(fenetre, tache, essai, t0, f, nom):
    # collecte temps de réaction et le renvoie à feedback et à reour console et à fichier
# On utilise la liste crée pour chaque tache ordre [essai[0] : couleur, essai[1] : cote, essai[2] : texte]

# change les variables brutes utilisées pour affichage en variables intelligibles pour inscription dans fichier :
# O = Orange, B = Bleu, None : variable non pertinente dans l'essai
    effet_Simon = None
    effet_Stroop = None

#[essai[0] : couleur
    if essai[0]== (255, 125, 0):
        essai[0] = "O"
    elif essai[0]== (0, 125, 255):
        essai[0] = "B"

#[essai[1] : cote
    if tache=="NiNi" or tache =="Stroop":
        essai[1]=None
    else:
        if essai[1]==GAUCHE:
            essai[1] = "Cote_Gauche"
        elif essai[1]==CENTRE:
            essai[1] = "Centre"
        elif essai[1]==DROITE:
            essai[1] = "Cote_Droit"

        if (essai[1] == "Cote_Gauche" and essai[0] == "O") or (essai[1] == "Cote_Droit" and essai[0] == "B"):
            effet_Simon= "Compatible"
        elif (essai[1] =="Cote_Gauche" and essai[0] == "B") or (essai[1] == "Cote_Droit" and essai[0] == "O"):
            effet_Simon= "Incompatible"
        else:
            effet_Simon = "Neutre"

    if tache in ('NiNi', 'Simon'):
        essai[2]=None
    else:
        if (essai[2]== 'GAUCHE' and essai[0] == "O") or (essai[2] == 'DROITE' and essai[0] == "B"):
            effet_Stroop = "Congruent"
        elif (essai[2]== 'DROITE' and essai[0] == "O") or (essai[2] == 'GAUCHE' and essai[0] == "B"):
            effet_Stroop = "Incongruent"
        else:
            effet_Stroop = "Neutre"

# renvoie un feedback au sujet, récupère e : evenement
    collecte = False
    while not collecte:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_LEFT or e.key == K_RIGHT:
                    temps_reaction=mesure_temps_reaction(t0)
                    if e.key== 276:
                        e.key="TOUCHE_GAUCHE"
                    elif e.key==275:
                        e.key="TOUCHE_DROITE"
                    if (e.key == "TOUCHE_GAUCHE" and essai[0] == "O") or (e.key == "TOUCHE_DROITE" and essai[0] == "B"):
                        reponse = "Correcte"
                        retour_console(tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
    # Rappel : entete de colonne "NOM", "TACHE", "COULEUR", "REPONSE", "CORRECTE", "COTE", "TEXTE", "TEMPS"
    # On utilise la liste crée pour chaque tache d'ordre [couleur, cote, texte]
                        feedback (fenetre, f, nom, tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
                        collecte=True
                    elif (e.key == "TOUCHE_GAUCHE" and essai[0] == "B") or (e.key == "TOUCHE_DROITE"and essai[0] == "O"):
                        reponse = "Incorrecte"
                        retour_console(tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
# Rappel : entete de colonne "NOM", "TACHE", "COULEUR", "REPONSE", "CORRECTE", "COTE", "TEXTE", "TEMPS"
# On utilise la liste crée pour chaque tache d'ordre [couleur, cote, texte]
                        feedback (fenetre, f, nom, tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
                        collecte=True
                    else:
                        print "error"
    return (e, reponse, temps_reaction)

def retour_console(tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop):
    print ""
    print "Tâche : "+ tache
    print "Essai : " + str(essai)
    print "Touche : " + e.key
    print "Reponse : " + reponse
    print "temps de reaction : " + str(temps_reaction)
    print "Simon : " + str(effet_Simon)
    print "Stroop : " + str(effet_Stroop)

def feedback(fenetre, f, nom, tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop):
    pygame.font.init
    font = pygame.font.Font(None, 50)
    MY_TEXT= font.render(reponse, 1, NOIR)
    fenetre.blit(MY_TEXT, [230, 450])
    pygame.display.flip()
# rappel en-têtes "NOM", "TACHE", "COULEUR", "TOUCHE", "REPONSE", "TEMPS", "COTE", "SIMON", "TEXTE", "STROOP"
# rappel : on utilise la liste créée pour chaque tache d'ordre [couleur, cote, texte]
    print >>f, nom, tache, essai[0], e.key, reponse, temps_reaction,  essai[1], effet_Simon, essai[2],  effet_Stroop
    pygame.time.wait(500)

def mesure_temps_reaction(t0):
    temps_reaction = False
    while not temps_reaction:
        temps_reaction = pygame.time.get_ticks() - t0
    return (temps_reaction)

def pause(fenetre):
# affiche les instructions, ligne par ligne
    pygame.font.init
    fenetre.fill(FOND)
    font = pygame.font.Font(None, 30)
    text = (u"Félicitations !", u"Vous êtes très fort", u"Prenez une petite pause et on continue !",
    u"", u"Appuyez sur la touche espace quand vous êtes prêt")
    for i in range(len(text)):
        ordonnee_ligne= 250 + 40*i
        MY_TEXT= font.render(text[i], 1, NOIR)
        fenetre.blit(MY_TEXT, [20, ordonnee_ligne])
        pygame.display.flip()
        pygame.time.wait(500)

    pygame.time.wait(1000)
    pygame.event.get()
    attente()

def main():
#creation fichier et creation en-tetes
    f, nom = creation_fichier()
# Affichage fenetre et instructions des taches
    fenetre = pygame.display.set_mode([S, S])
    pygame.display.set_caption('Simon-Stroop')
    instructions(fenetre, nom)


##Création liste et Tache NiNi
    tache = "NiNi"
    liste_essais=melange_couleur_cote_texte(tache)[0:nombre_essais_NiNi]
    nini_et_simon (fenetre, tache, liste_essais, f, nom)

#Création liste et Tache simon
    tache = "Simon"
    liste_essais= melange_couleur_cote_texte(tache)[0:nombre_essais_Simon]
    nini_et_simon (fenetre, tache, liste_essais, f, nom)

#Création liste et tahce stroop
    tache = "Stroop"
    liste_essais=melange_couleur_cote_texte(tache)[0:nombre_essais_Stroop]
    stroop_et_sisi (fenetre, tache, liste_essais, f, nom)

#Création liste et tache simon-stroop
    tache = "Simon-Stroop-test"
    liste_essais=melange_couleur_cote_texte(tache)[0:nombre_essais_NiNi]
    stroop_et_sisi (fenetre, tache, liste_essais, f, nom)

    pause(fenetre)

# Tache simon-stroop evaluation
    tache = "Simon-Stroop-evaluation"
    liste_essais=melange_couleur_cote_texte(tache)
    stroop_et_sisi (fenetre, tache, liste_essais, f, nom)

try:
    pygame.init()
    main()

finally:
    pygame.quit()
