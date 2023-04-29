import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import datetime

# class pour stocker l'identifiant de l'utilisateur


class UserData:
    def __init__(self):
        self.utilisateur = None

    def set_utilisateur(self, utilisateur):
        self.utilisateur = utilisateur

    def get_utilisateur(self):
        return self.utilisateur

# Page de la gestion des comptes


class GestionCompte(tk.Frame):
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        super(GestionCompte, self).__init__()

        self.root.title("Gestion des comptes")
        self.root.geometry("1280x720")

        label = tk.Label(root, text="Gestion des comptes",
                         font=('Arial', 30), anchor='n')
        label.grid(row=0, column=1, padx=0, pady=0)

        # importation des donnees
        def importer_donnees():
            """
            None -> dict
            Lit le fichier et retourne le contenu en dict
            """
            dict_utilisateur = {}
            with open(f"Gestion Compte/{self.user_data.get_utilisateur()}.txt") as f:
                contenu = f.read()
                # contenu = decryptage_cesar(cle, contenu)
                # pour chaque ligne du fichier
                for ligne in contenu.splitlines():
                    # on separe les infos de la ligne
                    info = ligne.split("*")
                    if info[0] == "CPT":
                        dict_utilisateur[info[1]] = {
                            "budgets": [], "operations": []}
                    elif info[0] == "OPE":
                        dict_utilisateur[info[3]]["operations"].append(
                            {"date": info[1], "nom": info[2], "montant": float(info[4]), "type": info[5], "statut": info[6], "budget": info[7]})
                    elif info[0] == "BUD":
                        dict_utilisateur[info[3]]["budgets"].append(
                            {"nom": info[1], "montant": float(info[2])})
                return dict_utilisateur

        # dictionnaire des comptes de l'utilisateur

        dict_utilisateur = importer_donnees()

        def exporter_donnees():
            """
            None -> None
            Exporte les donnees dans le fichier
            """
            with open(f"Gestion Compte/{self.user_data.get_utilisateur()}.txt", "w") as f:
                for compte in dict_utilisateur:
                    f.write(f"CPT*{compte}\n")
                    for budget in dict_utilisateur[compte]["budgets"]:
                        f.write(
                            f"BUD*{budget['nom']}*{budget['montant']}*{compte}\n")
                    for operation in dict_utilisateur[compte]["operations"]:
                        f.write(
                            f"OPE*{operation['date']}*{operation['nom']}*{compte}*{operation['montant']}*{operation['type']}*{operation['statut']}*{operation['budget']}\n")
        # calcul du solde du compte

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

        # Bouton pour se déconnecter
        def deconnecter():
            # Mettre ici le code pour se déconnecter de l'application
            # Par exemple, réinitialiser l'objet user_data et afficher une fenêtre de connexion
            messagebox.showinfo("Déconnexion", "Vous avez été déconnecté.")
            self.root.destroy()

        button_deconnexion = ttk.Button(
            root, text="Déconnexion", command=deconnecter)
        button_deconnexion.grid(row=8, column=1, padx=10, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    user_data = UserData()
    # Définir l'identifiant de l'utilisateur ici
    user_data.set_utilisateur("00000002")
    app = GestionCompte(root, user_data=user_data)
    app.mainloop()
