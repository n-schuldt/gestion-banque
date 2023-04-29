import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from math import ceil
import random
import datetime

LARGEFONT = ("Verdana", 35)


def importer_donnees(identifiant_utilisateur):
    """
    None -> dict
    Lit le fichier et retourne le contenu en dict
    """
    global dict_utilisateur
    dict_utilisateur = {}
    with open(f"00000000.txt") as f:  # a changer
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


def exporter_donnees(identifiant_utilisateur, dict_utilisateur):
    """
    str * dict -> None
    Exporte les donnees du dictionnaire dans le fichier
    """
    with open(f"{identifiant_utilisateur}.txt", "w") as f:
        for compte in dict_utilisateur:
            f.write(f"CPT*{compte}\n")
            for operation in dict_utilisateur[compte]["operations"]:
                f.write(
                    f"OPE*{operation['date']}*{operation['nom']}*{compte}*{operation['montant']}*{operation['type']}*{operation['statut']}*{operation['budget']}\n")
            for budget in dict_utilisateur[compte]["budgets"]:
                f.write(f"BUD*{budget['nom']}*{budget['montant']}*{compte}\n")


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
        for FrameClass in (LoginPage, DashboardPage, Comptes, Budget, AffichBud, AffichOpe, NewBud):
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

    def set_identifiant(self, identifiant):
        dashboard_frame = self.frames[DashboardPage]
        dashboard_frame.set_identifiant(identifiant)

    def init_dict(self, identifiant):
        """
        str -> None
        Initialise le dictionnaire de l'utilisateur avec les donnees du fichier """
        dict_utilisateur = importer_donnees(identifiant)

        print("init_dict")

        self.set_dict(dict_utilisateur)

    def set_dict(self, dict_utilisateur):
        """
        str -> None
        Met a jour le dictionnaire de l'utilisateur avec les donnees du fichier
        dans tous les frames
        """

        print("set_dict")
        print("Comptes", list(dict_utilisateur.keys()))
        print("Budgets", dict_utilisateur['Compte A']["budgets"])
        print("Operations", dict_utilisateur["Compte A"]["operations"])

        dashboard_frame = self.frames[DashboardPage]
        dashboard_frame.set_dict(dict_utilisateur)

        comptes_frame = self.frames[Comptes]
        comptes_frame.set_dict(dict_utilisateur)

        budgets_frame = self.frames[Budget]
        budgets_frame.set_dict(dict_utilisateur)

        affichbud_frame = self.frames[AffichBud]
        affichbud_frame.set_dict(dict_utilisateur)

        affichope_frame = self.frames[AffichOpe]
        affichope_frame.set_dict(dict_utilisateur)

        newbud_frame = self.frames[NewBud]
        newbud_frame.set_dict(dict_utilisateur)


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        def on_click_login():
            numero_identification = username_entry.get()
            mot_de_passe = mot_de_passe_entry.get()
            if self.check_identification(numero_identification, mot_de_passe):
                self.master.set_username(numero_identification)
                self.master.set_identifiant(numero_identification)
                self.master.init_dict(numero_identification)
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

    def check_identification(self, numero_identification, mot_de_passe):
        """
        str * str * str -> bool
        Verifie si le numero d'identification et le mot de passe
        sont corrects retourne True si le numero d'identification et le mot de passe
        sont corrects, False sinon
        """

        numero_identification = "00000000"  # a enlever
        mot_de_passe = "111111"  # a enlever

        with open("ident.txt") as f:
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

# Class pour la fenêtre Menu :


