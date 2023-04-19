import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import random
import datetime

LARGEFONT = ("Verdana", 35)


def check_identification(numero_identification, mot_de_passe, fichier="ident.txt"):
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


def importer_donnees(identifiant_utilisateur):
    """
    None -> dict
    Lit le fichier et retourne le contenu en dict
    """
    global dict_utilisateur
    dict_utilisateur = {}
    with open(f"00000000.txt") as f:  # a enlever
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


def calculer_solde(compte):
    solde = 0
    for operation in dict_utilisateur[compte]["operations"]:
        if operation["statut"] == "True":
            solde += operation["montant"]
    return solde


class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.title("Banking App")

        self.frames = {}
        for FrameClass in (LoginPage, DashboardPage, Comptes, Budget, AffichBud, AffichOpe, AjoutBud, ModiffBud, NewBud):
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
        """
        str -> None
        Met a jour le dictionnaire de l'utilisateur avec les donnees du fichier
        dans tous les frames
        """

        dashboard_frame = self.frames[DashboardPage]
        dict_utilisateur = importer_donnees(identifiant)

        dashboard_frame.set_dict(dict_utilisateur)
        comptes_frame = self.frames[Comptes]
        comptes_frame.set_dict(dict_utilisateur)

        budgets_frame = self.frames[Budget]
        budgets_frame.set_dict(dict_utilisateur)

        affichbud_frame = self.frames[AffichBud]
        affichbud_frame.set_dict(dict_utilisateur)

        affichope_frame = self.frames[AffichOpe]
        affichope_frame.set_dict(dict_utilisateur)

        ajoutbud_frame = self.frames[AjoutBud]
        ajoutbud_frame.set_dict(dict_utilisateur)

        modiffbud_frame = self.frames[ModiffBud]
        modiffbud_frame.set_dict(dict_utilisateur)


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


# Class pour la fenêtre Menu :


