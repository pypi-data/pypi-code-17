#!/usr/bin/env python
# -*- coding: utf-8 -*-
texts = {
    "Engine": """
                 Bienvenue dans le royaume de l'Ogre.
                 
                 Lors d'une balade dominicale, vous avez par hasard trouver le Graal (enfin vous pensez car vous ne 
                 savez toujours pas si c'est un vase, une coupe, une corne d'abondance...).
                 Tout guilleret de cette découverte, vous allez boire à la taverne et, l'alcool aidant, vous hurlez à
                 qui veut l'entendre que le saint des saints est en votre possession. 
                 Mais cette information parvient aux oreilles de l'ignoble seigneur Léodagan qui décide d'enlever votre
                 femme afin de monnayer sa vie contre le précieux objet.
                 Lorsque vous apprenez la situation, vous décidez d'effectuer un assaut sur le donjon qui retient votre 
                 chère et tendre pour la libérer.""",
    "Death": """
                 Malgré vos efforts, vous n'avez pas réussi à sortir du donjon en vie. Votre femme n'ayant plus
                 d'interêt pour Leodagan, ce dernier la vendra au marché aux esclaves de la ville.
                 Lors de sa présentation à la vente, la population hurlera à votre femme: \"Pour votre mari, c'est
                 dommage, une autre fois peut être...\" et s'esclaffera.
                 Je sais, c'est rageant. Cela mériterai une nouvelle tentative;)
                 
                                                            GAME OVER
                 """,
    "DungeonGate": """
                 Vous voila devant la porte du donjon qui est entourée de graviers. Derriere le bosquet
                 qui vous permet de vous dissilmuler, vous constatez que la porte d'entrée est surveillée par un garde
                 lourdement armé. A sa droite se trouve son cheval qui n'est, bizarrement, pas attaché.
                 
                 Que faites vous pour tenter d'entrer?
                 """,
    "DungeonGate_cheval": """
                 Lorsque le caillou frappe le cheval, ce derinier part au galop. Le garde, ne voulant pas se
                 retrouver à son tour enfermé dans le cachot, cours en direction de son cheval pour tenter de le
                 ratraper. Vous pouvez donc rentrer dans le donjon.
                 """,
    "DungeonGate_combat": """
                 Apres un premier combat difficile vous pouvez désormais entrer dans le donjon. Vous commencez à avoir
                 dés doutes sur vos chances de succes si d'autres combats de ce genre vous attendent à l'interieur.
                 """,
    "GuardsRoom_intro": """
                 Vous entrez dans la salle de garde. Dans cette salle vous surprenez 2 gardes qui sont en train de
                 boire.
                 """,
    "GuardsRoom_outro": """
                 En reprenant votre souffle après ce combat éreintant, vous constatez que les clefs des cellules sont
                 accorchées à un clou. Vous les récupèrez et vous rebroussez chemin.
                 """,
    "Cell_intro": """
                 Un escalier d'où vous parvient des cris de personne que l'on torture. Glacé d'effroi, vous déscendez
                 l'escalier à toute vitesse.""",
    "Cell_with_key": """
                 En bas de l'escalier, insérez la clé dans la serrure du cachot et aider votre femme à se
                 relever. Vous la placez derriere vous pour la protéger et lui dites \"Suis moi, il faut vite 
                 ressortir\".
                 """,
    "Cell_without_key": """
                 Vous arrivez en bas de l'escalier et par chance, votre femme se trouve dans la cellule devant vous.
                 Elle pleure de joie en vous voyant et vous remarquez que son regard semble vous dire \"Je pensais
                 ne plus jamais te revoir\". Et la, vous regardez votre femme, penaud, et lui dites: \"Et merde... 
                 J'ai pas la clé... Ne t'inquiètes pas je reviens.\" et reprenez l'escalier en sens inverse.
                 """,
    "Dormitory": """
                 Vous entrez dans le dortoir des gardes. Vous remarquez qu'un seul lit est occupé et que son occupant
                 s'est réveillé suite à votre entrée. Cela semble etre un guerrier aguérri mais heureusement, il avait
                 retiré son armure pour dormir.""",
    "Dormitory_armor": """
                 Vous récuperer l'armure près du lit, l'enfilez et rebroussez chemin.
                 """,
    "Armory": """
                 Vous entrez dans l'armurerie. Dans cette salle, vous constattez qu'il y a effectivement des armes
                 mais que celles-ci sont enfermées dans des armoires vérouillées par un cadenas à code.
                 vous avez 2 possiblités:
                    1- Forcer le cadenas
                    2- Tenter d'ouvrir le cadenas (trouver le code à 3 chiffree 10 tentatives)
                    3- Quitter la pièce
                 
                 Que faites vous? (saisissez le numéro correspondant à l'action)""",
    "Armory_fight": """
                En tentant de forcer le cadenas, vous faites beaucoup de bruit. Vous entendez la porte s'ouvrir derrière
                vous et {} gardes apparaissent. 
                """,
    "Armory_weapon": """
                Vous récuperer une arme dans l'armoire et rebroussez chemin.
                """,
    "Corridor": """
                Vous vous trouvez dans un couloir avec 5 portes. Laquelle voulez vous ouvrir? 
                (entrez un numéro de 1 à 5)
                """,
    "Corridor_fight": """
                En entrant à nouveau dans le couloir, vous tombez nez à nez avec {} gardes. C'est votre dernier
                combat. C'est le moment d'être héroïque.
                """,
    "EmptyRoom": """
                Cette pièce semble vide et bien sombre. Vous preféréez faire demi tour.
                """,
    "Victory": """
               Vous voila sorti victorieux du donjon.
               Vous rentez chez vous pour récuperer le Graal et chevauchez avec votre femme en direction de Camelot
               pour le remettre au roi Arthur. Ce dernier, qui semblait très heureux de votre présent, vous demanda 
               d'assister à la prochaine reunion de la table ronde pour raconter votre quête afin qu'elle soit
               retranscrite pour l'eternité.
               Lorsque la réunion commenca, Arthur vous ordonna chevalier puis vous demanda comment vous aviez fait pour
               trouver ce que toute la chretienté recherche depuis des centaines d'années. C'est alors que, fièrement,
               vous lui répondi : \"Mon seigneur, je suis juste allé aux champignons...\"
               C'est ainsi que fut forgée votre légende
                                                           VICTOIRE
               """
}
