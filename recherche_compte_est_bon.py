#! /usr/bin/env python3

""" Implémentation des parcours de l’arbre de calculs à la volée :
- parcours en profondeur d’abord itératif
- parcours en profondeur d’abord récursif
- parcours en largeur d’abord itératif """

from TAD.piles_listes_python import Pile
from TAD.files_listes_python import File
from TAD.piles_listes_simplement_chainees import Pile
from TAD.files_listes_doublement_chainees import File
from notation_polonaise_inverse import *

OPERATEURS = ("+", "-", "*", "/")


def _appliquer_operateur(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b if a >= b else None
    if op == "*":
        return a * b
    if op == "/":
        if b != 0 and a % b == 0:
            return a // b
        return None
    return None


def _generer_suivants(expr, pile_vals, restants):
    enfants = []

    deja_vus = set()
    for i, carton in enumerate(restants):
        if carton not in deja_vus:
            deja_vus.add(carton)
            nouveaux_restants = restants[:i] + restants[i + 1 :]
            enfants.append((expr + [carton], pile_vals + [carton], nouveaux_restants))

    if len(pile_vals) >= 2:
        b = pile_vals[-1]
        a = pile_vals[-2]
        base = pile_vals[:-2]
        for op in OPERATEURS:
            res = _appliquer_operateur(a, b, op)
            if res is not None:
                enfants.append((expr + [op], base + [res], restants))

    return enfants


def parcours_DFS(cartons, cible):
    nb_noeuds = 0
    meilleure_expression = []
    meilleure_distance = float("inf")
    taille_max_pile = 0

    pile = Pile()
    pile.empiler(([], [], list(cartons)))
    taille_max_pile = max(taille_max_pile, pile.longueur())

    while not pile.est_vide():
        expr, pile_vals, restants = pile.depiler()
        nb_noeuds += 1

        if len(pile_vals) == 1:
            valeur = pile_vals[0]
            distance = abs(cible - valeur)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_expression = list(expr)
                print(f"Rapprochement ({valeur}, cible={cible}) : {' '.join(map(str, expr))}")
            if valeur == cible:
                return meilleure_expression, nb_noeuds

        for enfant in reversed(_generer_suivants(expr, pile_vals, restants)):
            pile.empiler(enfant)
            taille_max_pile = max(taille_max_pile, pile.longueur())

    return meilleure_expression, nb_noeuds


def parcours_BFS(cartons, cible):
    nb_noeuds = 0
    meilleure_expression = []
    meilleure_distance = float("inf")
    taille_max_file = 0

    file = File()
    file.enfiler(([], [], list(cartons)))
    taille_max_file = max(taille_max_file, file.longueur())

    while not file.est_vide():
        expr, pile_vals, restants = file.defiler()
        nb_noeuds += 1

        if len(pile_vals) == 1:
            valeur = pile_vals[0]
            distance = abs(cible - valeur)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_expression = list(expr)
                print(f"Rapprochement ({valeur}, cible={cible}) : {' '.join(map(str, expr))}")
            if valeur == cible:
                return meilleure_expression, nb_noeuds

        for enfant in _generer_suivants(expr, pile_vals, restants):
            file.enfiler(enfant)
            taille_max_file = max(taille_max_file, file.longueur())

    return meilleure_expression, nb_noeuds


def parcours_DFS_recursif(cartons, cible):
    meilleure_expression = []
    nb_noeuds = 0
    meilleure_distance = float("inf")
    cible_atteinte = False

    def parcours_DFSR_aux(choisis, pile_vals, restants):
        nonlocal meilleure_expression, nb_noeuds, meilleure_distance, cible_atteinte

        if cible_atteinte:
            return

        nb_noeuds += 1

        if len(pile_vals) == 1:
            valeur = pile_vals[0]
            distance = abs(cible - valeur)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_expression = list(choisis)
                print(f"Rapprochement ({valeur}, cible={cible}) : {' '.join(map(str, choisis))}")
            if valeur == cible:
                cible_atteinte = True
                return

        for next_expr, next_pile, next_rest in _generer_suivants(choisis, pile_vals, restants):
            parcours_DFSR_aux(next_expr, next_pile, next_rest)
            if cible_atteinte:
                return

    parcours_DFSR_aux([], [], list(cartons))
    return meilleure_expression, nb_noeuds


if __name__ == "__main__":
    print("DFS :", parcours_DFS([3, 5, 7, 9, 25, 50], 859))
    print("BFS :", parcours_BFS([3, 5, 7, 9, 25, 50], 859))
    print("DFSR :", parcours_DFS_recursif([3, 5, 7, 9, 25, 50], 859))