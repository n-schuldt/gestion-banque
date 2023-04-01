import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # creation du conteneur
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # taille de la fenetre
        self.geometry("1000x600")
        # titre de la fenetre
        self.title("Gestion Banque")

        # initializing frames to an empty array
        self.frames = {}
        
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LoginPage, Page1, Page2):

            frame = F(container, self)

            # initializing frame of that object from
            # Login Page, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # raise the frame to the top

# first window frame Login Page


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Login Page", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        def check_identification(numero_identification, mot_de_passe, fichier="ident.txt"):
            """
            str * str * str -> bool
            Verifie si le numero d'identification et le mot de passe
            sont corrects retourne True si le numero d'identification et le mot de passe
            sont corrects, False sinon
            """

            # numero_identification = "00000000"  # a enlever
            # mot_de_passe = "111111"  # a enlever

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

        def on_click_login():
            numero_identification = numero_identification_entry.get()
            mot_de_passe = mot_de_passe_entry.get()
            if check_identification(numero_identification, mot_de_passe):
                controller.show_frame(Page1)
            else:
                # afficher un message d'erreur
                tk.messagebox.showerror(
                    "Information", "Le numero d'identification ou le mot de passe est incorrect")
                print("Le numero d'identification ou le mot de passe est incorrect")

        # numero utilisateur
        numero_identification_label = ttk.Label(
            self, text="Numero d'identification")
        numero_identification_label.grid(row=1, column=1, padx=10, pady=10)
        numero_identification_entry = ttk.Entry(self)
        numero_identification_entry.grid(row=1, column=2, padx=10, pady=10)

        # password entry in keypad
        mot_de_passe = tk.StringVar()
        mot_de_passe_label = ttk.Label(self, text="Mot de passe")
        mot_de_passe_label.grid(row=2, column=1, padx=10, pady=10)
        # disable entry
        mot_de_passe_entry = ttk.Entry(
            self, textvariable=mot_de_passe, state="disabled")
        mot_de_passe_entry.grid(row=2, column=2, padx=10, pady=10)
        mot_de_passe_grid = ttk.Frame(self)
        mot_de_passe_grid.grid(row=3, column=2, padx=10, pady=10)

        # buttons for keypad
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        # randomize nums list
        random.shuffle(nums)
        # random buttons for keypad
        for i in range(9):
            ttk.Button(mot_de_passe_grid, text=nums[i], command=lambda n=nums[i]: mot_de_passe.set(
                mot_de_passe.get() + n)).grid(row=i//3+5, column=i % 3, padx=3, pady=3)

        ttk.Button(mot_de_passe_grid, text='Delete', command=lambda: mot_de_passe.set(
            mot_de_passe.get()[:-1])).grid(row=8, column=0, padx=3, pady=3)

        ttk.Button(mot_de_passe_grid, text=nums[9], command=lambda n=nums[9]: mot_de_passe.set(
            mot_de_passe.get() + n)).grid(row=8, column=1, padx=3, pady=3)

        ttk.Button(mot_de_passe_grid, text='Login',
                   command=on_click_login).grid(row=8, column=2, padx=0, pady=0)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        
        # usefull functions
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
        
        def calculer_solde(compte): # numero_identification -> compte
            """Dict, Str -> Float
            Calcule le solde du compte."""
            solde = 0
            for operation in dict_utilisateur[compte]["operations"]:
                if operation["statut"] == "True":
                    solde += operation["montant"]
            return solde
        
        # create label for displaying solde
        self.solde_label = ttk.Label(self, text="", font=LARGEFONT)
        self.solde_label.grid(row=0, column=2, padx=10, pady=10)
        
        # calculate and update solde label
        dict_utilisateur = importer_donnees(numero_identification) # numero_identification -> compte (need to be global)
        solde = calculer_solde(dict_utilisateur)
        self.solde_label.configure(text=f"Solde: {solde}€")

        # button to show frame 2 with text
        # layout2
        logout_button = ttk.Button(self, text="LoginPage",
                             command=lambda: controller.show_frame(LoginPage))

        # putting the button in its place by using grid
        logout_button.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        bank_manager = ttk.Button(self, text="Bank manager",
                             command=lambda: controller.show_frame(Page2))
        # putting the button in its place by using grid
        bank_manager.grid(row=2, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        budget_manager = ttk.Button(self, text="Budget manager",
                             command=lambda: controller.show_frame(Page3))
        # putting the button in its place by using grid
        budget_manager.grid(row=1, column=2, padx=10, pady=10)


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Login Page",
                             command=lambda: controller.show_frame(LoginPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


app = tkinterApp()
app.mainloop()