class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self,  master)

        # Fonctions pour calculer le solde
        budget = 1000  # Budget a modifier

        # Créer des boutons ici (FRAME LEFT)
        self.button = tk.Button(self, text="GESTION BUDGET", command=lambda: self.master.show_frame(
            Budget), font=('DejaVu Sans', 15), width=20, height=5)
        self.button.grid(row=1, column=0, padx=5, pady=5)

        self.button2 = tk.Button(self, text="GESTION COMPTE", command=lambda: self.master.show_frame(
            Comptes), font=('DejaVu Sans', 15), width=20, height=5)
        self.button2.grid(row=2, column=0, padx=5, pady=5)

        self.button3 = tk.Button(self, text="LOGOUT", command=self.logout, font=(
            'DejaVu Sans', 15), width=10, height=2,  bg="red3", fg="white", activebackground="red3", activeforeground="white")
        self.button3.grid(row=3, column=0, padx=5, pady=5)

        # Créer des label ici (FRAME CENTER)
        self.budget_label = tk.Label(
            self, text="Solde : ", font=('DejaVu Sans', 40), fg="#675A8B")
        self.budget_label.grid(row=2, column=1, padx=5, pady=5)

        self.name_label = tk.Label(self, text="", font=('DejaVu Sans', 30))
        self.name_label.grid(row=1, column=1, padx=5, pady=5)

        # Créer des boutons ici (FRAME RIGHT)
        self.calc_button = tk.Button(self, text="CALCULATRICE", command=self.open_calculator, font=(
            'DejaVu Sans', 15), width=20, height=2,  bg="green", fg="black", activebackground="green", activeforeground="black")
        self.calc_button.grid(row=1, column=2, padx=5, pady=5)

        self.estate_button = tk.Button(self, text="SIMULATEUR", command=self.real_estate_simulator, font=(
            'DejaVu Sans', 15), width=20, height=2,  bg="green", fg="black", activebackground="green", activeforeground="black")
        self.estate_button.grid(row=2, column=2, padx=5, pady=5)

        # Afficher le budget dans le label

        self.budget_label.config(
            text="Votre solde est de\n+{}€".format(budget))

    def set_username(self, username):
        self.name_label.config(text="Bienvenue {}".format(username))

    def display_dict(self):
        print("Dict", self.dict_utilisateur)

    def set_dict(self, dict_utilisateur):
        self.dict_utilisateur = dict_utilisateur

    def logout(self):
        self.master.show_frame(LoginPage)

    # nouvelle fenêtre pour la gestion du budget

    # def open_new_window(self):
    #     """Ouvre une nouvelle fenêtre (Gestion Budget)"""
    #     # Cée une nouvelle fenêtre ici
    #     asset_manager_window = tk.Toplevel(self.master)
    #     asset_manager_window.title("Gestion Budget")

    #     # A activer quand la classe GestionBudget sera créée
    #     window = Comptes(asset_manager_window)
    #     window.pack()

    # # nouvelle fenêtre pour la gestion du compte
    # def open_new_window2(self):
    #     """Ouvre une nouvelle fenêtre (Gestion Compte))"""
    #     # Crée une nouvelle fenêtre ici
    #     account_manager_window = tk.Toplevel(self.master)
    #     account_manager_window.title("Gestion Compte")

    #     # A activer quand la classe GestionCompte sera créée
    #     window = Budget(account_manager_window)
    #     window.pack()

    # nouvelle fenêtre pour le simulateur d'emprunt

    def real_estate_simulator(self):
        """Ouvre une nouvelle fenêtre (Emprunt)"""
        # Crée une nouvelle fenêtre ici
        real_estate_window = tk.Toplevel(self.master)
        real_estate_window.title("Emprunt")
        # Créer des widgets pour la nouvelle fenêtre ici
        loan = RealEstateSimulator(real_estate_window)
        loan.pack()

    # nouvelle fenêtre pour la calculatrice
    def open_calculator(self):
        """Ouvre une nouvelle fenêtre avec une calculatrice"""
        # Crée une nouvelle fenêtre ici
        calculator_window = tk.Toplevel(self.master)
        calculator_window.title("Calculatrice")
        # Créer des widgets pour la nouvelle fenêtre ici
        calculator = Calculator(calculator_window)
        calculator.pack()


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


class Budget(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.dict_utilisateur = {
            "Compte A": {
                "budgets": [
                    {"nom": "sorties", "montant": 300.0},
                    {"nom": "divers", "montant": 1000.0}
                ],
                "operations": [
                    {"date": "01/01/2022", "nom": "cinema", "montant": 18.5,
                     "type": "CB", "statut": "False", "budget": "sorties"}
                ]
            },
            "Compte B": {
                "budgets": [
                    {"nom": "alimentation", "montant": 500.0},
                    {"nom": "alimentation 2", "montant": 400.0}
                ],
                "operations": [
                    {"date": "06/01/2022", "nom": "galette", "montant": 10.54,
                     "type": "CB", "statut": "True", "budget": "alimentation"}
                ]
            }
        }

        tk.Frame.__init__(self,  master)
        label = ttk.Label(self, text="Budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Retour",
                             command=lambda:  master.show_frame(DashboardPage))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # putting the button in its place by
        ButAffBud = tk.Button(self,
                              text="Afficher mes budgets",
                              command=lambda:  master.show_frame(AffichBud),
                              height=3,
                              width=30)

        ButAffBud.grid(row=1, column=4, padx=10, pady=10)

        ButAffOpe = tk.Button(self,
                              text="Afficher les opérations d'un budget",
                              command=lambda:  master.show_frame(AffichOpe),
                              height=3,
                              width=30)

        ButAffOpe.grid(row=2, column=4, padx=30, pady=30)

        ButAjouBud = tk.Button(self,
                               text="Ajouter ou modifier un budget",
                               command=lambda:  master.show_frame(AjoutBud),
                               height=3,
                               width=30)

        ButAjouBud.grid(row=3, column=4, padx=30, pady=30)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur


class AffichBud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self,  master)

        self.dict_utilisateur = {}

        label = ttk.Label(self, text="Afficher mes budgets", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Comptes",
                             command=lambda:  master.show_frame(Comptes))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda:  master.show_frame(LoginPage))
        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Budget",
                             command=lambda:  master.show_frame(Budget))

        # putting the button in its place by
        # using grid
        button3.grid(row=2, column=1, padx=10, pady=10)
        # Créer un widget Treeview
        self.tableau = ttk.Treeview(
            self, columns=('Budget', 'Montant', 'Solde'))
        tableau = self.tableau

        # Ajouter les colonnes
        tableau.heading('#0', text='Compte')
        tableau.heading('Budget', text='Budget')
        tableau.heading('Montant', text='Montant')
        tableau.heading('Solde', text='Solde')

        # Afficher le tableau
        tableau.grid(row=1, column=4, padx=10, pady=10)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        print("set_dict", dict_utilisateur)
        self.dict_utilisateur = dict_utilisateur

       # Actualiser le tableau
        self.tableau.delete(*self.tableau.get_children())
        for compte, dict_compte in self.dict_utilisateur.items():
            for budget in dict_compte["budgets"]:
                self.tableau.insert(
                    '', 'end', text=compte, values=(budget["nom"],
                                                    budget["montant"],
                                                    budget["montant"]))

        self.tableau.grid(row=1, column=4, padx=10, pady=10)


