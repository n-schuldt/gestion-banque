import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import random
import datetime


def check_identification(numero_identification, mot_de_passe, fichier="ident.txt"):
    """
    str * str * str -> bool
    Verifie si le numero d'identification et le mot de passe
    sont corrects retourne True si le numero d'identification et le mot de passe
    sont corrects, False sinon
    """

    # numero_identification = "00000000"  # a enlever
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


class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.title("Banking App")

        self.frames = {}
        for FrameClass in (LoginPage, DashboardPage, Comptes, Budgets):
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(LoginPage)

    def show_frame(self, FrameClass):
        frame = self.frames[FrameClass]
        frame.tkraise()

    def set_username(self, username):
        dashboard_frame = self.frames[DashboardPage]
        dashboard_frame.set_username(username)

    def set_dict(self, identifiant):
        dashboard_frame = self.frames[DashboardPage]
        dict_utilisateur = importer_donnees(identifiant)

        dashboard_frame.set_dict(dict_utilisateur)
        comptes_frame = self.frames[Comptes]
        comptes_frame.set_dict(dict_utilisateur)

        budgets_frame = self.frames[Budgets]
        budgets_frame.set_dict(dict_utilisateur)


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        def on_click_login():
            numero_identification = username_entry.get()
            mot_de_passe = mot_de_passe_entry.get()
            if check_identification(numero_identification, mot_de_passe):
                self.master.set_username(numero_identification)
                self.master.set_dict(numero_identification)
                self.master.show_frame(DashboardPage)
                self.master.show_frame(DashboardPage)
            else:
                # afficher un message d'erreur
                tk.messagebox.showerror(
                    "Information", "Le numero d'identification ou le mot de passe est incorrect")
                print("Le numero d'identification ou le mot de passe est incorrect")

        username_label = tk.Label(self, text="Numero d'utilisateur:")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        username_entry = tk.Entry(self)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        mot_de_passe_label = tk.Label(self, text="Mot De Passe:")
        mot_de_passe = tk.StringVar()
        mot_de_passe_label.grid(row=2, column=1, padx=10, pady=10)

        # keypad
        mot_de_passe_entry = ttk.Entry(
            self, textvariable=mot_de_passe, state="disabled")
        mot_de_passe_entry.grid(row=2, column=2, padx=10, pady=10)
        mot_de_passe_grid = ttk.Frame(self)
        mot_de_passe_grid.grid(row=3, column=2, padx=10, pady=10)

        # buttons for keypad
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        # randomize nums list
        random.shuffle(nums)

        for i in range(9):
            ttk.Button(mot_de_passe_grid, text=nums[i], command=lambda n=nums[i]: mot_de_passe.set(
                mot_de_passe.get() + n)).grid(row=i//3+5, column=i % 3, padx=3, pady=3)

        ttk.Button(mot_de_passe_grid, text='Delete', command=lambda: mot_de_passe.set(
            mot_de_passe.get()[:-1])).grid(row=8, column=0, padx=3, pady=3)

        ttk.Button(mot_de_passe_grid, text=nums[9], command=lambda n=nums[9]: mot_de_passe.set(
            mot_de_passe.get() + n)).grid(row=8, column=1, padx=3, pady=3)

        ttk.Button(mot_de_passe_grid, text='Login',
                   command=on_click_login).grid(row=8, column=2, padx=0, pady=0)

    # def login(self):
    #     username = self.username_entry.get()
    #     password = self.password_entry.get()

    #     # Add your authentication check here
    #     if check_identification(username, password):
    #         self.master.set_username(username)
    #         self.master.set_dict(username)
    #         self.master.show_frame(DashboardPage)

    #     else:
    #         self.username_entry.delete(0, tk.END)
    #         self.password_entry.delete(0, tk.END)
    #         self.username_entry.insert(0, "Invalid username or password")


class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # dictionnaire des utilisateurs, ceci change une fois qu'on se connecte
        self.dict_utilisateur = {"Compte A": {
            "budgets": [{}], "operations": [{}]}}

        self.hello_label = tk.Label(self, text="")
        self.hello_label.grid(row=0, column=0, padx=5, pady=5)

       # nav bar
        self.navbar = tk.Frame(self)
        self.navbar.grid(row=1, column=0, padx=5, pady=5)

        self.comptes_button = tk.Button(self.navbar, text="Comptes",
                                        command=lambda: master.show_frame(Comptes))
        self.comptes_button.grid(row=0, column=0, padx=5, pady=5)

        self.budgets_button = tk.Button(self.navbar, text="Budgets",
                                        command=lambda: master.show_frame(Budgets))
        self.budgets_button.grid(row=0, column=1, padx=5, pady=5)

        self.deconnection_button = tk.Button(self.navbar, text="Deconnection",
                                             command=lambda: master.show_frame(LoginPage))
        self.deconnection_button.grid(row=0, column=2, padx=5, pady=5)

    def display_dict(self):
        print("Dict", self.dict_utilisateur)

    def set_username(self, username):
        self.hello_label.config(text=f"Hello {username}")

    def set_dict(self, dict_utilisateur):
        self.dict_utilisateur = dict_utilisateur


class Comptes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.dict_utilisateur = {"Compte A": {
            "budgets": [{}], "operations": [{"nom": "Operation 1", "montant": 100, "statut": "True", "date": "2020-01-01", "type": "Type", "budget": "Test BUD"}]}}

        # titre
        self.label = tk.Label(self, text="Gestion des comptes")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        # bouton pour revenir au dashboard
        self.button = tk.Button(self, text="Retour au dashboard",
                                command=lambda: master.show_frame(DashboardPage))
        self.button.grid(row=1, column=0, padx=5, pady=5)

        solde_compte = 0

        def actualiser_solde(soldeLabel):
            """
            Label -> None
            Actualise le solde du compte sélectionné.
            """
            solde_compte = self.calculer_solde(
                self.dict_utilisateur, self.compteCombo)
            actualiser_operations(
                tableau, self.dict_utilisateur, self.compteCombo)
            soldeLabel.config(text=f"Solde du compte : {solde_compte}")

        def actualiser_operations(tableau, dict_utilisateur, compteCombo):
            """
            Tableau * dict * str -> None
            Actualise les opérations du compte sélectionné.
            """
            operations_compte = dict_utilisateur[compteCombo.get(
            )]["operations"]
            tableau.delete(*tableau.get_children())
            for operation in operations_compte:
                tableau.insert("", "end", values=(operation["date"], operation["nom"], operation["montant"],
                                                  operation["type"], operation["statut"], operation["budget"]))

        def valider_transaction(montant):
            """
            float * str -> Bool
            Valide la transaction.
            """
            if self.calculer_solde(self.dict_utilisateur, self.compteCombo) + float(montant) < 0:
                return False
            else:
                return True

        # liste des comptes de l'utilisateur
        liste_comptes = list(self.dict_utilisateur.keys())

        # liste déroulante
        labelCompte = tk.Label(self, text="Veuillez choisir un compte :")
        labelCompte.grid(row=2, column=1, padx=10, pady=10)

        # liste déroulante
        self.compteCombo = ttk.Combobox(
            self, values=list(self.dict_utilisateur.keys()))
        self.compteCombo.grid(row=3, column=1, padx=8, pady=8)

        # valeur par défaut de la liste déroulante
        self.compteCombo.current(0)

        # actualisation du solde du compte choisi
        self.compteCombo.bind("<<ComboboxSelected>>",
                              lambda event: actualiser_solde(self.soldeLabel))

        # calcul du solde du compte choisi

        operations_compte = self.dict_utilisateur[self.compteCombo.get(
        )]["operations"]

        # affichage du solde du compte
        self.soldeLabel = tk.Label(
            self, text=f"Solde du compte : {solde_compte}")
        self.soldeLabel.grid(row=4, column=1, padx=10, pady=10)

        # affichage des données du compte sous forme de tableau
        # Treeview (tableau)

        self.tableau = ttk.Treeview(self, columns=(
            "Date", "Nom", "Montant", "Type", "Statut", "Budget"))
        tableau = self.tableau
        tableau.heading("Date", text="Date")
        tableau.heading("Nom", text="Nom")
        tableau.heading("Montant", text="Montant")
        tableau.heading("Type", text="Type")
        tableau.heading("Statut", text="Statut")
        tableau.heading("Budget", text="Budget")

        # Sans la ligne suivante, il y aurait une colonne vide à gauche

        tableau['show'] = 'headings'

        # Ajout des données

        for operation in self.dict_utilisateur[self.compteCombo.get(
        )]["operations"]:
            tableau.insert("", "end", values=(
                operation["date"], operation["nom"], operation["montant"], operation["type"], operation["statut"], operation["budget"]))
        tableau.grid(row=5, column=1, padx=1, pady=1, )

    def calculer_solde(self, dict_utilisateur, compteCombo):
        """Dict, Str -> Float
        Calcule le solde du compte."""
        solde = 0
        for operation in dict_utilisateur[compteCombo.get()]["operations"]:
            if operation["statut"] == "True":
                solde += operation["montant"]
        return solde

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur

        self.compteCombo.config(values=list(self.dict_utilisateur.keys()))
        for operation in self.dict_utilisateur[self.compteCombo.get(
        )]["operations"]:
            self.tableau.insert("", "end", values=(
                operation["date"], operation["nom"], operation["montant"], operation["type"], operation["statut"], operation["budget"]))
        self.tableau.grid(row=5, column=1, padx=1, pady=1, )

        self.soldeLabel.config(
            text=f"Solde du compte : {self.calculer_solde(self.dict_utilisateur, self.compteCombo)}")


class Budgets(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.dict_utilisateur = {"Compte A": {
            "budgets": [{}], "operations": [{}]}}

        # titre
        self.label = tk.Label(self, text="Gestion des budgets")
        self.label.pack(padx=5, pady=5)

        # bouton pour revenir au dashboard
        self.button = tk.Button(self, text="Retour au dashboard",
                                command=lambda: master.show_frame(DashboardPage))
        self.button.pack(padx=5, pady=5)

        # liste des budgets
        self.liste_budgets = tk.Listbox(self)
        self.liste_budgets.pack(padx=5, pady=5)

        # remplissage de la liste des budgets
        for compte in self.dict_utilisateur:
            for budget in self.dict_utilisateur[compte]["budgets"]:
                self.liste_budgets.insert(tk.END, budget)

    def set_dict(self, dict_utilisateur):
        self.dict_utilisateur = dict_utilisateur
        # remplissage de la liste des budgets
        self.liste_budgets.delete(0, tk.END)
        for compte in self.dict_utilisateur:
            for budget in self.dict_utilisateur[compte]["budgets"]:
                self.liste_budgets.insert(tk.END, budget)


if __name__ == "__main__":
    app = BankingApp()
    app.columnconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)
    app.mainloop()
