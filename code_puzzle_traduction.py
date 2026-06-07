#version streamlite sans module tkinter
import streamlit as st
from streamlit_sortables import sort_items

st.set_page_config(page_title="Puzzle ADN", page_icon="🧬")

st.title("🧬 Puzzle ADN → Protéine")

blocs = [
    {
        "id": "C",
        "code": """brin_ADN = input("Entrez la séquence ADN :")
brin_ADN_propre = brin_ADN.upper()"""
    },
    {
        "id": "B",
        "code": """brin_ARN = brin_ADN_propre.replace('T','U')"""
    },
    {
        "id": "A",
        "code": """j = 0
brin_ARN_propre = []

while j < len(brin_ARN):
    brin_ARN_propre.append(brin_ARN[j:j+3])
    j += 3"""
    },
    {
        "id": "D",
        "code": """code_genet = {
'AUG':'Met',
'UUU':'Phe',
'UAA':'STOP'
}"""
    },
    {
        "id": "F",
        "code": """def nettoyage(tab):
    return tab"""
    },
    {
        "id": "G",
        "code": """resultat = nettoyage(brin_ARN_propre)"""
    },
    {
        "id": "E",
        "code": """for codon in resultat:
    print(codon)"""
    }
]


# affichage des blocs
elements = []

for b in blocs:
    elements.append(
        f"""
        🧩 Bloc {b['id']}

        {b['code']}
        """
    )


ordre = sort_items(
    elements,
    direction="vertical"
)


st.subheader("Programme reconstruit")

for bloc in ordre:
    st.code(bloc, language="python")


if st.button("✅ Vérifier"):

    solution = ["C","B","A","D","F","G","E"]

    st.write("Ordre obtenu :")
    st.write(ordre)
