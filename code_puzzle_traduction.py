#version stramite sans tkinter
import streamlit as st

st.set_page_config(
    page_title="Puzzle ADN → Protéine",
    page_icon="🧬"
)

st.title("🧬 Puzzle ADN → Protéine")

st.write(
    "Replace les blocs dans le bon ordre pour reconstruire le programme."
)

# ----------------------------
# Blocs du puzzle
# ----------------------------

blocs = {

"C": """# Bloc C
brin_ADN = input("Entrez la séquence ADN : ")
brin_ADN_propre = brin_ADN.upper()
""",

"B": """# Bloc B
brin_ARN = brin_ADN_propre.replace('T','U')
""",

"A": """# Bloc A
j = 0
brin_ARN_propre = []

while j < len(brin_ARN):
    brin_ARN_propre.append(brin_ARN[j:j+3])
    j += 3
""",

"D": """# Bloc D
code_genet = {
'AUG':'Met',
'UUU':'Phe',
'UUC':'Phe',
'UAA':'STOP',
'UAG':'STOP',
'UGA':'STOP'
}
""",

"F": """# Bloc F
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
            for k in range(j,len(tab)):
                del tab[j]
            break
        j += 1

    return tab
""",

"G": """# Bloc G
resultat = nettoyage(brin_ARN_propre)
""",

"E": """# Bloc E
proteine = []

for codon in resultat:

    if codon in code_genet:

        if code_genet[codon]=="STOP":
            break

        proteine.append(code_genet[codon])

    else:
        proteine.append("Erreur")

print("-".join(proteine))
"""
}


ordre_correct = [
"C",
"B",
"A",
"D",
"F",
"G",
"E"
]


# ----------------------------
# Choix de l'élève
# ----------------------------

choix = st.multiselect(
    "Choisis l'ordre des blocs :",
    list(blocs.keys())
)


# affichage

if choix:

    st.subheader("Ton programme :")

    for lettre in choix:
        st.code(blocs[lettre], language="python")


# ----------------------------
# Vérification
# ----------------------------

if st.button("✅ Vérifier"):

    if choix == ordre_correct:

        st.success("Bravo ! Le programme est correct 🎉")

    else:

        st.error(
            "Ce n'est pas encore le bon ordre. Essaie encore."
        )


# ----------------------------
# Test ADN
# ----------------------------

st.divider()

st.subheader("Tester la traduction")

sequence = st.text_input(
    "Séquence ADN",
    "ATGGTTTAA"
)


if st.button("Traduire"):

    arn = sequence.upper().replace("T","U")

    codons = [
        arn[i:i+3]
        for i in range(0,len(arn),3)
    ]

    code = {
        'AUG':'Met',
        'UUU':'Phe',
        'UUC':'Phe',
        'UAA':'STOP',
        'UAG':'STOP',
        'UGA':'STOP'
    }

    proteine=[]

    for c in codons:

        if c in code:

            if code[c]=="STOP":
                break

            proteine.append(code[c])

    st.info(
        " → ".join(proteine)
    )
