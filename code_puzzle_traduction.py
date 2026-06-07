import streamlit as st
from streamlit_sortables import sort_items


st.set_page_config(
    page_title="Puzzle ADN → Protéine",
    page_icon="🧬"
)


st.title("🧬 Puzzle ADN → Protéine")

st.write(
    "Replace les blocs pour reconstruire le programme."
)


# =================================================
# Blocs du programme
# =================================================

blocs = [

{
"id":"C",
"code":"""# Bloc C
brin_ADN = input("Entrez la séquence ADN : ")
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
    "🧩 Bloc "+b["id"]: b["code"]
    for b in blocs
}



# =================================================
# Puzzle
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

    st.info(
        bloc + "\n\n" + apercu
    )



# =================================================
# Reconstruction
# =================================================

st.divider()

st.subheader("📜 Programme reconstruit")


programme = ""


for bloc in ordre:

    programme += "\n\n"
    programme += codes[bloc]


st.code(
    programme,
    language="python"
)



# =================================================
# Vérification
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
            "🎉 Bravo ! Le programme est correct."
        )


        st.subheader("🐍 Retour Python")


        brin_ADN = "ATGGTTTAA"

        brin_ADN_propre = brin_ADN.upper()

        brin_ARN = brin_ADN_propre.replace(
            "T","U"
        )


        brin_ARN_propre = []

        for i in range(0,len(brin_ARN),3):

            brin_ARN_propre.append(
                brin_ARN[i:i+3]
            )


        code_genet = {

            'AUG':'Met',
            'UUU':'Phe',
            'UUC':'Phe',
            'UAA':'STOP',
            'UAG':'STOP',
            'UGA':'STOP'
        }


        proteine=[]


        for codon in brin_ARN_propre:

            if codon in code_genet:

                if code_genet[codon]=="STOP":
                    break

                proteine.append(
                    code_genet[codon]
                )


        st.code(
            "Protéine correspondante :\n\n"
            +
            "-".join(proteine),
            language="text"
        )


    else:


        st.warning(
            "⚠️ Ordre incorrect"
        )


        st.subheader(
            "Ce que Python reçoit :"
        )


        st.code(
            programme,
            language="python"
        )
