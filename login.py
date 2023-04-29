
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        def on_click_login():
            numero_identification = username_entry.get()
            mot_de_passe = mot_de_passe_entry.get()
            if self.check_identification(numero_identification, mot_de_passe):
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

# exporter