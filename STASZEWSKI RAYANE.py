#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 21:50:36 2023

@author: matt
"""

import pandas as pd


class Graphe:
    """
    Création de l'objet graphe
    """

    def __init__(self):
        self.liste_adjacence = {}
        self.distances = {}
        self.predecesseurs = {}
        self.visites = []

    def ajout_sommet(self, sommet, voisin, poids=1):
        """Ajoute un sommet au graphe
        Args:
            sommet (str): Nom du sommet
            voisin (str): Nom du voisin
            poids (int, optional): Poid entre le sommet et le voisin. Defaults to 1.
        """
        if sommet not in self.liste_adjacence:
            self.liste_adjacence[sommet] = [(voisin, poids)]
        else:
            self.liste_adjacence[sommet].append((voisin, poids))

    def chargement(self, fichier):
        """Charge un graphe depuis un fichier
        Args:
            fichier (str): Nom du fichier
        """
        content = pd.read_csv(fichier, sep=';')
        for i in range(0, len(content)):
            self.ajout_sommet(content['name1'][i],
                              content['name2'][i],
                              content['distance'][i])

    def classement_adjacence(self):
        """
        Trie dans l'ordre alphabétique les valeurs de la liste d'adjacence
        """
        for sommet in self.liste_adjacence:
            self.liste_adjacence[sommet].sort()


    def initialisation(self, depart):
        """
        Initialise les dictionnaires distances et predecesseurs
        """
        for sommet in self.liste_adjacence:
            self.distances[sommet] = float('inf')
            
        self.predecesseurs[depart] = depart
        self.distances[depart] = 0
        self.visites = [] # Pour djikstra on le reset

        return self.distances, self.predecesseurs

    def chemin(self, depart, arrivee):
        """Trouve le chemin à partir du dictionnaire des predecesseurs

        Args:
            depart (str): Sommet de départ
            arrivee (str): Sommet d'arrivée
        """
        ville = arrivee
        chemin = []

        while ville != depart:
            chemin.append(ville)
            ville = self.predecesseurs[ville]

        chemin.append(ville)
        chemin.reverse()

        return chemin

    def distance_mini(self):
        """Renvoie pour une étape donnée la distance minimale du départ
        et le sommet qui correspond

        Returns:
            distance (int): Distance minimale
            ville (str): Nom du sommet
        """
        distance = float('inf')
        ville = ""

        # Parcourt les sommets 
        for sommet in self.liste_adjacence:
            # Si la distance du sommet est inférieure à la distance minimale
            if sommet not in self.visites and self.distances[sommet] < distance:
                # Met à jour la distance minimale et le sommet
                distance = self.distances[sommet]
                ville = sommet

        return distance, ville

    def dijkstra(self, depart, arrivee):
        """Trouve le chemin et la distance minimale 

        Args:
            depart (str): Le nom du sommet de départ
            arrivee (str): Le nom du sommet d'arrivée
        """

        self.initialisation(depart)
        sommet = depart
        # Tant qu'on n'a pas visité tous les sommets
        etape = 0
        while sommet != arrivee:
            distance_mini, sommet = self.distance_mini()

            self.visites.append(sommet)
           
            # Parcourt les voisins du sommet en cours
            voisins = self.liste_adjacence[sommet]

            for voisin, distance in filter(lambda voisin: voisin not in self.visites, voisins): # au lieu de mettre 2 if imbriqué
                # Calcule la distance en passant par le sommet en cours        
                if self.distances[sommet] + distance < self.distances[voisin]:
                    # Met à jour la distance du voisin car on a trouvé un chemin plus court
                    self.distances[voisin] = self.distances[sommet] + distance
                    self.predecesseurs[voisin] = sommet

            etape += 1

            # Print le tableau à chaque itération
            self.print_tableau(etape)

        # Renvoie la distance et le chemin
        return distance_mini, self.chemin(depart, arrivee)

    def print_tableau(self, index_etape):
        """ Print l'étape actuelle sous forme de tableau

        Args:
            index_etape (int): Le numéro de l'étape
        """

        # Récupère les sommets en cours et les trie
        sommets_en_cours = list(self.distances.keys())
        sommets_en_cours.sort()

        # Récupère les distances et les prédécesseurs
        distances = list(self.distances.values())
        predecesseurs = list(self.predecesseurs.values())

        print("Etape " + str(index_etape))

        # Print les colonnes
        print("{:<15}".format("Sommet en cours"), end="\t")
        for sommet in sommets_en_cours:
            print("{:<15}".format(sommet), end="\t")
        print()
        print("{:<15}".format("Distance"), end="\t")
        for distance in distances:
            print("{:<15}".format(distance), end="\t")
        print()
        print("{:<15}".format("Prédécesseur"), end="\t")
        for predecesseur in predecesseurs:
            print("{:<15}".format(predecesseur), end="\t")
        print()
        print()

# =============================================================================
# PROGRAMME PRINCIPAL
# =============================================================================


if __name__ == '__main__':
    tgv = Graphe()
    
    tgv.chargement("tgv_edges.csv")

    # # Vérification de "classement_adjacence"
    tgv.classement_adjacence()
    assert tgv.liste_adjacence == {'Paris': [('Bordeaux', 499), ('Lille', 204), ('Lyon', 391), ('Metz', 330), ('Rennes', 335)],
                                   'Lille': [('Paris', 204)],
                                   'Rennes': [('Paris', 335)],
                                   'Bordeaux': [('Marseille', 505), ('Paris', 499)],
                                   'Metz': [('Paris', 330), ('Strasbourg', 129)],
                                   'Lyon': [('Marseille', 278), ('Paris', 391), ('Strasbourg', 382)],
                                   'Marseille': [('Bordeaux', 505), ('Lyon', 278)],
                                   'Strasbourg': [('Lyon', 382), ('Metz', 129)]}


    # # Vérification de "initialisation"
    distances, predecesseurs = tgv.initialisation("Metz")

    assert distances == {'Paris': float('inf'),
                         'Lille': float('inf'),
                         'Rennes': float('inf'),
                         'Bordeaux': float('inf'),
                         'Metz': 0,
                         'Lyon': float('inf'),
                         'Marseille': float('inf'),
                         'Strasbourg': float('inf')}
    assert predecesseurs == {'Metz': 'Metz'}

    # # Vérification de "chemin"
    tgv.predecesseurs = {'Metz': 'Metz',
                         'Paris': 'Metz',
                         'Strasbourg': 'Metz',
                         'Lyon': 'Strasbourg',
                         'Bordeaux': 'Paris',
                         'Lille': 'Paris',
                         'Rennes': 'Paris',
                         'Marseille': 'Lyon'}
    assert tgv.chemin("Metz", "Bordeaux") == ['Metz', 'Paris', 'Bordeaux']

    # # Vérification de "distance_mini"
    tgv.visites = ['Metz', 'Strasbourg', 'Paris',
                   'Lyon', 'Lille', 'Rennes', 'Marseille']
    tgv.distances = {'Paris': 330,
                     'Lille': 534,
                     'Rennes': 665,
                     'Bordeaux': 829,
                     'Metz': 0,
                     'Lyon': 511,
                     'Marseille': 789,
                     'Strasbourg': 129}
    dist_mini, ville = tgv.distance_mini()
    assert dist_mini == 829
    assert ville == "Bordeaux"

    depart = "Metz"
    arrivee = "Lyon"

    results = tgv.dijkstra(depart, arrivee)

    print("Distance : " + str(results[0]))
    print("Chemin : " + str(results[1]))