class AffichOpe(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self, master)

        self.dict_utilisateur = {
            "Compte A": {
                "budgets": [
                    {"nom": "sorties", "montant": 300.0},
                    {"nom": "divers", "montant": 1000.0}
                ],
                "operations": [
                    {"date": "01/01/2022", "nom": "cinema", "montant": 18.5,
                     "type": "CB", "statut": "False", "budget": "sorties"},
                    {"date": "12/01/2022", "nom": "anniversaire", "montant": 50.0,
                     "type": "VIR", "statut": "True", "budget": "divers"},
                    {"date": "15/03/2023", "nom": "test", "montant": -10.0,
                     "type": "CB", "statut": "False", "budget": "sorties"}
                ]
            },
            "Compte B": {
                "budgets": [
                    {"nom": "alimentation", "montant": 500.0},
                    {"nom": "divers", "montant": 400.0}
                ],
                "operations": [
                    {"date": "06/01/2022", "nom": "galette", "montant": 10.54,
                     "type": "CB", "statut": "True", "budget": "alimentation"}
                ]
            },
            "Compte C": {
                "budgets": [
                    {"nom": "asfsadfsdf", "montant": 500.0},
                    {"nom": "bbbbbbbb", "montant": 400.0}
                ],
                "operations": [
                    {"date": "06/01/2022", "nom": "galette", "montant": 10.54,
                     "type": "CB", "statut": "True", "budget": "alimentation"}
                ]
            }
        }

        label = ttk.Label(
            self, text="Afficher les opérations d'un budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Comptes",
                             command=lambda: master.show_frame(Comptes))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda: master.show_frame(LoginPage))
        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Budget",
                             command=lambda: master.show_frame(Budget))

        # putting the button in its place by
        # using grid
        button3.grid(row=2, column=1, padx=10, pady=10)

        comptes = list(self.dict_utilisateur.keys())

        listeCombo1 = ttk.Combobox(self, values=["-"] + comptes)
        listeCombo1.current(0)
        listeCombo1.grid(row=1, column=4, padx=0, pady=5)

        listeComboBud = ttk.Combobox(self, values=list(
            self.dict_utilisateur.values()), height=5, width=10,)
        listeComboBud.grid(row=1, column=2, padx=10, pady=10)

        budgets = ['-']
        for compte in self.dict_utilisateur.values():
            for b in compte['budgets']:
                budgets.append(b['nom'])
        print(budgets)

        listeComboBud.configure(values=budgets, height=5)
        listeComboBud.grid(row=2, column=4, padx=10, pady=5)

        listeCombo3 = ttk.Combobox(self, values=[
                                   "-", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        listeCombo3.current(0)
        listeCombo3.grid(row=3, column=4, padx=0, pady=5)

        listeCombo4 = ttk.Combobox(
            self, values=["-", "2019", "2020", "2021", "2022", "2023"])
        listeCombo4.current(0)
        listeCombo4.grid(row=1, column=3, padx=0, pady=5)

        # Créer un widget Treeview
        tableau = ttk.Treeview(self, columns=('Libellé', 'Montant', 'Type'))

        # Ajouter les colonnes
        tableau.heading('#0', text='Date')
        tableau.heading('Libellé', text='Libellé')
        tableau.heading('Montant', text='Montant')
        tableau.heading('Type', text='Type')

        # Parcourir les données du dictionnaire dict_utilisateur
        for compte, infos in self.dict_utilisateur.items():
            for operation in infos["operations"]:
                date = operation["date"]
                libelle = operation["nom"]
                montant = operation["montant"]
                type_operation = operation["type"]
                # Insérer les données dans le tableau
                tableau.insert(parent='', index='end', text=date,
                               values=(libelle, montant, type_operation))

        # Afficher le tableau
        tableau.grid(row=4, column=4, padx=30, pady=30)
        # Définir une fonction de filtrage des opérations

        def filtrer_operations():
            # Récupérer les valeurs sélectionnées dans les combobox
            compte_selec = listeCombo1.get()
            budget_selec = listeCombo2.get()
            mois_selec = listeCombo3.get()
            year_selec = listeCombo4.get()

            print(compte_selec, budget_selec, mois_selec, year_selec)

            # Effacer les données actuellement affichées dans le tableau
            tableau.delete(*tableau.get_children())

            # Parcourir les données du dictionnaire dict_utilisateur, filtrer et insérer les données dans le tableau
            # Si la valeur sélectionnée dans la combobox est "-" (tous), on affiche toutes les données
            for compte, infos in self.dict_utilisateur.items():
                if compte_selec == "-" or compte_selec == compte:
                    for operation in infos["operations"]:
                        date = operation["date"]
                        libelle = operation["nom"]
                        montant = operation["montant"]
                        type_operation = operation["type"]
                        budget = operation["budget"]
                        if (budget_selec == "-" or budget_selec == budget) and (mois_selec == "-" or mois_selec == date[3:5]) and (year_selec == "-" or year_selec == date[6:]):
                            tableau.insert(parent='', index='end', text=date,
                                           values=(libelle, montant, type_operation))

        # Modifier les commandes des combobox pour appeler la fonction de filtrage
        listeCombo1 = ttk.Combobox(
            self, values=["-"] + comptes, state="readonly")
        listeCombo1.current(0)
        listeCombo1.grid(row=1, column=4, padx=0, pady=5)
        listeCombo1.bind("<<ComboboxSelected>>",
                         lambda event: filtrer_operations())

        listeCombo2 = ttk.Combobox(self, values=(["-"] + list(
            self.dict_utilisateur.values())), height=5, width=10, state="readonly")
        listeCombo2.configure(values=budgets, height=10)
        listeCombo2.current(0)
        listeCombo2.grid(row=2, column=4, padx=0, pady=5)
        listeCombo2.bind("<<ComboboxSelected>>",
                         lambda event: filtrer_operations())

        listeCombo3 = ttk.Combobox(self, values=[
                                   "-", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], state="readonly")
        listeCombo3.current(0)
        listeCombo3.grid(row=3, column=4, padx=0, pady=5)
        listeCombo3.bind("<<ComboboxSelected>>",
                         lambda event: filtrer_operations())

        listeCombo4 = ttk.Combobox(
            self, values=["-", "2019", "2020", "2021", "2022", "2023"], state="readonly")
        listeCombo4.current(0)
        listeCombo4.grid(row=1, column=3, padx=0, pady=5)
        listeCombo4.bind("<<ComboboxSelected>>",
                         lambda event: filtrer_operations())

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        print("set_dict appelé", dict_utilisateur)
        self.dict_utilisateur = dict_utilisateur

        # # Mettre à jour les combobox
        # self.listeCombo1.configure(
        #     values=["-"] + list(dict_utilisateur.keys()))
        # self.listeCombo2.configure(
        #     values=["-"] + list(dict_utilisateur.values()))

        # # Mettre à jour le tableau
        # self.filtrer_operations()


class AjoutBud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self, master)

        self.dict_utilisateur = {}

        label = ttk.Label(
            self, text="Ajouter ou Modifier un budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Comptes",
                             command=lambda:  master.show_frame(Comptes))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda:  master.show_frame(LoginPage))

        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Budget",
                             command=lambda:  master.show_frame(Budget))

        button3.grid(row=2, column=1, padx=10, pady=10)

        AjouteBud = tk.Button(self,
                              text="Nouveau Budget",
                              command=lambda:  master.show_frame(NewBud),
                              height=3,
                              width=30)
        AjouteBud.grid(row=3, column=4, padx=10, pady=10)

        ModifBud = tk.Button(self,
                             text="Modifier un Budget",
                             command=lambda:  master.show_frame(ModiffBud),
                             height=3,
                             width=30)
        ModifBud.grid(row=4, column=4, padx=30, pady=30)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur


