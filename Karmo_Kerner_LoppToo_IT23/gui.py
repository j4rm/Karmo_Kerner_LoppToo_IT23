import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data import Andmetöötleja


class Rakendus:
    def __init__(self, root):
        self.root = root
        self.root.title("Andmetöötluse rakendus")

        self.processor = None

        self.loo_gui()

    def loo_gui(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.faili_vali = ttk.Label(self.frame, text="Vali JSON fail")
        self.faili_vali.grid(row=0, column=0, sticky=tk.W)

        self.vali_nupp = ttk.Button(self.frame, text="Vali fail", command=self.vali_fail)
        self.vali_nupp.grid(row=0, column=1, sticky=tk.W)

        self.küsimuste_frame = ttk.Frame(self.frame, padding="10")
        self.küsimuste_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

    def vali_fail(self):
        failitee = filedialog.askopenfilename(filetypes=[("JSON failid", "*.json")])
        if failitee:
            try:
                self.processor = Andmetöötleja(failitee)
                self.kuva_andmed()
            except Exception as e:
                messagebox.showerror("Viga", f"Faili laadimisel tekkis viga: {e}")

    def kuva_andmed(self):
        for widget in self.küsimuste_frame.winfo_children():
            widget.destroy()

        küsimused = [
            ("Isikute arv kokku:", self.processor.isikute_arv),
            ("Kõige pikem nimi ja tähemärkide arv:", self.processor.kõige_pikem_nimi),
            ("Kõige vanem elav inimene:", self.processor.vanim_elus_isik),
            ("Kõige vanem surnud inimene:", self.processor.vanim_surnud_isik),
            ("Näitlejate koguarv:", self.processor.näitlejate_arv),
            ("Sündinud 1997 aastal:", self.processor.sündinud_1997),
            ("Erinevate elukutsete arv:", self.processor.erinevad_elukutsed),
            ("Nimi sisaldab rohkem kui kaks nime:", self.processor.rohkem_kui_kaks_nime),
            ("Sama sünni- ja surmaaeg (v.a. aasta):", self.processor.sama_sünni_surmaaeg),
            ("Elavaid ja surnud isikud:", self.processor.elavate_ja_surnute_arv)
        ]

        for i, (küsimus, funktsioon) in enumerate(küsimused):
            küsimuse_silt = ttk.Label(self.küsimuste_frame, text=küsimus)
            küsimuse_silt.grid(row=i, column=0, sticky=tk.W)

            vastus = funktsioon()
            if isinstance(vastus, tuple):
                vastus = ", ".join(map(str, vastus))

            vastuse_silt = ttk.Label(self.küsimuste_frame, text=vastus)
            vastuse_silt.grid(row=i, column=1, sticky=tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    app = Rakendus(root)
    root.mainloop()
