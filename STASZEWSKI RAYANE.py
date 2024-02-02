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

    def dijkstra(self, depart, arrivee, verbose = False):
        """Trouve le chemin et la distance minimale 

        Args:
            depart (str): Le nom du sommet de départ
            arrivee (str): Le nom du sommet d'arrivée
        """

        self.initialisation(depart)
        sommet = depart
        # Tant qu'on n'a pas visité tous les sommets
        etape = 0
        while len(self.visites) != len(self.predecesseurs):
            distance_mini, sommet = self.distance_mini()

            self.visites.append(sommet)
           
            # Parcourt les voisins du sommet en cours
            voisins = self.liste_adjacence[sommet]

            for voisin, distance in voisins:
                if voisin not in self.visites:
                        # Calcule la distance en passant par le sommet en cours        
                        if self.distances[sommet] + distance < self.distances[voisin]:
                            # Met à jour la distance du voisin car on a trouvé un chemin plus court
                            self.distances[voisin] = self.distances[sommet] + distance
                            self.predecesseurs[voisin] = sommet

            etape += 1

            # Print le tableau à chaque itération
            if verbose:
                self.print_tableau(etape)

        # Renvoie la distance et le chemin
        return self.distances[arrivee], self.chemin(depart, arrivee)

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

class Metro:
    def __init__(self, fichier_sommets, fichier_arcs) -> None:
        self.fichier_sommets = fichier_sommets
        self.fichier_arcs = fichier_arcs
        self.sommet_ligne = {}
        self.sommet_id = {}
        self.sommet_nom = {}

    def fabrication_graphe(self):
        """Crée un graphe à partir des fichiers sommets et arcs
        """
        # Création du graphe
        self.metro = Graphe()

        # Chargement des arcs
        df_arcs = pd.read_csv(self.fichier_arcs, sep=';')

        for i in range(0, len(df_arcs)):
            self.metro.ajout_sommet(df_arcs['id1'][i], df_arcs['id2'][i], df_arcs['time'][i])

        self.metro.classement_adjacence()

    def recuperation_donnees(self):
        """Récupère les données des sommets
        """
        df_sommets = pd.read_csv(self.fichier_sommets, sep=';')

        df_sommets.set_index('name').to_dict()

        self.sommet_ligne = df_sommets.set_index('id').to_dict()['line']

        self.sommet_id = df_sommets.set_index('id').to_dict()['name']

        self.sommet_nom = df_sommets.set_index('name').to_dict()['id']

    def itineraire_dijkstra(self, depart, arrivee):
        """Dijkstra pour le métro

        Args:
            depart (str): Nom du sommet de départ
            arrivee (str): Nom du sommet d'arrivée
        """
        depart = self.sommet_nom[depart]
        arrivee = self.sommet_nom[arrivee]

        results = list(self.metro.dijkstra(depart, arrivee)) # convertit le tuple en liste pour pouvoir le modifier

        results[1] = [(self.sommet_id[sommet_id], self.sommet_ligne[sommet_id]) for sommet_id in results[1]]

        return tuple(results)
    
    def affichage(self, resultats):
        """Affichage du temps et des lignes empruntées

        Args:
            resultats (tuple): Les résultats de dijkstra
        """
        duree_minutes = resultats[0]
        duree_jour = duree_minutes // 1440
        duree_heures = duree_minutes // 60
        duree_minutes %= 60

        duree_formattee = str(duree_jour).zfill(2) + ":" + str(duree_heures).zfill(2) + ":" + str(duree_minutes).zfill(2)
        print("Durée : " + duree_formattee)

        print()

        max_length = max([len(sommet) for sommet, ligne in resultats[1]])

        for sommet, ligne in resultats[1]:
            print("{:<{max_length}} : ligne {}".format(sommet, ligne, max_length=max_length))


# =============================================================================
# PROGRAMME PRINCIPAL
# =============================================================================


if __name__ == '__main__':
    tgv = Graphe()
    
    tgv.chargement("tgv_edges.csv")

    # # Vérification de "classement_adjacence"
    tgv.classement_adjacence()

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


    print("\n\n\nItinéraire de Pigalle à Place d'Italie :\n")
    metro = Metro("ratp_nodes.csv", "ratp_edges.csv")
    metro.fabrication_graphe()
    metro.recuperation_donnees()
    metro.affichage(metro.itineraire_dijkstra("Pigalle", "Place d'Italie"))

    # du tribunal de Justice à la gare de l'est
    print("\n\n\nItinéraire de Châtelet à la Gare de l'Est :\n")
    metro.affichage(metro.itineraire_dijkstra("Châtelet", "Gare de l'Est"))

    # du tribunal de Justice à la gare de l'est
    print("\n\n\nItinéraire de Châtelet à la Gare de l'Est :\n")
    metro.affichage(metro.itineraire_dijkstra("Châtelet", "Gare de l'Est"))


    print("\n\n\nItinéraire de Wall Street à Roosevelt Island :\n")
    metro = Metro("mta_nodes.csv", "mta_edges.csv")
    metro.fabrication_graphe()
    metro.recuperation_donnees()
    metro.affichage(metro.itineraire_dijkstra("Wall St", "Roosevelt Island"))