class NewBud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self, master)

        self.dict_utilisateur = {}

        label = ttk.Label(
            self, text="Entrez les infos du nouveau Budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Comptes",
                             command=lambda: master.show_frame(Comptes))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda: master.show_frame(LoginPage))

        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Ajouter ou Modifier",
                             command=lambda: master.show_frame(AjoutBud))
        button3.grid(row=2, column=1, padx=10, pady=10)

        def recuperer_texte():
            # Récupérer le texte entré par l'utilisateur
            texte1 = entree1.get()
            texte2 = entree2.get()
            # Récupérer le choix du compte de l'utilisateur
            compte = var_compte.get()
            # Appeler la fonction pour ajouter le budget
            ajouter_budget(compte, texte1, texte2)
            # Afficher le texte dans la console
            print(texte1, texte2, compte)

        # Créer un champ d'entrée
        entree1 = tk.Entry(self, text="Nom du budget")
        etiquette1 = tk.Label(self, text='Nom du budget')
        etiquette1.grid(row=1, column=2, padx=5, pady=5)
        entree1.grid(row=2, column=2, padx=5, pady=5)
        entree2 = tk.Entry(self, text="Montant du budget")
        etiquette2 = tk.Label(self, text='Montant du budget')
        etiquette2.grid(row=3, column=2, padx=5, pady=5)
        entree2.grid(row=4, column=2, padx=5, pady=5)

        # Créer une variable pour le choix du compte
        var_compte = tk.StringVar(self)
        var_compte.set("Compte A")  # Définir la valeur par défaut
        # Créer un menu déroulant pour choisir le compte
        menu_compte = tk.OptionMenu(self, var_compte, "Compte A", "Compte B")
        etiquette4 = tk.Label(self, text='Compte')
        etiquette4.grid(row=7, column=2, padx=5, pady=5)
        menu_compte.grid(row=8, column=2, padx=5, pady=5)

        # Créer un bouton pour récupérer le texte
        bouton = tk.Button(self, text='terminer',
                           height=3,
                           width=10,
                           command=recuperer_texte)
        bouton.grid(row=3, column=4, padx=10, pady=10)

        def ajouter_budget(compte, nom_budget, montant_budget):

            # Vérifier si le compte existe dans le dictionnaire de l'utilisateur
            if compte in dict_utilisateur:
                # Ajouter le nouveau budget au compte existant
                nouveau_budget = {"nom": nom_budget,
                                  "montant": float(montant_budget)}
                dict_utilisateur[compte]["budgets"].append(nouveau_budget)

            # Afficher le dictionnaire mis à jour dans la console
            print(dict_utilisateur)

            # Afficher un message de succès à l'utilisateur
            messagebox.showinfo("Le nouveau budget a été ajouté avec succès.")

            # Réinitialiser les champs d'entrée
            entree1.delete(0, tk.END)
            entree2.delete(0, tk.END)
            var_compte.set("Compte A")