class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self,  master)
        self.master = master
        self.identifiant = ""

        # Fonctions pour calculer le solde
        budget = 1000  # Budget a modifier

        # Créer des boutons ici (FRAME LEFT)
        self.button = tk.Button(self, text="GESTION BUDGET", command=lambda: self.master.show_frame(
            Budget), font=('DejaVu Sans', 15), width=20, height=5)
        self.button.grid(row=1, column=0, padx=5, pady=5)

        self.button2 = tk.Button(self, text="GESTION COMPTE", command=lambda: self.master.show_frame(
            Comptes), font=('DejaVu Sans', 15), width=20, height=5)
        self.button2.grid(row=2, column=0, padx=5, pady=5)

        self.button3 = tk.Button(self, text="LOGOUT", command=lambda: self.logout(), font=(
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

    def set_identifiant(self, identifiant):
        print("IDENT set", identifiant)
        self.identifiant = identifiant

    def set_dict(self, dict_utilisateur):
        """
        Dict -> None
        Met à jour le dictionnaire de l'utilisateur
        """
        self.dict_utilisateur = dict_utilisateur

    def logout(self):
        """Fonction pour se déconnecter"""
        print("Déconnexion")
        print("IDENT", self.identifiant)
        exporter_donnees(self.identifiant, self.dict_utilisateur)
        self.master.show_frame(LoginPage)

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

        self.master = master

        self.dict_utilisateur = {"Compte A": {
            "budgets": [{}], "operations": [{"nom": "Operation 1", "montant": 100, "statut": "True", "date": "2020-01-01", "type": "Type", "budget": "Test BUD"}]}, "Compte B": {"budgets": [{}], "operations": [{"nom": "Operation B", "montant": 300, "statut": "True", "date": "2020-01-01", "type": "Type", "budget": "Test BUD"}]}}

        # titre
        self.label = tk.Label(self, text="Gestion des comptes")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        # bouton pour revenir au dashboard
        self.button = tk.Button(self, text="Retour au dashboard",
                                command=lambda: master.show_frame(DashboardPage))
        self.button.grid(row=1, column=0, padx=5, pady=5)

        # liste des comptes de l'utilisateur
        self.liste_comptes = list(self.dict_utilisateur.keys())

        # liste déroulante
        labelCompte = tk.Label(self, text="Veuillez choisir un compte :")
        labelCompte.grid(row=2, column=1, padx=10, pady=10)

        # liste déroulante
        self.compteCombo = ttk.Combobox(
            self, values=self.liste_comptes, state="readonly")
        self.compteCombo.grid(row=3, column=1, padx=8, pady=8)

        # valeur par défaut de la liste déroulante
        self.compteCombo.current(0)

        self.solde = tk.StringVar()

        # calcul du solde du compte choisi

        self.operations_compte = self.dict_utilisateur[self.compteCombo.get(
        )]["operations"]

        # affichage du solde du compte
        self.soldeLabel = tk.Label(
            self, text=f"Solde du compte : {str(self.solde.get())}")
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

        # actualisation du solde du compte choisi
        self.compteCombo.bind("<<ComboboxSelected>>",
                              lambda event: self.onCompteChange())

        # bouton pour ajouter une opération
        self.button = tk.Button(self, text="Ajouter une opération",
                                command=lambda: self.ajouter_operation())
        self.button.grid(row=6, column=1, padx=5, pady=5)

        # Bouton pour faire un virement

        buttonVirement = tk.Button(
            self, text="Faire un virement", command=self.faire_virement)
        buttonVirement.grid(row=7, column=1, padx=10, pady=10)

        # Bouton pour ajouter un compte
        buttonCompte = tk.Button(
            self, text="Ajouter un compte", command=self.ajouter_compte)
        buttonCompte.grid(row=8, column=1, padx=10, pady=10)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur

        self.compteCombo.config(values=list(dict_utilisateur.keys()))
        self.compteCombo.current(0)

        # actualisation du tableau
        self.actualiser_operations(
            self.tableau, self.dict_utilisateur, self.compteCombo.get())

        self.tableau.grid(row=5, column=1, padx=1, pady=1, columnspan=2)

        # actualisation du solde
        self.actualiser_solde(
            self.soldeLabel)

    def onCompteChange(self):
        """None -> None
        Actualise le solde et le tableau avec les donnees du compte sélectionné."""

        self.actualiser_operations(
            self.tableau, self.dict_utilisateur, self.compteCombo.get())
        self.actualiser_solde(
            self.soldeLabel)

    def actualiser_operations(self, tableau, dict_utilisateur, compte):
        """
        Tableau * dict * str -> None
        Actualise les opérations du compte sélectionné.
        """
        operations_compte = dict_utilisateur[compte]["operations"]
        for operation in tableau.get_children():
            tableau.delete(operation)
        for operation in operations_compte:
            tableau.insert("", "end", values=(operation["date"], operation["nom"], operation["montant"],
                                              operation["type"], operation["statut"], operation["budget"]))

    def valider_transaction(self, compte, montant):
        """
        float * str -> Bool
        Valide la transaction.
        """
        if self.calculer_solde(self.dict_utilisateur, compte) + float(montant) < 0:
            return False
        else:
            return True

    def actualiser_solde(self, soldeLabel):
        """
        Label -> None
        Actualise le solde du compte sélectionné.
        Ne prend pas en compte les opérations en attente de validation (statut = False)
        """
        solde = self.calculer_solde(
            self.dict_utilisateur, self.compteCombo.get())
        self.solde.set(solde)
        soldeLabel.config(text=f"Solde du compte : {ceil(solde)}")

    # Fonction pour ajouter une opération
    def ajouter_operation(self):
        # Créer une nouvelle fenêtre de dialogue
        dialog = tk.Toplevel()
        dialog.title("Nouvelle opération")

        # Widgets pour saisir les détails de l'opération
        operation_name_label = tk.Label(dialog, text="Nom :")
        operation_name_label.grid(row=0, column=0, padx=5, pady=5)

        operation_name = tk.Entry(dialog)
        operation_name.grid(row=0, column=1, padx=5, pady=5)

        operation_amount_label = tk.Label(dialog, text="Montant :")
        operation_amount_label.grid(row=1, column=0, padx=5, pady=5)

        operation_amount = tk.Entry(dialog)
        operation_amount.grid(row=1, column=1, padx=5, pady=5)

        operation_type_label = tk.Label(dialog, text="Type :")
        operation_type_label.grid(row=2, column=0, padx=5, pady=5)

        operation_type = ttk.Combobox(dialog, values=[
            "CB", "VIR", "CHE"], state="readonly")

        operation_type.grid(row=2, column=1, padx=5, pady=5)

        operation_budget_label = tk.Label(dialog, text="Budget :")
        operation_budget_label.grid(row=3, column=0, padx=5, pady=5)

        operation_budget = tk.Entry(dialog)
        operation_budget.grid(row=3, column=1, padx=5, pady=5)

        operation_budget_paragraph_label = tk.Label(
            dialog, text="Si vous mettez un budget qui n'existe pas, créez-le après avoir enregistré le virement.")
        operation_budget_paragraph_label.grid(row=3, column=2, padx=5, pady=5)

        operation_date_label = tk.Label(dialog, text="Date :")
        operation_date_label.grid(row=4, column=0, padx=5, pady=5)

        operation_jour = ttk.Combobox(dialog, values=[
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31'], state='readonly')

        operation_mois = ttk.Combobox(dialog, values=[
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12'], state='readonly')

        operation_annee = ttk.Combobox(dialog, values=[
            '2018', '2019', '2020', '2021', '2022', '2023'], state='readonly')

        operation_jour.grid(row=4, column=1, padx=0, pady=0)
        operation_mois.grid(row=4, column=2, padx=0, pady=0)
        operation_annee.grid(row=4, column=3, padx=0, pady=0)

        compteCombo_label = tk.Label(dialog, text="Compte :")
        compteCombo_label.grid(row=5, column=0, padx=5, pady=5)

        compteCombo = ttk.Combobox(
            dialog, values=list(self.dict_utilisateur.keys()), state="readonly")
        compteCombo.grid(row=5, column=1, padx=5, pady=5)

        # Bouton pour enregistrer l'opération
        enregistrerButton = tk.Button(dialog, text="Enregistrer", command=lambda: self.save_operation(self.dict_utilisateur, compteCombo.get(),
                                                                                                      dialog, operation_name, operation_amount, operation_type,
                                                                                                      operation_budget, (operation_jour.get() + '/' + operation_mois.get() +
                                                                                                                         '/' + operation_annee.get())))
        enregistrerButton.grid(row=6, column=0, padx=10, pady=10)

        # Bouton pour fermer la fenêtre de dialogue
        annulerButton = tk.Button(
            dialog, text="Annuler", command=dialog.destroy)
        annulerButton.grid(row=6, column=1, padx=10, pady=10)

        # Bouton pour ajouter une opération
        buttonOp = tk.Button(self, text="Ajouter une opération",
                             command=self.ajouter_operation)
        buttonOp.grid(row=6, column=1, padx=10, pady=10)

    def save_operation(self, dict_utilisateur, compteCombo, dialog, operation_name, operation_amount, operation_type, operation_budget, operation_date):
        name = operation_name.get()
        amount = operation_amount.get()
        type = operation_type.get()
        budget = operation_budget.get()
        date = operation_date
        status = self.valider_transaction(compteCombo, amount)

        # Ajouter l'opération au dictionnaire
        dict_utilisateur[compteCombo]["operations"].append(
            {"nom": name, "montant": float(amount), "statut": str(status), "date": date, "type": type, "budget": budget})

        # Afficher une boîte de dialogue de confirmation
        messagebox.showinfo("Opération enregistrée",
                            "L'opération a été enregistrée avec succès.")

        # Actualiser les opérations du compte
        self.actualiser_operations(
            self.tableau, self.dict_utilisateur, self.compteCombo.get())

        # Actualiser le solde du compte
        self.actualiser_solde(self.soldeLabel)

        # Fermer la fenêtre de dialogue
        dialog.destroy()

    def save_virement(self, dict_utilisateur, compteCombo, compteCiblecombo, dialog, virement_name, virement_amount, virement_budget, virement_date):

        # récupération des données saisies
        nom = virement_name
        montant = virement_amount
        budget = virement_budget
        compte_cible = compteCiblecombo
        statut = self.valider_transaction(compteCombo, montant)
        date = virement_date

        # création du dictionnaire de l'opération
        dict_virement = {"nom": nom, "montant": (-1.0 * float(montant)), "statut": str(
            statut), "date": date, "type": "VIR", "budget": budget}

        # création dictionnaire pour compte cible
        dict_virement_c = {"nom": nom, "montant": float(montant), "statut": str(
            statut), "date": date, "type": "VIR", "budget": budget}

        # ajout de l'opération au compte
        dict_utilisateur[compteCombo]["operations"].append(dict_virement)

        # ajout de l'opération au compte cible
        dict_utilisateur[compte_cible]["operations"].append(dict_virement_c)

        self.master.set_dict(dict_utilisateur)

        # fermeture de la fenêtre de dialogue
        dialog.destroy()

    # fonction pour faire un virement
    def faire_virement(self):
        # Créer une nouvelle fenêtre de dialogue
        dialog = tk.Toplevel()
        dialog.title("Nouveau virement")

        # Widgets pour saisir les détails du virement
        virement_name_label = tk.Label(dialog, text="Nom :")
        virement_name_label.grid(row=0, column=0, padx=5, pady=5)

        virement_name = tk.Entry(dialog)
        virement_name.grid(row=0, column=1, padx=5, pady=5)

        virement_amount_label = tk.Label(dialog, text="Montant :")
        virement_amount_label.grid(row=1, column=0, padx=5, pady=5)

        virement_amount = tk.Entry(dialog)
        virement_amount.grid(row=1, column=1, padx=5, pady=5)

        virement_budget_label = tk.Label(dialog, text="Budget :")
        virement_budget_label.grid(row=3, column=0, padx=5, pady=5)

        virement_budget = tk.Entry(dialog)
        virement_budget.grid(row=3, column=1, padx=5, pady=5)

        virement_budget_paragraph_label = tk.Label(
            dialog, text="")
        virement_budget_paragraph_label.grid(row=3, column=2, padx=5, pady=5)

        virement_date_label = tk.Label(dialog, text="Date :")
        virement_date_label.grid(row=4, column=0, padx=5, pady=5)

        virement_jour = ttk.Combobox(dialog, values=[
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
            '31'], state='readonly')

        virement_mois = ttk.Combobox(dialog, values=[
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12'], state='readonly')

        virement_annee = ttk.Combobox(dialog, values=[
            '2018', '2019', '2020', '2021', '2022', '2023'], state='readonly')

        virement_jour.grid(row=4, column=1, padx=0, pady=0)
        virement_mois.grid(row=4, column=2, padx=0, pady=0)
        virement_annee.grid(row=4, column=3, padx=0, pady=0)

        compteCombo_label = tk.Label(dialog, text="Compte :")
        compteCombo_label.grid(row=5, column=0, padx=5, pady=5)

        compteCombo = ttk.Combobox(
            dialog, values=list(self.dict_utilisateur.keys()))
        compteCombo.grid(row=5, column=1, padx=5, pady=5)

        compteCible_label = tk.Label(dialog, text="Compte cible :")
        compteCible_label.grid(row=2, column=0, padx=5, pady=5)

        compteCibleCombo = ttk.Combobox(
            dialog, values=list(self.dict_utilisateur.keys()), state="readonly")
        compteCibleCombo.grid(row=2, column=1, padx=5, pady=5)

        # Bouton pour enregistrer le virement
        enregistrerButton = tk.Button(dialog, text="Enregistrer", command=lambda: self.save_virement(dict_utilisateur, compteCombo.get(),
                                                                                                     compteCibleCombo.get(), dialog, virement_name.get(),
                                                                                                     virement_amount.get(), virement_budget.get(),
                                                                                                     (virement_jour.get() + "/" + virement_mois.get() + "/" + virement_annee.get())))
        enregistrerButton.grid(row=6, column=0, padx=10, pady=10)

        # Bouton pour fermer la fenêtre de dialogue
        annulerButton = tk.Button(
            dialog, text="Annuler", command=dialog.destroy)
        annulerButton.grid(row=6, column=1, padx=10, pady=10)

    # fonction pour ajouter un compte
    def ajouter_compte(self):
        # Créer une nouvelle fenêtre de dialogue
        dialog = tk.Toplevel()
        dialog.title("Nouveau compte")

        # Widgets pour saisir les détails du compte
        compte_name_label = tk.Label(dialog, text="Nom :")
        compte_name_label.grid(row=0, column=0, padx=5, pady=5)

        compte_name = tk.Entry(dialog)
        compte_name.grid(row=0, column=1, padx=5, pady=5)

        # Bouton pour enregistrer le compte
        enregistrerButton = tk.Button(dialog, text="Enregistrer", command=lambda: self.save_compte(
            compte_name.get(), dialog))
        enregistrerButton.grid(row=2, column=0, padx=10, pady=10)

        # Bouton pour fermer la fenêtre de dialogue
        annulerButton = tk.Button(
            dialog, text="Annuler", command=dialog.destroy)
        annulerButton.grid(row=2, column=1, padx=10, pady=10)

        # fonction pour enregistrer le compte
    def save_compte(self, nom, dialog):
        # création dictionnaire pour le compte
        dict_compte = {"budgets": [], "operations": []}

        # ajout du compte au dictionnaire utilisateur
        new_dict_utilisateur = self.dict_utilisateur
        self.dict_utilisateur[nom] = dict_compte
        print("\nBefore : ", self.liste_comptes)
        self.liste_comptes = list(self.dict_utilisateur.keys())

        print("Nouveau compte ajouté : ", self.liste_comptes, "\n")

        # actualisation du dictionnaire utilisateur
        self.master.set_dict(new_dict_utilisateur)

        # actualisation de la liste des comptes
        self.compteCombo["values"] = self.liste_comptes
        self.compteCombo.current(len(self.liste_comptes)-1)
        self.onCompteChange()

        # fermeture de la fenêtre de dialogue
        dialog.destroy()

    def calculer_solde(self, dict_utilisateur, compte):
        """Dict, Str -> Float
        Calcule le solde du compte."""
        solde = 0
        for operation in dict_utilisateur[compte]["operations"]:
            if operation["statut"] == "True":
                solde = solde + float(operation["montant"])
        return solde


class Budget(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.dict_utilisateur = {}

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
                               text="Ajouter un budget",
                               command=lambda:  master.show_frame(NewBud),
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

        bouton_retour = ttk.Button(self, text="Retour",
                                   command=lambda:  master.show_frame(Budget))

        bouton_retour.grid(row=2, column=1, padx=10, pady=10)
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

        self.dict_utilisateur = {}

        # Titre
        label = ttk.Label(
            self, text="Afficher les opérations d'un budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # Bouton retour
        bouton_retour = ttk.Button(self, text="Retour",
                                   command=lambda: master.show_frame(Budget))
        bouton_retour.grid(row=2, column=1, padx=10, pady=10)

        comptes = list(self.dict_utilisateur.keys())

        # combo box pour choisir le compte
        label_combo_comptes = ttk.Label(self, text="Compte :")
        label_combo_comptes.grid(row=2, column=3, padx=0, pady=5)
        self.liste_combo_comptes = ttk.Combobox(
            self, values=["-"] + comptes, state="readonly")
        self.liste_combo_comptes.current(0)
        self.liste_combo_comptes.grid(row=2, column=4, padx=0, pady=5)
        self.liste_combo_comptes.bind("<<ComboboxSelected>>",
                                      lambda event: filtrer_operations())

        # combo box pour choisir le budget
        label_combo_budgets = ttk.Label(self, text="Budget :")
        label_combo_budgets.grid(row=3, column=3, padx=0, pady=5)
        self.liste_combo_budgets = ttk.Combobox(self, values=(["-"] + list(
            self.dict_utilisateur.values())), height=5, width=10, state="readonly")
        # get budgets
        budgets = ['-']
        for compte in self.dict_utilisateur.values():
            for b in compte['budgets']:
                budgets.append(b['nom'])
        self.liste_combo_budgets.configure(values=budgets, height=10)
        self.liste_combo_budgets.current(0)
        self.liste_combo_budgets.grid(row=3, column=4, padx=0, pady=5)
        self.liste_combo_budgets.bind("<<ComboboxSelected>>",
                                      lambda event: filtrer_operations())

        # combo box pour choisir le mois
        label_combo_mois = ttk.Label(self, text="Mois :")
        label_combo_mois.grid(row=4, column=3, padx=0, pady=5)
        liste_combo_mois = ttk.Combobox(self, values=[
            "-", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], state="readonly")
        liste_combo_mois.current(0)
        liste_combo_mois.grid(row=4, column=4, padx=0, pady=5)
        liste_combo_mois.bind("<<ComboboxSelected>>",
                              lambda event: filtrer_operations())

        # combo box pour choisir l'année
        label_combo_annees = ttk.Label(self, text="Année :")
        label_combo_annees.grid(row=5, column=3, padx=0, pady=5)
        liste_combo_annees = ttk.Combobox(
            self, values=["-", "2019", "2020", "2021", "2022", "2023"], state="readonly")
        liste_combo_annees.current(0)
        liste_combo_annees.grid(row=5, column=4, padx=0, pady=5)
        liste_combo_annees.bind("<<ComboboxSelected>>",
                                lambda event: filtrer_operations())

        # Créer un widget Treeview (tableau)
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
        tableau.grid(row=6, column=4, padx=30, pady=30)

        # fonction de filtrage des opérations
        def filtrer_operations():
            # Récupérer les valeurs sélectionnées dans les combobox
            compte_selec = self.liste_combo_comptes.get()
            budget_selec = self.liste_combo_budgets.get()
            mois_selec = liste_combo_mois.get()
            year_selec = liste_combo_annees.get()

            if self.liste_combo_comptes.get() != '-':
                compte = dict_utilisateur[self.liste_combo_comptes.get()]
                budgets = ['-']
                for b in compte['budgets']:
                    budgets.append(b['nom'])
                self.liste_combo_budgets.configure(values=budgets)

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

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur

        # Mettre à jour les combobox
        self.liste_combo_comptes.configure(
            values=["-"] + list(dict_utilisateur.keys()))

        # get budgets
        budgets = ['-']

        if self.liste_combo_comptes.get() != '-':
            compte = dict_utilisateur[self.liste_combo_comptes.get()]
            for b in compte['budgets']:
                budgets.append(b['nom'])
            self.liste_combo_budgets.configure(values=budgets)

        # Mettre à jour le tableau
        # self.filtrer_operations()


class NewBud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Frame.__init__(self, master)

        self.dict_utilisateur = {}

        label = ttk.Label(
            self, text="Entrez les infos du nouveau Budget", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        bouton_retour = ttk.Button(self, text="Retour",
                                   command=lambda: master.show_frame(Budget))
        bouton_retour.grid(row=2, column=1, padx=10, pady=10)

        def recuperer_texte():
            compte = self.comptes_combo.get()
            # Appeler la fonction pour ajouter le budget
            ajouter_budget(compte, nom_budget.get(), montant_budget.get())

        # Créer un champ d'entrée
        nom_budget = tk.Entry(self, text="Nom du budget")
        etiquette1 = tk.Label(self, text='Nom du budget')
        etiquette1.grid(row=1, column=2, padx=5, pady=5)
        nom_budget.grid(row=2, column=2, padx=5, pady=5)
        montant_budget = tk.Entry(self, text="Montant du budget")
        etiquette2 = tk.Label(self, text='Montant du budget')
        etiquette2.grid(row=3, column=2, padx=5, pady=5)
        montant_budget.grid(row=4, column=2, padx=5, pady=5)

        # Créer une variable pour le choix du compte
        var_compte = list(self.dict_utilisateur.keys())
        # Définir la valeur par défaut
        # Créer un menu déroulant pour choisir le compte
        self.comptes_combo = ttk.Combobox(
            self, values=var_compte, height=5, width=10, state="readonly")
        etiquette_combo = tk.Label(self, text='Comptes')
        etiquette_combo.grid(row=7, column=2, padx=5, pady=5)
        self.comptes_combo.grid(row=8, column=2, padx=5, pady=5)

        # Créer un bouton pour récupérer le texte
        bouton = tk.Button(self, text='Ajouter',
                           height=3,
                           width=10,
                           command=recuperer_texte)
        bouton.grid(row=3, column=4, padx=10, pady=10)

        def ajouter_budget(compte, nom_budget, montant_budget):

            try:
                # Vérifier si le montant est un nombre
                float(montant_budget)
            except ValueError:
                # Afficher un message d'erreur à l'utilisateur
                messagebox.showerror(
                    "Erreur", "Le montant doit être un nombre.")
                return
            # Vérifier si le montant est positif
            if float(montant_budget) < 0:
                # Afficher un message d'erreur à l'utilisateur
                messagebox.showerror(
                    "Erreur", "Le montant doit être positif.")
                return

            if nom_budget == "":
                messagebox.showerror(
                    "Erreur", "Veuillez entrer un nom de budget.")
                return

            if montant_budget == "":
                messagebox.showerror(
                    "Erreur", "Veuillez entrer un montant de budget.")
                return

            if compte == "":
                messagebox.showerror(
                    "Erreur", "Veuillez choisir un compte.")
                return

            # Vérifier si le compte existe dans le dictionnaire de l'utilisateur
            if compte in dict_utilisateur:
                # Ajouter le nouveau budget au compte existant
                nouveau_budget = {"nom": nom_budget,
                                  "montant": float(montant_budget)}
                dict_utilisateur[compte]["budgets"].append(nouveau_budget)

            # Afficher le dictionnaire mis à jour dans la console
            print(dict_utilisateur)

            # Afficher un message de confirmation à l'utilisateur
            messagebox.showinfo(
                "Confirmation", "Le budget a été ajouté avec succès.")

            # retourner à la page Budget
            master.set_dict(dict_utilisateur)
            master.show_frame(Budget)

    def set_dict(self, dict_utilisateur):
        """Dict -> None
        Met à jour le dictionnaire de l'utilisateur."""

        self.dict_utilisateur = dict_utilisateur

        # Mettre à jour les combobox
        self.comptes_combo.configure(
            values=list(dict_utilisateur.keys()))


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
