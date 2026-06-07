import streamlit as st
from streamlit_sortables import sort_items


st.set_page_config(
    page_title="Puzzle ADN → Protéine",
    page_icon="🧬"
)


st.title("🧬 Puzzle ADN → Protéine")

st.write(
    "Replace les blocs dans le bon ordre pour reconstruire le programme."
)


# =================================================
# Blocs du programme
# =================================================

blocs = [

{
"id": "B",
"code": """# Bloc B
brin_ARN = brin_ADN_propre.replace('T', 'U')"""
},


{
"id": "F",
"code": """# Bloc F
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


    return tab"""
},


{
"id": "C",
"code": """# Bloc C
brin_ADN = input("Entrez la séquence ADN : ")

brin_ADN_propre = brin_ADN.upper()"""
},


{
"id": "D",
"code": """# Bloc D

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
"id": "A",
"code": """# Bloc A

j = 0

brin_ARN_propre = []


while j < len(brin_ARN):

    brin_ARN_propre.append(
        brin_ARN[j:j+3]
    )

    j += 3"""
},


{
"id": "G",
"code": """# Bloc G

resultat = nettoyage(brin_ARN_propre)"""
},


{
"id": "E",
"code": """# Bloc E

print("Protéine correspondante :")


for codon in resultat:

    if codon in code_genet:

        if code_genet[codon] == "STOP":
            break


        print(
            code_genet[codon],
            end='-'
        )


    else:

        print(
            "Erreur codon",
            codon
        )

        break"""
}

]


# =================================================
# Zone puzzle
# =================================================

st.subheader("🧩 Déplace les blocs")


liste_depart = [
    "🧩 Bloc " + b["id"]
    for b in blocs
]


ordre = sort_items(
    liste_depart,
    direction="vertical"
)


for element in ordre:
    st.info(element)



# =================================================
# Reconstruction du code
# =================================================

st.subheader("📜 Programme reconstruit")


table = {
    "🧩 Bloc " + b["id"]: b["code"]
    for b in blocs
}


programme = ""


for bloc in ordre:

    programme += "\n\n"
    programme += table[bloc]


st.code(
    programme,
    language="python"
)



# =================================================
# Correction
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

        st.success(
            "Bravo 🎉 Le programme est correct !"
        )

    else:

        st.error(
            "Il faut encore modifier l'ordre des blocs."
        )