class ModiffBud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self, master)

        self.dict_utilisateur = {
            "Compte A": {
                "budgets": [
                    {"nom": "sorties", "montant": 300.0},
                    {"nom": "divers", "montant": 1000.0}
                ],
                "operations": [
                    {"date": "01/01/2022", "nom": "cinema", "montant": 18.5,
                     "type": "CB", "statut": "False", "budget": "sorties"}
                ]
            },
            "Compte B": {
                "budgets": [
                    {"nom": "alimentation", "montant": 500.0},
                    {"nom": "alimentation 2", "montant": 400.0}
                ],
                "operations": [
                    {"date": "06/01/2022", "nom": "galette", "montant": 10.54,
                     "type": "CB", "statut": "True", "budget": "alimentation"}
                ]
            }
        }

        label = ttk.Label(
            self, text="Quel budget voulez vous modifier?", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Comptes",
                             command=lambda: master.show_frame(Comptes))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda: master.show_frame(LoginPage))

        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Ajouter ou Modifier",
                             command=lambda: master.show_frame(AjoutBud))
        button3.grid(row=2, column=1, padx=10, pady=10)

        listeCombo = ttk.Combobox(self, values=list(
            self.dict_utilisateur.values()), height=5, width=10,)
        listeCombo.grid(row=1, column=2, padx=10, pady=10)

        budgets = []
        for compte in self.dict_utilisateur.values():
            for b in compte['budgets']:
                budgets.append(b['nom'])
        listeCombo['values'] = budgets

        def recuperer_texte():
            # Récupérer le nom du budget sélectionné dans la combobox
            budget = listeCombo.get()
            # Récupérer le texte entré par l'utilisateur dans les champs d'entrée
            nouveau_nom = entree1.get()
            nouveau_montant = float(entree2.get())

            # Modifier le nom et le montant du budget dans le dictionnaire
            for compte in dict_utilisateur.values():
                for b in compte['budgets']:
                    if b['nom'] == budget:
                        b['nom'] = nouveau_nom
                        b['montant'] = nouveau_montant

            # Afficher le texte dans la console
            print("Nouveau nom du budget:", nouveau_nom)
            print("Nouveau montant du budget:", nouveau_montant)
            print(dict_utilisateur)

        entree1 = tk.Entry(self, text="Nouveau Nom du Budget")
        etiquette1 = tk.Label(self, text='Nouveau Nom du Budget')
        etiquette1.grid(row=1, column=3, padx=5, pady=5)
        entree1.grid(row=2, column=3, padx=5, pady=5)
        entree2 = tk.Entry(self, text="Nouveau Montant du budget")
        etiquette2 = tk.Label(self, text='Nouveau Montant du budget')
        etiquette2.grid(row=3, column=3, padx=5, pady=5)
        entree2.grid(row=4, column=3, padx=5, pady=5)

        bouton = tk.Button(self, text='terminer',
                           height=3,
                           width=10,
                           command=recuperer_texte)
        bouton.grid(row=3, column=4, padx=1, pady=1)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur


