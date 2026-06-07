import streamlit as st
from streamlit_sortables import sort_items


st.set_page_config(
    page_title="Puzzle ADN → Protéine",
    page_icon="🧬"
)

st.title("🧬 Puzzle ADN → Protéine")

st.write("Déplace les blocs pour reconstruire le programme.")


# =================================================
# BLocs
# =================================================

blocs = [

{
"id":"C",
"code":"""# Bloc C
brin_ADN = st.text_input("Entrez la séquence ADN :", "ATGGTTTAA")
brin_ADN_propre = brin_ADN.upper()"""
},

{
"id":"B",
"code":"""# Bloc B
brin_ARN = brin_ADN_propre.replace('T','U')"""
},

{
"id":"A",
"code":"""# Bloc A
j = 0
brin_ARN_propre = []

while j < len(brin_ARN):
    brin_ARN_propre.append(brin_ARN[j:j+3])
    j += 3"""
},

{
"id":"D",
"code":"""# Bloc D
code_genet = {
'AUG':'Met',
'UUU':'Phe',
'UUC':'Phe',
'UAA':'STOP',
'UAG':'STOP',
'UGA':'STOP'
}"""
},

{
"id":"F",
"code":"""# Bloc F
def nettoyage(tab):

    j = 0

    for i in tab:

        if tab[j]=='AUG':

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

    return tab"""
},

{
"id":"G",
"code":"""# Bloc G
resultat = nettoyage(brin_ARN_propre)"""
},

{
"id":"E",
"code":"""# Bloc E
print("Protéine correspondante :")

for codon in resultat:

    if codon in code_genet:

        if code_genet[codon]=="STOP":
            break

        print(code_genet[codon], end='-')

    else:
        print("Erreur codon", codon)
        break"""
}

]


# =================================================
# Préparation
# =================================================

noms = [
    "🧩 Bloc " + b["id"]
    for b in blocs
]

codes = {
    "🧩 Bloc " + b["id"]: b["code"]
    for b in blocs
}


# =================================================
# PUZZLE
# =================================================

st.subheader("🧩 Déplace les blocs")

ordre = sort_items(
    noms,
    direction="vertical"
)


for bloc in ordre:

    lignes = codes[bloc].split("\n")

    if len(lignes) > 3:
        apercu = "\n".join(lignes[:3]) + "\n..."
    else:
        apercu = "\n".join(lignes)

    st.info(bloc + "\n\n" + apercu)


# =================================================
# CODE RECONSTRUIT
# =================================================

st.divider()

st.subheader("📜 Programme reconstruit")

programme = ""

for bloc in ordre:
    programme += "\n\n" + codes[bloc]

st.code(programme, language="python")


# =================================================
# EXÉCUTION RÉELLE
# =================================================

st.divider()

st.subheader("🐍 Exécution du programme")

if st.button("▶️ Lancer"):

    try:
        exec_globals = {"st": st}

        exec(programme, exec_globals)

    except Exception as e:

        st.error(f"Erreur : {e}")


# =================================================
# VÉRIFICATION
# =================================================

solution = [
"🧩 Bloc C",
"🧩 Bloc B",
"🧩 Bloc A",
"🧩 Bloc D",
"🧩 Bloc F",
"🧩 Bloc G",
"🧩 Bloc E"
]


if st.button("✅ Vérifier"):

    if ordre == solution:

        st.success("🎉 Bravo ! Ordre correct.")

    else:

        st.warning("❌ Ordre incorrect, essaie encore.")
