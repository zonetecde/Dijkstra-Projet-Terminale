import json
import pprint
from pile import Pile
from file import File


class Graphe:
    """Création de l'objet graphe
    """

    def __init__(self):
        self.liste_adjacente = {}
        self.matrice_adjacente = []
        self.parcours = []
        self.predecesseur = {}
        self.solution = []

    def ajout_sommet(self, sommet, voisin, poids=1):
        """Ajoute un sommet au graphe

        Args:
            sommet (str): Nom du sommet
            voisin (str): Nom du voisin
            poids (int, optional): Poid entre le sommet et le voisin. Defaults to 1.
        """
        if sommet not in self.liste_adjacente:
            self.liste_adjacente[sommet] = [(voisin, poids)]
        else:
            self.liste_adjacente[sommet].append((voisin, poids))

    def __str__(self) -> str:
        """ Affiche le graph en texte
        """
        return json.dumps(self, default=lambda o: o.liste_adjacente,
                          sort_keys=True, indent=4)

    def profondeur(self, sommet):
        """Parcours le graphe en profondeur

        Args:
            sommet (str): Le sommet de départ

        Returns:
            list: Le parcours
        """
        parcours = []
        sommet_voisin = ""
        pile = Pile()

        pile.empiler(sommet)
        while not pile.est_vide():
            sommet = pile.depiler()

            if sommet not in parcours:
                parcours.append(sommet)
                for arete in self.liste_adjacente[sommet]:
                    sommet_voisin = arete[0]

                    if sommet_voisin not in parcours:
                        pile.empiler(sommet_voisin)
                        self.predecesseur[sommet_voisin] = sommet

        self.parcours = parcours
        return parcours

    def largeur(self, sommet):
        """Parcours le graphe en largeur

        Args:
            sommet (str): Le sommet de départ

        Returns:
            list: Le parcours
        """
        parcours = []
        sommet_voisin = ""
        file = File()

        file.enfiler(sommet)
        while not file.est_vide():
            sommet = file.defiler()

            if sommet not in parcours:
                parcours.append(sommet)
                for arete in self.liste_adjacente[sommet]:
                    sommet_voisin = arete[0]

                    if sommet_voisin not in parcours:
                        file.enfiler(sommet_voisin)
                        self.predecesseur[sommet_voisin] = sommet

        self.parcours = parcours
        return parcours

    def chemin(self, depart, arrivee):
        """Donne un chemin de départ à arrivée

        Args:
            depart (str): Le départ
            arrivee (str): L'arrivée
        """
        ville = arrivee
        self.dijkstra(depart, arrivee)
        while ville != depart:
            self.solution.append(ville)
            ville = self.predecesseur[ville]

        self.solution.append(ville)
        self.solution.reverse()

    def matrice(self):
        """Init la matrice adjacente du graph
        """
        villes = list(self.liste_adjacente.keys())
        villes.sort()  # ordre alphabetique

        for i in range(len(villes)):
            self.matrice_adjacente.append([None for _ in range(len(villes))])

            for z in range(len(villes)):
                tuple = [x for x in self.liste_adjacente[villes[i]]
                         if x[0] == villes[z]]
                if len(tuple) == 0:
                    self.matrice_adjacente[i][z] = 0
                else:
                    self.matrice_adjacente[i][z] = tuple[0][1]

    def dijkstra(self, depart):
        self.sommet_visites = []
        self.distances = {}  # clé = sommet, valeur = distance
        self.predecesseur = {}  # clé = sommet, valeur = prédécesseur

        for sommet in self.liste_adjacente:
            self.distances[sommet] = float('inf')
            self.predecesseur[sommet] = None

        self.distances[depart] = 0

        for sommet in self.liste_adjacente:
            # rechercher dans les distances la plus petite
            plus_petite_distance = float('inf')
            sommet_plus_petite_distance = ""

            for sommet in self.liste_adjacente:
                if sommet not in self.sommet_visites and self.distances[sommet] < plus_petite_distance:
                    plus_petite_distance = self.distances[sommet]
                    sommet_plus_petite_distance = sommet

            self.sommet_visites.append(sommet_plus_petite_distance)

            for voisin in self.liste_adjacente[sommet_plus_petite_distance]:
                if voisin[1] + self.distances[sommet_plus_petite_distance] < self.distances[voisin[0]]:
                    self.distances[voisin[0]] = voisin[1] + \
                        self.distances[sommet_plus_petite_distance]
                    self.predecesseur[voisin[0]] = sommet_plus_petite_distance

        return self.distances, self.predecesseur


graphe_tgv = Graphe()
graphe_tgv.ajout_sommet("Marseille", "Bordeaux", 505)
graphe_tgv.ajout_sommet("Marseille", "Lyon", 278)
graphe_tgv.ajout_sommet("Rennes", "Paris", 355)
graphe_tgv.ajout_sommet("Paris", "Lille", 204)
graphe_tgv.ajout_sommet("Paris", "Rennes", 355)
graphe_tgv.ajout_sommet("Paris", "Bordeaux", 499)
graphe_tgv.ajout_sommet("Paris", "Metz", 330)
graphe_tgv.ajout_sommet("Paris", "Lyon", 391)

graphe_tgv.ajout_sommet("Lyon", "Marseille", 278)
graphe_tgv.ajout_sommet("Lyon", "Paris", 391)
graphe_tgv.ajout_sommet("Lyon", "Strasbourg", 382)

graphe_tgv.ajout_sommet("Lille", "Paris", 204)
graphe_tgv.ajout_sommet("Metz", "Strasbourg", 129)
graphe_tgv.ajout_sommet("Metz", "Paris", 330)
graphe_tgv.ajout_sommet("Strasbourg", "Lyon", 382)
graphe_tgv.ajout_sommet("Strasbourg", "Metz", 128)
graphe_tgv.ajout_sommet("Bordeaux", "Paris", 499)
graphe_tgv.ajout_sommet("Bordeaux", "Marseille", 505)


print(graphe_tgv.dijkstra("Metz"))


# graphe = Graphe()

# graphe.ajout_sommet("Accueil", "G")
# graphe.ajout_sommet("G", "Accueil")
# graphe.ajout_sommet("G", "C")
# graphe.ajout_sommet("G", "H")
# graphe.ajout_sommet("G", "D")
# graphe.ajout_sommet("Boutique", "A")
# graphe.ajout_sommet("A", "C")
# graphe.ajout_sommet("A", "B")
# graphe.ajout_sommet("B", "F")
# graphe.ajout_sommet("B", "A")
# graphe.ajout_sommet("B", "D")
# graphe.ajout_sommet("B", "E")
# graphe.ajout_sommet("C", "A")
# graphe.ajout_sommet("C", "D")
# graphe.ajout_sommet("C", "G")
# graphe.ajout_sommet("D", "B")
# graphe.ajout_sommet("D", "C")
# graphe.ajout_sommet("D", "E")
# graphe.ajout_sommet("D", "G")
# graphe.ajout_sommet("E", "D")
# graphe.ajout_sommet("E", "B")
# graphe.ajout_sommet("F", "B")
# graphe.ajout_sommet("F", "E")
# graphe.ajout_sommet("H", "G")

# graphe.chemin("H", "A")
# print(graphe.solution)