class Calculator(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # AFFICHAGE
        self.display_value = tk.StringVar()
        self.display_value.set('0')
        # Empêche le redimensionnement de la fenêtre
        master.resizable(width=False, height=False)
        # Création du widget d'affichage
        display = tk.Entry(self, textvariable=self.display_value,
                           justify='right', font=('DejaVu Sans', 20))
        display.grid(row=0, column=0, columnspan=4)

        # Disposition des boutons
        button_list = [
            '7',  '8',  '9',  '/',
            '4',  '5',  '6',  '*',
            '1',  '2',  '3',  '-',
            '0',  'C',  '=', '+'
        ]

        # Création des boutons et ajout à la calculatrice
        r = 1
        c = 0
        for b in button_list:
            tk.Button(self, text=b, width=5, height=2, font=('DejaVu Sans', 20),
                      command=lambda x=b: self.button_press(x)).grid(row=r, column=c)
            c += 1
            if c > 3:
                c = 0
                r += 1

        # initialisation des variables pour le calcul
        self.current_value = 0
        self.operator = ''

    def button_press(self, value):
        if value == 'C':
            self.display_value.set('0')
        elif value in ['+', '-', '*', '/']:
            self.current_value = float(self.display_value.get())
            self.operator = value
            self.display_value.set('')
        elif value == '=':
            if self.operator == '+':
                self.display_value.set(
                    str(self.current_value + float(self.display_value.get())))
            elif self.operator == '-':
                self.display_value.set(
                    str(self.current_value - float(self.display_value.get())))
            elif self.operator == '*':
                self.display_value.set(
                    str(self.current_value * float(self.display_value.get())))
            elif self.operator == '/':
                self.display_value.set(
                    str(self.current_value / float(self.display_value.get())))
        else:
            if self.display_value.get() == '0':
                self.display_value.set(value)
            else:
                self.display_value.set(self.display_value.get() + value)

# Class simulateur de crédit :


class RealEstateSimulator(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title("Simulateur de crédit immobilier")

        # les variables de contrôle
        self.loan_amount_var = tk.StringVar()
        self.interest_rate_var = tk.StringVar()
        self.loan_term_var = tk.StringVar()

        # les champs de sortie
        self.output_label = ttk.Label(self.master, text="")
        self.output_label.grid(row=3, column=0, columnspan=2)

        # les champs d'entrée
        loan_amount_label = ttk.Label(self.master, text="Emprunt (€):")
        loan_amount_label.grid(row=0, column=0, padx=5, pady=5)
        loan_amount_entry = ttk.Entry(
            self.master, textvariable=self.loan_amount_var)
        loan_amount_entry.grid(row=0, column=1, padx=5, pady=5)

        interest_rate_label = ttk.Label(
            self.master, text="Taux d'intérêt (%):")
        interest_rate_label.grid(row=1, column=0, padx=5, pady=5)
        interest_rate_entry = ttk.Entry(
            self.master, textvariable=self.interest_rate_var)
        interest_rate_entry.grid(row=1, column=1, padx=5, pady=5)

        loan_term_label = ttk.Label(self.master, text="Durée (ans)")
        loan_term_label.grid(row=2, column=0, padx=5, pady=5)
        loan_term_entry = ttk.Entry(
            self.master, textvariable=self.loan_term_var)
        loan_term_entry.grid(row=2, column=1, padx=5, pady=5)

        # Define calculate button
        calculate_button = ttk.Button(
            self.master, text="Calculer", command=self.calculate)
        calculate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def calculate(self):
        """Calculer le paiement mensuel d'un prêt immobilier"""

        # récupérer les valeurs des champs d'entrée
        try:
            loan_amount = float(self.loan_amount_var.get())
            interest_rate = float(self.interest_rate_var.get())
            loan_term = float(self.loan_term_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalide", "Veuillez entrer des valeurs numériques")
            return

        # calculer le paiement mensuel
        # convertir le taux d'intérêt en pourcentage en taux mensuel
        monthly_interest_rate = interest_rate / 1200
        num_payments = loan_term * 12  # convertir les années en mois
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (
            1 + monthly_interest_rate)**(-num_payments))  # formule de calcul du paiement mensuel

        # afficher le résultat
        # afficher le résultat avec 2 chiffre après la virgule
        self.output_label.configure(
            text=f"Vous devrez payer {monthly_payment:.2f}€ par mois.")


if __name__ == "__main__":
    app = BankingApp()
    app.columnconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)
    app.mainloop()
