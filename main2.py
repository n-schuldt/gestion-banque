import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import random


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

        self.geometry("800x600")
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
            "budgets": [{}], "operations": [{}]}}

        # titre
        self.label = tk.Label(self, text="Gestion des comptes")
        self.label.pack(padx=5, pady=5)

        # bouton pour revenir au dashboard
        self.button = tk.Button(self, text="Retour au dashboard",
                                command=lambda: master.show_frame(DashboardPage))
        self.button.pack(padx=5, pady=5)

        # liste des comptes
        self.liste_comptes = tk.Listbox(self)
        self.liste_comptes.pack(padx=5, pady=5)

        # remplissage de la liste des comptes
        for compte in self.dict_utilisateur:
            self.liste_comptes.insert(tk.END, compte)

    def set_dict(self, dict_utilisateur):
        self.dict_utilisateur = dict_utilisateur

        # remplissage de la liste des comptes
        self.liste_comptes.delete(0, tk.END)

        for compte in self.dict_utilisateur:
            self.liste_comptes.insert(tk.END, compte)


class GestionCompte(tk.Frame):
    def __init__(self, root):
        self.root = root
        # self.user_data = user_data
        super(GestionCompte, self).__init__()

        self.root.title("Gestion des comptes")
        self.root.geometry("1280x720")

        label = tk.Label(root, text="Gestion des comptes",
                         font=('Arial', 30), anchor='n')
        label.grid(row=0, column=1, padx=0, pady=0)

        # importation des donnees
        # def importer_donnees():
        #     """
        #     None -> dict
        #     Lit le fichier et retourne le contenu en dict
        #     """
        #     dict_utilisateur = {}
        #     with open(f"Gestion Compte/{self.user_data.get_utilisateur()}.txt") as f:
        #         contenu = f.read()
        #         # contenu = decryptage_cesar(cle, contenu)
        #         # pour chaque ligne du fichier
        #         for ligne in contenu.splitlines():
        #             # on separe les infos de la ligne
        #             info = ligne.split("*")
        #             if info[0] == "CPT":
        #                 dict_utilisateur[info[1]] = {
        #                     "budgets": [], "operations": []}
        #             elif info[0] == "OPE":
        #                 dict_utilisateur[info[3]]["operations"].append(
        #                     {"date": info[1], "nom": info[2], "montant": float(info[4]), "type": info[5], "statut": info[6], "budget": info[7]})
        #             elif info[0] == "BUD":
        #                 dict_utilisateur[info[3]]["budgets"].append(
        #                     {"nom": info[1], "montant": float(info[2])})
        #         return dict_utilisateur

        # # dictionnaire des comptes de l'utilisateur

        # dict_utilisateur = importer_donnees()

        # def exporter_donnees():
        #     """
        #     None -> None
        #     Exporte les donnees dans le fichier
        #     """
        #     with open(f"Gestion Compte/{self.user_data.get_utilisateur()}.txt", "w") as f:
        #         for compte in dict_utilisateur:
        #             f.write(f"CPT*{compte}\n")
        #             for budget in dict_utilisateur[compte]["budgets"]:
        #                 f.write(
        #                     f"BUD*{budget['nom']}*{budget['montant']}*{compte}\n")
        #             for operation in dict_utilisateur[compte]["operations"]:
        #                 f.write(
        #                     f"OPE*{operation['date']}*{operation['nom']}*{compte}*{operation['montant']}*{operation['type']}*{operation['statut']}*{operation['budget']}\n")
        # # calcul du solde du compte

        def calculer_solde():
            """Dict, Str -> Float
            Calcule le solde du compte."""
            solde = 0
            for operation in dict_utilisateur[compteCombo.get()]["operations"]:
                if operation["statut"] == "True":
                    solde += operation["montant"]
            return solde

        solde_compte = 0

        def actualiser_solde(*args):
            solde_compte = calculer_solde()
            actualiser_operations()
            soldeLabel.config(text=f"Solde du compte : {solde_compte}")

        def actualiser_operations(*args):
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
            if calculer_solde() + float(montant) < 0:
                return False
            else:
                return True

        # Bloc des fonctions pour ajouter une opération

        def ajouter_operation():
            # Créer une nouvelle fenêtre de dialogue modale
            dialog = tk.Toplevel()
            dialog.title("Nouvelle opération")

            # Fonction pour enregistrer l'opération
            def save_operation(dict_utilisateur=dict_utilisateur, compteCombo=compteCombo.get()):
                name = operation_name.get()
                amount = operation_amount.get()
                type = operation_type.get()
                budget = operation_budget.get()
                status = valider_transaction(amount)

                # Ajouter l'opération au dictionnaire
                dict_utilisateur[compteCombo]["operations"].append(
                    {"date": datetime.date.today(), "nom": name, "montant": float(amount),
                     "type": type, "statut": status, "budget": budget})
                dict_utilisateur = importer_donnees()
                actualiser_operations()
                actualiser_solde()
                exporter_donnees()

                # Actualiser les données dans le fichier

                # Afficher une boîte de dialogue de confirmation
                messagebox.showinfo("Opération enregistrée",
                                    "L'opération a été enregistrée avec succès.")

                # Ajouter ici le code pour enregistrer l'opération dans votre application

                # Bouton pour ajouter une opération
                ajouterButton = tk.Button(
                    root, text="Ajouter une opération", command=ajouter_operation)
                ajouterButton.grid(row=6, column=1, padx=10, pady=10)

                # fermer la fenêtre de dialogue
                dialog.destroy()

            # Ajouter des widgets pour saisir les informations de l'opération
            tk.Label(dialog, text="Nom de l'opération:").grid(row=0, column=0)
            operation_name = tk.Entry(dialog)
            operation_name.grid(row=0, column=1)

            tk.Label(dialog, text="Montant de l'opération:").grid(
                row=1, column=0)
            operation_amount = tk.Entry(dialog)
            operation_amount.grid(row=1, column=1)

            tk.Label(dialog, text="Budget :").grid(row=2, column=0)
            operation_budget = tk.Entry(dialog)
            operation_budget.grid(row=2, column=1)

            tk.Label(dialog, text="Type de l'opération:").grid(row=3, column=0)
            operation_type = tk.Entry(dialog)
            operation_type.grid(row=3, column=1)

            tk.Label(dialog, text="Montant de l'opération:").grid(
                row=1, column=0)
            operation_amount = tk.Entry(dialog)
            operation_amount.grid(row=1, column=1)

            # Ajouter des boutons pour enregistrer ou annuler l'opération
            buttonSave = tk.Button(
                dialog, text="Enregistrer", command=save_operation)
            buttonCancel = tk.Button(
                dialog, text="Annuler", command=dialog.destroy)
            buttonSave.grid(row=6, column=0, padx=10, pady=10)
            buttonCancel.grid(row=6, column=1, padx=10, pady=10)

        # liste des comptes de l'utilisateur
        liste_comptes = list(dict_utilisateur.keys())

        # liste déroulante
        labelCompte = tk.Label(root, text="Veuillez choisir un compte :")
        labelCompte.grid(row=2, column=1, padx=10, pady=10)

        # dictionnaire des comptes de l'utilisateur
        dict_utilisateur = importer_donnees()
        # liste des comptes de l'utilisateur
        liste_comptes = list(dict_utilisateur.keys())

        # liste déroulante
        compteCombo = ttk.Combobox(root, values=liste_comptes)
        compteCombo.grid(row=3, column=1, padx=10, pady=10)
        # valeur par défaut de la liste déroulante
        compteCombo.current(0)
        # actualisation du solde du compte choisi
        solde_compte = calculer_solde()

        compteCombo.bind("<<ComboboxSelected>>", actualiser_solde)
        # calcul du solde du compte choisi

        operations_compte = dict_utilisateur[compteCombo.get()]["operations"]

        # affichage du solde du compte
        soldeLabel = tk.Label(root, text=f"Solde du compte : {solde_compte}")
        soldeLabel.grid(row=4, column=1, padx=10, pady=10)

        # affichage des données du compte sous forme de tableau
        # Treeview (tableau)

        tableau = ttk.Treeview(root, columns=(
            "Date", "Nom", "Montant", "Type", "Statut", "Budget"))
        tableau.heading("Date", text="Date")
        tableau.heading("Nom", text="Nom")
        tableau.heading("Montant", text="Montant")
        tableau.heading("Type", text="Type")
        tableau.heading("Statut", text="Statut")
        tableau.heading("Budget", text="Budget")

        # Sans la ligne suivante, il y aurait une colonne vide à gauche

        tableau['show'] = 'headings'

        # Ajout des données

        for operation in operations_compte:
            tableau.insert("", "end", values=(
                operation["date"], operation["nom"], operation["montant"], operation["type"], operation["statut"], operation["budget"]))
        tableau.grid(row=5, column=1, padx=5, pady=5, )

        # Bouton pour ajouter une opération
        buttonOp = tk.Button(
            root, text="Ajouter une opération", command=ajouter_operation)
        buttonOp.grid(row=6, column=1, padx=10, pady=10)


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
