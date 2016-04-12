# -*- encoding: utf-8 -*-

# randomiser direction et couleur changer direction
#pas de diagonales
# Plein écran
# faire pauses ++
# supprimer déclenchement de l'essai manuel

import pygame, sys
from pygame.locals import *
import random
import copy

#probleme gauche position = chiffre, pas transparent
# S taille de la fenetre
S= 600
GAUCHE = S/4
DROITE = 3*S/4
CENTRE = S/2

HAUT = S/4
BAS= 3*S/4
COTES = (GAUCHE, HAUT, BAS, DROITE)
TEXTE_COTES= ("GAUCHE", "HAUT", "BAS", "DROITE")
abcisses = (GAUCHE, DROITE, CENTRE, CENTRE)
ordonnees = (HAUT, BAS, CENTRE, CENTRE)

# Nombres essais en phase d'essai
nombre_essais_NiNi=8
nombre_essais_Simon=8
nombre_essais_Stroop=5
nombre_essais_Sisi=5
# Nombres essais en phase évaluation
nombre_de_blocs_complets_sisi=1

#Couleurs essais
ROUGE = (255, 0, 0)
VERT = (0,255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)

COULEURS = (ROUGE, VERT, BLEU, JAUNE)
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
            u"la touche \'Droite\' si la couleur du stimulus est vert",
            u"et \'Gauche\' si la couleur du stimulus est rouge.",
            u"et \'Haut\' si la couleur du stimulus est bleu.",
            u"et \'Bas\' si la couleur du stimulus est jaune.",
            u"Merci pour votre coopération.", "",
            u"Appuyez sur la touche \'Espace\' pour démarrer",
            u"un essai dès que vous êtes prêt",
            u"A tout moment, appuyez sur \'Esc\' pour quitter")

    for i, txt in enumerate(text):
        ordonnee_ligne= 10 + 40*i
        MY_TEXT= font.render(txt, 1, NOIR)
        fenetre.blit(MY_TEXT, [20, ordonnee_ligne])
        pygame.time.wait(50)
        pygame.display.flip()

    attente()
    fenetre.fill(FOND)
    rouecouleur = pygame.image.load('rouecouleur.gif')
    rouecouleurStretchedImage = pygame.transform.scale(rouecouleur, (S, S))
    fenetre.blit(rouecouleurStretchedImage, (0,0))

    pygame.display.flip()
    pygame.time.wait(50)

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
    liste_essais=[]
    for texte in TEXTE_COTES:
        essai={}
        essai["texte"]=texte
        for color in COULEURS:
            essai2 = copy.deepcopy(essai)
            essai2["couleur"]=color
            #rajouter reponse correcte
            if tache == "NiNi":
                essai3 = copy.deepcopy(essai2)
                essai3["x"]=S/2
                essai3["y"]=S/2
            for x in abcisses:
                essai3 = copy.deepcopy(essai2)
                essai3["x"]=x
                if essai3["x"] == S/2:
                    for y in ordonnees:
                        essai4 = copy.deepcopy(essai3)
                        essai4["y"]=y
                        liste_essais.append(essai4)
                else:
                    for y in ordonnees:
                        essai4 = copy.deepcopy(essai3)
                        essai4["y"]=S/2
                        liste_essais.append(essai4)

    print liste_essais
    random.shuffle(liste_essais)
    print liste_essais
    #ATTENTION randomise sur texte pas sur autre éléments
    return liste_essais

def nini_et_simon(fenetre, tache, liste_essais, f, nom):
# string pour inscription dans fichier f
#essai à partir de la liste générée pour chaque tache d'ordre [couleur, cote, texte]
    for essai in liste_essais:
        # changer nombre essai, être systématique pas aléatoire
        point_fixation(fenetre)
        if tache == "NiNi":
            position_abs=S/2
            position_ord=S/2
        elif tache == "Simon":
            position_abs= essai["x"]
            position_ord= essai["y"]
        pygame.draw.circle(fenetre, essai["couleur"], (position_abs, position_ord), 30, 0)
        pygame.display.flip()
        t0 = pygame.time.get_ticks()
        collecte(fenetre, tache, essai, t0, f, nom)
        pygame.time.wait(400)
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
            essai["x"]=S/2
            essai["y"]=S/2

        MY_TEXT = font.render(essai["texte"], 1, essai["couleur"])
        MY_TEXT_POSITION = MY_TEXT.get_rect()
        MY_TEXT_POSITION.center = fenetre.get_rect().center
        fenetre.blit(MY_TEXT, [essai["x"]-30, S/2-15])
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
#    effet_Simon = None
#    effet_Stroop = None

