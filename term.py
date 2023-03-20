# dates
from datetime import datetime

# simulation d'identification a une banque par le terminal


def check_identification(numero_identification, mot_de_passe, fichier):
    """
    str * str * str -> bool
    Verifie si le numero d'identification et le mot de passe
    sont corrects retourne True si le numero d'identification et le mot de passe
    sont corrects, False sinon
    """

    numero_identification = "00000000"  # a enlever
    mot_de_passe = "111111"  # a enlever

    with open(fichier) as f:
        global utilisateur
        global identifiant
        global cle
        for ligne in f:
            info = ligne.split("*")
            num, mot = info[0], info[1]
            if numero_identification == num and mot_de_passe == mot:
                utilisateur = info[2]
                cle = info[3]
                identifiant = num
                return True
    return False


def deconnexion():
    """None -> None
    Déconnecte l'utilisateur du compte."""
    # Déconnexion du compte
    exporter_donnees(identifiant)
    print("Vous avez été déconnecté.")
    quit()  # Quitte le programme


def decryptage_cesar(cle, message):
    """
    str * str -> str
    Decrypte le message avec la cle de Cesar
    """
    message_decrypte = ""
    for lettre in message:
        if lettre.isalpha():
            if lettre.isupper():
                message_decrypte += chr((ord(lettre) -
                                        ord("A") - int(cle)) % 26 + ord("A"))
            else:
                message_decrypte += chr((ord(lettre) -
                                        ord("a") - int(cle)) % 26 + ord("a"))
        else:
            message_decrypte += lettre
    return message_decrypte


def identification():
    """
    None -> bool
    Demande a l'utilisateur de saisir son numero de compte et son mot de passe
    Verifie si le numero de compte et le mot de passe sont corrects
    Retourne True si le numero de compte et le mot de passe sont corrects
    Retourne False sinon
    """
    print("Veuillez entrer votre numero de compte")
    compte = input()
    print("Veuillez entrer votre mot de passe")
    mot_de_passe = input()

    if check_identification(compte, mot_de_passe, "ident.txt"):
        return True
    else:
        print("Identification echouee")
        return False


def importer_donnees(identifiant_utilisateur):
    """
    None -> dict
    Lit le fichier et retourne le contenu en dict
    """
    global dict_utilisateur
    dict_utilisateur = {}
    with open(f"{identifiant_utilisateur}.txt") as f:
        contenu = f.read()
        # contenu = decryptage_cesar(cle, contenu)
        # pour chaque ligne du fichier

        for ligne in contenu.splitlines():
            # on separe les infos de la ligne
            info = ligne.split("*")
            if info[0] == "CPT":
                dict_utilisateur[info[1]] = {"budgets": [], "operations": []}
            elif info[0] == "OPE":
                dict_utilisateur[info[3]]["operations"].append(
                    {"date": info[1], "nom": info[2], "montant": float(info[4]), "type": info[5], "statut": info[6], "budget": info[7]})
            elif info[0] == "BUD":
                dict_utilisateur[info[3]]["budgets"].append(
                    {"nom": info[1], "montant": float(info[2])})
        return dict_utilisateur


def exporter_donnees(identifiant_utilisateur):
    """
    None -> None
    Exporte les donnees dans le fichier
    """
    with open(f"{identifiant_utilisateur}.txt", "w") as f:
        for compte in dict_utilisateur:
            f.write(f"CPT*{compte}\n")
            for budget in dict_utilisateur[compte]["budgets"]:
                f.write(f"BUD*{budget['nom']}*{budget['montant']}*{compte}\n")
            for operation in dict_utilisateur[compte]["operations"]:
                f.write(
                    f"OPE*{operation['date']}*{operation['nom']}*{compte}*{operation['montant']}*{operation['type']}*{operation['statut']}*{operation['budget']}\n")


def calculer_solde(compte):
    """Dict, Str -> Float
    Calcule le solde du compte."""
    solde = 0
    for operation in dict_utilisateur[compte]["operations"]:
        if operation["statut"] == "True":
            solde += operation["montant"]
    return solde


def menu():
    """Dict -> None
    Affiche une liste d’options réalisables sur la banque. Exécute la fonction définie pour l’option choisie."""
    print("-" * 50)
    # Affichage du titre
    print("Bienvenue dans votre banque en ligne !")
    # Affichage du nom de l'utilisateur
    print("Vous êtes connecté en tant que " + utilisateur + ".")
    print("-" * 50)
    # Affichage des options
    compte_principal = list(dict_utilisateur.keys())[0]
    # Affichage du solde
    print(
        f"Vous avez actuellement {calculer_solde(compte_principal)} € sur votre compte {compte_principal}")
    print("-" * 50)
    print("1. Gestion de mes comptes")
    print("2. Gestion de mes budgets")
    print("3. Déconnexion")
    print("-" * 50)
    # Vérification de la validité du choix
    choix = '0'
    while choix not in ["1", "2", "3"]:
        choix = input("Que voulez-vous faire ? ")
        if choix == "1":
            # Gestion du compte
            print("Gestion du compte")
            gestion_compte()  # Fonction à définir
        elif choix == "2":
            # Gestion des budgets
            gestion_budgets()  # Fonction à définir
            print("Gestion des budgets")
        elif choix == "3":
            # Déconnexion
            deconnexion()
        else:  # Si le choix n'est pas valide
            print("Veuillez choisir une option valide.")
            choix = input("Que voulez-vous faire ? ")

