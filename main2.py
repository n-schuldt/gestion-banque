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
                                        command=lambda: master.show_frame(Budget))
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

        self.dict_utilisateur = {}

        tk.Frame.__init__(self,  master)
        label = ttk.Label(
            self, text="Afficher les opérations d'un budget", font=LARGEFONT)
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

        listeCombo1 = ttk.Combobox(self, values=["Compte A", "Compte B"])
        listeCombo1.current(None)
        listeCombo1.grid(row=1, column=4, padx=0, pady=5)

        listeCombo2 = ttk.Combobox(
            self, values=["Sorties", "Divers", "Cinema", "Alimentation"])
        listeCombo2.current(None)
        listeCombo2.grid(row=2, column=4, padx=0, pady=5)

        listeCombo3 = ttk.Combobox(self, values=["Janvier", "février", "mars", "avril",
                                   "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"])
        listeCombo3.current(None)
        listeCombo3.grid(row=3, column=4, padx=0, pady=5)

        # Créer un widget Treeview
        tableau = ttk.Treeview(self, columns=('Libellé', 'Montant', 'Type'))

        # Ajouter les colonnes
        tableau.heading('#0', text='Date')
        tableau.heading('Libellé', text='Libellé')
        tableau.heading('Montant', text='Montant')
        tableau.heading('Type', text='Type')

        # Ajouter des données a partir du dictionnaire
        for key, value in self.dict_utilisateur.items():
            tableau.insert(parent='', index='end', iid=1, text=(
                key), values=(value[0], value[1], value[2]))

        tableau.grid(row=4, column=4, padx=30, pady=30)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur


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
        tk.Frame.__init__(self,  master)

        self.dict_utilisateur = {}

        label = ttk.Label(
            self, text="Entrez les infos du nouveau Budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Comptes",
                             command=lambda:  master.show_frame(Comptes))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda:  master.show_frame(LoginPage))

        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Ajouter ou Modifier",
                             command=lambda:  master.show_frame(AjoutBud))
        button3.grid(row=2, column=1, padx=10, pady=10)

        def recuperer_texte():
            # Récupérer le texte entré par l'utilisateur
            texte1 = entree1.get()
            texte2 = entree2.get()
            texte3 = entree3.get()
            # Afficher le texte dans la console
            print(texte1, texte2, texte3)

        # Créer un champ d'entrée
        entree1 = tk.Entry(self, text="Nom du budget")
        etiquette1 = tk.Label(self, text='Nom du budget')
        etiquette1.grid(row=1, column=2, padx=5, pady=5)
        entree1.grid(row=2, column=2, padx=5, pady=5)
        entree2 = tk.Entry(self, text="Montant du budget")
        etiquette2 = tk.Label(self, text='Montant du budget')
        etiquette2.grid(row=3, column=2, padx=5, pady=5)
        entree2.grid(row=4, column=2, padx=5, pady=5)
        entree3 = tk.Entry(self, text="Solde du budget")
        etiquette3 = tk.Label(self, text='Solde du budget')
        etiquette3.grid(row=5, column=2, padx=5, pady=5)
        entree3.grid(row=6, column=2, padx=5, pady=5)

        # Créer un bouton pour récupérer le texte
        bouton = tk.Button(self, text='terminer',
                           height=3,
                           width=10,
                           command=recuperer_texte)
        bouton.grid(row=3, column=3, padx=10, pady=10)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur


class ModiffBud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self,  master)

        self.dict_utilisateur = {}

        label = ttk.Label(
            self, text="Quel budget voulez vous modifier?", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Comptes",
                             command=lambda:  master.show_frame(Comptes))

        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Déconnexion",
                             command=lambda:  master.show_frame(LoginPage))

        button2.grid(row=3, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Ajouter ou Modifier",
                             command=lambda:  master.show_frame(AjoutBud))
        button3.grid(row=2, column=1, padx=10, pady=10)

        listeCombo = ttk.Combobox(
            self, values=["Sorties", "Divers", "Cinema", "Alimentation"], height=5, width=10,)
        listeCombo.grid(row=1, column=2, padx=10, pady=10)

        def recuperer_texte():
            # Récupérer le texte entré par l'utilisateur
            texte1 = entree1.get()
            texte2 = entree2.get()
            texte3 = entree3.get()
            # Afficher le texte dans la console
            print(texte1, texte2, texte3)

        entree1 = tk.Entry(self, text="Nouveau Nom du Budget")
        etiquette1 = tk.Label(self, text='Nouveau Nom du Budget')
        etiquette1.grid(row=1, column=3, padx=5, pady=5)
        entree1.grid(row=2, column=3, padx=5, pady=5)
        entree2 = tk.Entry(self, text="Nouveau Montant du budget")
        etiquette2 = tk.Label(self, text='Nouveau Montant du budget')
        etiquette2.grid(row=3, column=3, padx=5, pady=5)
        entree2.grid(row=4, column=3, padx=5, pady=5)
        entree3 = tk.Entry(self, text="Nouveau Solde du budget")
        etiquette3 = tk.Label(self, text='Nouveau Solde du budget')
        etiquette3.grid(row=5, column=3, padx=5, pady=5)
        entree3.grid(row=6, column=3, padx=5, pady=5)

        bouton = tk.Button(self, text='terminer',
                           height=3,
                           width=10,
                           command=recuperer_texte)
        bouton.grid(row=3, column=4, padx=1, pady=1)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur


if __name__ == "__main__":
    app = BankingApp()
    app.columnconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)
    app.mainloop()