#    if tache=="NiNi" or tache =="Stroop":
#        if (essai[1] == "Cote_Gauche" and essai[0] == "O") or (essai[1] == "Cote_Droit" and essai[0] == "B"):
#            effet_Simon= "Compatible"
#        elif (essai[1] =="Cote_Gauche" and essai[0] == "B") or (essai[1] == "Cote_Droit" and essai[0] == "O"):
#            effet_Simon= "Incompatible"
#        else:
#            effet_Simon = "Neutre"
#
#    if tache in ('NiNi', 'Simon'):
#        essai[2]=None
#    else:
#        if (essai[2]== 'GAUCHE' and essai["couleur"]  == "O") or (essai["couleur"] == 'DROITE' and essai["couleur"] == "B"):
#            effet_Stroop = "Congruent"
#        elif (essai[2]== 'DROITE' and essai["couleur"]  == "O") or (essai[2] == 'GAUCHE' and essai["couleur"]  == "B"):
#            effet_Stroop = "Incongruent"
#        else:
#            effet_Stroop = "Neutre"

# renvoie un feedback au sujet, récupère e : evenement

#Couleurs essais
#ROUGE = (255, 0, 0)
#VERT = (0,255, 0)
#BLEU = (0, 0, 255)
#JAUNE = (255, 255, 0)

    collecte = False
    while not collecte:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_LEFT or e.key == K_RIGHT or e.key == K_UP or e.key == K_DOWN:
                    temps_reaction=mesure_temps_reaction(t0)
                    if (e.key == K_LEFT and essai["couleur"]  == (255, 0, 0)) or (e.key == K_RIGHT and essai["couleur"]  == (0,255, 0)) or (e.key == K_UP and essai["couleur"] == (0, 0, 255)) or (e.key == K_DOWN and essai["couleur"] == (255, 255, 0)):
                        reponse = "Correct"
                        retour_console(tache, essai, e, reponse, temps_reaction)
#                        retour_console(tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
    # Rappel : entete de colonne "NOM", "TACHE", "COULEUR", "REPONSE", "CORRECTE", "COTE", "TEXTE", "TEMPS"
    # On utilise la liste crée pour chaque tache d'ordre [couleur, cote, texte]
                        #feedback (fenetre, f, nom, tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
                        feedback (fenetre, f, nom, tache, essai, e, reponse, temps_reaction)
                        collecte=True
                    else:
                        reponse = "Incorrect"
                        retour_console(tache, essai, e, reponse, temps_reaction)
#                       retour_console(tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
# Rappel : entete de colonne "NOM", "TACHE", "COULEUR", "REPONSE", "CORRECTE", "COTE", "TEXTE", "TEMPS"
# On utilise la liste crée pour chaque tache d'ordre [couleur, cote, texte]

#                        feedback (fenetre, f, nom, tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop)
                        feedback (fenetre, f, nom, tache, essai, e, reponse, temps_reaction)
                        collecte=True

    return (e, reponse, temps_reaction)

#def retour_console(tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop):
def retour_console(tache, essai, e, reponse, temps_reaction):
    print ""
    print "Tâche : "+ tache
    print "Essai : " + str(essai)
    print "Touche : " + str(e.key)
    print "Reponse : " + reponse
    print "temps de reaction : " + str(temps_reaction)
    print "x : " + str (essai["x"])
    print "y : " + str(essai["y"])
#    print "Simon : " + str(effet_Simon)
#    print "Stroop : " + str(effet_Stroop)

#def feedback(fenetre, f, nom, tache, essai, e, reponse, temps_reaction, effet_Simon, effet_Stroop):
def feedback(fenetre, f, nom, tache, essai, e, reponse, temps_reaction):

    pygame.font.init
    font = pygame.font.Font(None, 50)
    MY_TEXT= font.render(reponse, 1, NOIR)
    fenetre.blit(MY_TEXT, [240, 500])
    pygame.display.flip()
# rappel en-têtes "NOM", "TACHE", "COULEUR", "TOUCHE", "REPONSE", "TEMPS", "COTE", "SIMON", "TEXTE", "STROOP"
# rappel : on utilise la liste créée pour chaque tache d'ordre [couleur, cote, texte]
#    print >>f, nom, tache, essai[0], e.key, reponse, temps_reaction,  essai[1], effet_Simon, essai[2],  effet_Stroop
    print >>f, nom, tache, essai["couleur"], e.key, reponse, temps_reaction,  essai["x"], essai["texte"]

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