# gestion du compte


def gestion_compte():
    """
    None -> None
    Affiche une liste d’options réalisables sur le compte.
    """
    print("-" * 50)
    print("Gestion de mon compte")
    print("Solde dans le compte principal : " +
          str(calculer_solde(list(dict_utilisateur.keys())[0])) + " €")
    print("-" * 50)
    print("1. Afficher mes comptes")
    print("2. Afficher les opérations d'un compte")
    print("3. Ajouter une opération")
    print("4. Effectuer un virement")
    print("5. Retour")
    print("-" * 50)
    # Vérification de la validité du choix
    choix = '0'
    while choix not in ["1", "2", "3", "4", "5"]:
        choix = input("Que voulez-vous faire ? ")
        if choix == "1":
            # Afficher les comptes
            afficher_comptes()
            gestion_compte()
        elif choix == "2":
            print("Veuillez choisir un compte parmi ceux-ci :")
            afficher_comptes()
            # Afficher les operations
            compte = choix_compte()
            afficher_operations(compte)
            gestion_compte()
        elif choix == "3":
            # Ajouter une operation
            demande_ajout_operation()
            gestion_compte()
        elif choix == "4":
            # Effectuer un virement
            demande_virement()
            gestion_compte()
        elif choix == "5":
            # Retour
            menu()
        else:  # Si le choix n'est pas valide
            print("Veuillez choisir une option valide.")
            choix = input("Que voulez-vous faire ? ")


def afficher_comptes():
    """
    str -> None
    """
    for compte in list(dict_utilisateur.keys()):
        print(compte, ": ", calculer_solde(compte), "€")


def choix_compte():
    """
    None -> str
    Demande a l'utilisateur de choisir un compte.
    """
    print("Veuillez choisir un compte.")
    compte = input()
    while compte not in dict_utilisateur:
        print("Veuillez choisir un compte valide.")
        compte = input()
    return compte


def afficher_operation(operation):
    """
    None -> None
    Affiche une operation.
    """
    print(f"Date: {operation['date']}, Nom: {operation['nom']}, Montant: {operation['montant']}, Type: {operation['type']}, Statut: {operation['statut']}, Budget: {operation['budget']}")


def afficher_operations(compte):
    """
    None -> None
    Affiche les operations du compte.
    """
    for operation in dict_utilisateur[compte]["operations"]:
        afficher_operation(operation)


def valider_transaction(montant, compte):
    """
    float * str -> Bool
    Valide la transaction.
    """
    if montant > calculer_solde(compte):
        return False
    else:
        return True


def ajouter_operation(compte, date, nom, montant, type_ope, statut, budget):
    """
    str * str * str * float * str * str * str -> None
    Ajoute une operation au compte.
    """
    dict_utilisateur[compte]["operations"].append(
        {"date": date, "nom": nom, "montant": float(montant), "type": type_ope, "statut": statut, "budget": budget})
    print("Operation ajoutee: ", afficher_operation(
        dict_utilisateur[compte]["operations"][-1]))


def demande_ajout_operation():
    """
    None -> None
    Demande a l'utilisateur les informations pour ajouter une operation.
    """
    print("Veuillez choisir un compte parmi ceux-ci :")
    afficher_comptes()
    compte = choix_compte()
    date = datetime.now().strftime("%d/%m/%Y")
    nom = input("Nom: ")
    montant = float(input("Montant: "))
    type_ope = input("Type: ")
    statut = input("Statut: ")
    budget = input("Budget: ")
    if valider_transaction(montant, compte):
        ajouter_operation(compte, date, nom, montant, type_ope, statut, budget)
        print("Transaction validee.")
    else:
        print("Transaction invalide, solde insuffisant.")


def ajouter_compte(nom_compte):
    """
    None -> None
    Ajoute un compte a l'utilisateur.
    """
    dict_utilisateur[nom_compte] = {"budgets": [], "operations": []}


def supprimer_compte(nom_compte):
    """
    None -> None
    Supprime un compte a l'utilisateur.
    """
    del dict_utilisateur[nom_compte]


