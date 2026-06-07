import streamlit as st
st.title("Code puzzle traduction")

# ==========================================
# Classe Bloc avec hauteur automatique
# ==========================================

class Bloc:
    def __init__(self, canvas, texte, x, y):

        self.canvas = canvas
        self.texte = texte

        lignes = texte.count("\n") + 1
        hauteur_ligne = 18
        marge = 20

        self.hauteur = lignes * hauteur_ligne + marge
        self.largeur = 520

        self.rect = canvas.create_rectangle(
            x, y, x + self.largeur, y + self.hauteur,
            fill="lightyellow",
            outline="black"
        )

        self.text = canvas.create_text(
            x + 10,
            y + 10,
            text=texte,
            font=("Courier", 10),
            anchor="nw",
            width=self.largeur - 20
        )

        for item in (self.rect, self.text):
            canvas.tag_bind(item, "<Button-1>", self.start_drag)
            canvas.tag_bind(item, "<B1-Motion>", self.drag)

        self.last_x = 0
        self.last_y = 0

    def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def drag(self, event):

        dx = event.x - self.last_x
        dy = event.y - self.last_y

        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.text, dx, dy)

        self.last_x = event.x
        self.last_y = event.y

        # mise à jour scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_y(self):
        return self.canvas.coords(self.rect)[1]


# ==========================================
# Application principale
# ==========================================

class App:

    def __init__(self, root):

        root.title("Puzzle ADN → Protéine")
        root.geometry("900x600")

        # frame principale
        frame = st.Frame(root)
        frame.pack(fill="both", expand=True)

        # canvas
        self.canvas = st.Canvas(frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # scrollbar verticale
        scrollbar = st.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # blocs mélangés (empilés verticalement)
        y = 20
        espace = 20

        self.blocs = []

        def ajouter_bloc(texte):
            nonlocal y
            bloc = Bloc(self.canvas, texte, 50, y)
            self.blocs.append(bloc)
            y += bloc.hauteur + espace

        ajouter_bloc(
'''# Bloc B
brin_ARN = brin_ADN_propre.replace('T', 'U')''')

        ajouter_bloc(
'''# Bloc F
def nettoyage(tab):
    j = 0
    for i in tab:
        if tab[j] == 'AUG':
            for k in range(j):
                del tab[0]
            break
        j += 1

    j = 0
    for i in tab:
        if tab[j] in ['UAA','UAG','UGA']:
            for k in range(j, len(tab)):
                del tab[j]
            break
        j += 1
    return tab''')

        ajouter_bloc(
'''# Bloc C
brin_ADN = input("Entrez la séquence ADN : ")
brin_ADN_propre = brin_ADN.upper()''')

        ajouter_bloc(
'''# Bloc D
code_genet = {
    'AUG':'Met',
    'UUU':'Phe','UUC':'Phe',
    'UAA':'STOP','UAG':'STOP','UGA':'STOP'
}''')

        ajouter_bloc(
'''# Bloc A
j = 0
brin_ARN_propre = []
while j < len(brin_ARN):
    brin_ARN_propre.append(brin_ARN[j:j+3])
    j += 3''')

        ajouter_bloc(
'''# Bloc G
resultat = nettoyage(brin_ARN_propre)''')
        
        ajouter_bloc(
'''# Bloc E
print("Protéine correspondante :")
for codon in resultat:
    if codon in code_genet:
        if code_genet[codon] == "STOP":
            break
        print(code_genet[codon], end='-')
    else:
        print("Erreur codon", codon)
        break''')


        # mise à jour scrollregion initiale
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # bouton exécuter
        bouton = st.Button(root, text="Exécuter", command=self.executer)
        bouton.pack(pady=5)

    # ==========================================
    # exécution
    # ==========================================

    def executer(self):

        blocs_tries = sorted(self.blocs, key=lambda b: b.get_y())

        code = ""

        for bloc in blocs_tries:
            code += bloc.texte + "\n\n"

        print("\n===== CODE EXECUTE =====\n")
        print(code)

        try:
            exec(code)
        except Exception as e:
            print("Erreur :", e)




