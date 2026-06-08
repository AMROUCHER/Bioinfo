import streamlit as st
from streamlit_sortables import sort_items
import io
import contextlib


st.set_page_config(
    page_title="Puzzle ADN Python",
    page_icon="🧬"
)


st.title("🧬 Puzzle Python : ADN → Protéine")


# =================================================
# Séquence ADN entrée par l'élève
# =================================================

brin_ADN = st.text_input(
    "Entre une séquence ADN :",
    "ATGGTTTAA"
)


# =================================================
# Blocs Python à remettre dans l'ordre
# =================================================

blocs = [

{
"id":"C",
"code":
"""# Bloc C

brin_ADN_propre = brin_ADN.upper()
"""
},


{
"id":"B",
"code":
"""# Bloc B

brin_ARN = brin_ADN_propre.replace(
    "T",
    "U"
)
"""
},


{
"id":"A",
"code":
"""# Bloc A

brin_ARN_propre = []

for i in range(0, len(brin_ARN), 3):

    brin_ARN_propre.append(
        brin_ARN[i:i+3]
    )
"""
},


{
"id":"D",
"code":
"""# Bloc D

code_genet = {

    "AUG":"Met",
    "UUU":"Phe",
    "UUC":"Phe",
    "UAA":"STOP",
    "UAG":"STOP"

}
"""
},


{
"id":"F",
"code":
"""# Bloc F

resultat = []


for codon in brin_ARN_propre:

    if codon in code_genet:

        if code_genet[codon]=="STOP":
            break

        resultat.append(
            code_genet[codon]
        )
"""
},


{
"id":"E",
"code":
"""# Bloc E

print("Protéine :")

print(
    "-".join(resultat)
)
"""
}

]


# =================================================
# Préparation des blocs
# =================================================

noms = [
    "🟥 Bloc " + b["id"]
    for b in blocs
]


codes = {
    "🟥 Bloc " + b["id"]: b["code"]
    for b in blocs
}



# =================================================
# Déplacement
# =================================================

st.subheader("🟥 Déplace les blocs")


ordre = sort_items(
    noms,
    direction="vertical"
)



# =================================================
# Code reconstruit
# =================================================

st.divider()

st.subheader("📜 Code Python reconstruit")


programme = ""


for bloc in ordre:

    programme += "\n\n"
    programme += codes[bloc]


st.code(
    programme,
    language="python"
)



# =================================================
# Exécution
# =================================================

st.divider()

st.subheader("▶️ Console Python")


if st.button("Lancer le programme"):


    sortie = io.StringIO()


    try:

        with contextlib.redirect_stdout(sortie):

            exec(
                programme,
                {
                    "brin_ADN": brin_ADN
                }
            )


        resultat = sortie.getvalue()


        if resultat:

            st.success("Résultat Python :")

            st.code(
                resultat,
                language="text"
            )

        else:

            st.info(
                "Le programme s'est exécuté sans afficher de résultat."
            )


    except Exception as erreur:


        st.error(
            "Erreur Python :"
        )


        st.code(
            str(erreur),
            language="text"
        )