def virement(compte1, compte2, nom, montant, type_ope, statut, budget):
    """
    str * str * float -> None
    Effectue un virement entre deux comptes.
    """

    date = datetime.now().strftime("%d/%m/%Y")

    if valider_transaction(montant, compte1):
        ajouter_operation(compte1, date, nom, -montant,
                          type_ope, statut, budget)
        ajouter_operation(compte2, date, nom, montant,
                          type_ope, statut, budget)
        print("Transaction validee.")
    else:
        print("Transaction invalide, solde insuffisant.")


def demande_virement():
    """
    None -> None
    Demande a l'utilisateur les informations pour effectuer un virement.
    """
    print("Veuillez choisir un compte pour debiter parmi ceux-ci :")
    afficher_comptes()
    compte1 = choix_compte()
    print("Veuillez choisir un compte pour recevoir parmi ceux-ci :")
    afficher_comptes()
    compte2 = choix_compte()
    nom = input("Nom: ")
    montant = float(input("Montant: "))
    type_ope = "VIR"
    statut = "True"
    budget = input("Nom budget: ")
    virement(compte1, compte2, nom, montant, type_ope, statut, budget)

# gestion des budgets


def gestion_budgets():
    """
    None -> None
    Affiche une liste d’options réalisables sur les budgets.
    """
    print("-" * 50)
    print("Gestion des budgets")
    print("Solde dans le compte principal : " +
          str(calculer_solde(list(dict_utilisateur.keys())[0])) + " €")
    print("-" * 50)
    print("1. Afficher mes budgets")
    print("2. Afficher les opérations d'un budget")
    print("3. Ajouter un budget")
    print("4. Retour")
    print("-" * 50)
    # Vérification de la validité du choix
    choix = '0'
    while choix not in ["1", "2", "3", "4"]:
        choix = input("Que voulez-vous faire ? ")
        if choix == "1":
            # Afficher les budgets
            print("Voici vos budgets.")
            afficher_budgets()
            gestion_budgets()
        elif choix == "2":
            print("Veuillez choisir un budget parmi ceux-ci :")
            afficher_budgets()
            # Afficher les operations
            compte = choix_compte()
            budget = choix_budget(compte)
            operations_budget(budget, compte)
            gestion_budgets()
        elif choix == "3":
            # Ajouter un budget
            demande_ajout_budget()
            gestion_budgets()
        elif choix == "4":
            # Retour
            menu()
        else:  # Si le choix n'est pas valide
            print("Veuillez choisir une option valide.")
            choix = input("Que voulez-vous faire ? ")


def afficher_budget(budget):
    """
    str -> None
    Affiche le budget.
    """
    print(f"{budget['nom']}: {budget['montant']}")


def afficher_budgets():
    """
    None -> None
    Affiche les budgets de l'utilisateur.
    """
    for compte in list(dict_utilisateur.keys()):
        print("Compte: ", compte)
        for budget in dict_utilisateur[compte]["budgets"]:
            info_budget(budget, compte)


def operations_budget(budget, compte):
    """
    str -> None
    Affiche les operations du budget.
    """
    print("Voici les operations du budget: ", budget)
    for operation in dict_utilisateur[compte]["operations"]:
        if operation["budget"] == budget:
            afficher_operation(operation)


def somme_ope_budget(budget, compte):
    """
    str -> float
    Retourne la somme des operations du budget.
    """
    somme = 0
    for operation in dict_utilisateur[compte]["operations"]:
        if operation["budget"] == budget:
            somme += operation["montant"]
    return somme


def choix_budget(compte):
    """
    None -> str
    Demande a l'utilisateur de choisir un budget.
    """
    list_budgets = []
    for budget in dict_utilisateur[compte]["budgets"]:
        list_budgets.append(budget["nom"])
    budget = input("Nom budget: ")
    while budget not in list_budgets:
        print("Veuillez choisir un budget valide.")
        budget = input("Nom budget: ")
    return budget


def ajouter_budget(compte, nom, montant):
    """
    None -> None
    Ajoute un budget au compte.
    """
    dict_utilisateur[compte]["budgets"].append(
        {"nom": nom, "montant": float(montant)})


def demande_ajout_budget():
    """
    None -> None
    Demande a l'utilisateur les informations pour ajouter un budget.
    """
    afficher_comptes()
    compte = choix_compte()
    nom = input("Nom: ")
    montant = float(input("Montant: "))
    ajouter_budget(compte, nom, montant)
    print("Budget ajoute.")


def info_budget(budget, compte):
    """
    str -> None
    Affiche les informations du budget.
    """
    print(f"{budget['nom']}:")
    print(f"    Montant: {budget['montant']}")
    print(
        f"    Solde: { budget['montant'] + somme_ope_budget(budget['nom'], compte)}")


def main():
    print("Bienvenue a la banque")
    is_logged = False
    while is_logged is False:
        is_logged = identification()
    importer_donnees(
        "00000000")  # a changer pour l'identification
    menu()
    print("Au revoir")


if __name__ == "__main__":
    main()
