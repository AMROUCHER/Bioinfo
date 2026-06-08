import streamlit as st
from streamlit_sortables import sort_items
import io
import contextlib


st.set_page_config(
    page_title="Puzzle ADN Python",
    page_icon="🧬"
)


st.title("🧬 Puzzle Python : ADN → Protéine")


# ==========================
# Saisie élève
# ==========================

brin_ADN = st.text_input(
    "Entre une séquence ADN :",
    "ATGGTTTAA"
)


# ==========================
# Blocs Python
# ==========================

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

for i in range(0,len(brin_ARN),3):

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
"UAA":"STOP"

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

print(
"Protéine :"
)

print(
"-".join(resultat)
)
"""
}

]


# ==========================
# Préparation
# ==========================

noms = [
"🟥 Bloc "+b["id"]
for b in blocs
]


codes = {
"🟥 Bloc "+b["id"]:b["code"]
for b in blocs
}



# ==========================
# Puzzle
# ==========================

st.subheader("🟥 Déplace les blocs")


ordre = sort_items(
    noms,
    direction="vertical"
)


for bloc in ordre:

    lignes = codes[bloc].split("\n")

    apercu = "\n".join(
        lignes[:4]
    )

    st.error(
        bloc+"\n\n"+apercu
    )



# ==========================
# Code final
# ==========================

st.divider()

st.subheader("📜 Code reconstruit")


programme = ""


for bloc in ordre:

    programme += "\n"
    programme += codes[bloc]


st.code(
    programme,
    language="python"
)



# ==========================
# Execution
# ==========================

st.divider()

st.subheader("▶️ Console Python")


if st.button("Lancer"):

    sortie = io.StringIO()

    try:

        with contextlib.redirect_stdout(sortie):

            exec(
                programme,
                {
                "brin_ADN":brin_ADN,
                "st":st
                }
            )


        texte = sortie.getvalue()


        st.success("Programme terminé")

        st.code(
            texte,
            language="text"
        )


    except Exception as e:

        st.error("Erreur Python")

        st.code(
            str(e),
            language="text"
        )
