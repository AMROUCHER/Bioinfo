import streamlit as st
import sqlite3
import pandas as pd
import requests

# =========================
# BASE SQLITE
# =========================
conn = sqlite3.connect("genes.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS genes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    organisme TEXT,
    chromosome TEXT,
    start INTEGER,
    end INTEGER,
    sequence TEXT
)
""")
conn.commit()

# =========================
# IMPORT GENBANK (NCBI)
# =========================
def fetch_gene_from_ncbi(gene_name):
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "gene", "term": gene_name, "retmode": "json"}

    r = requests.get(search_url, params=params)
    data = r.json()

    ids = data.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return None

    gene_id = ids[0]

    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {"db": "gene", "id": gene_id, "retmode": "json"}

    r = requests.get(summary_url, params=params)
    data = r.json()

    info = data["result"][gene_id]

    return {
        "nom": gene_name,
        "organisme": info.get("organism", {}).get("scientificname", "unknown"),
        "chromosome": str(info.get("chromosome", "unknown")),
        "start": 0,
        "end": 0,
        "sequence": "NA (résumé GenBank)"
    }

# =========================
# STREAMLIT UI
# =========================
st.title("🧬 Mini navigateur génomique SVT")

menu = st.sidebar.selectbox(
    "Menu",
    ["Importer gène GenBank", "Voir base", "Navigateur chromosome"]
)

# =========================
# IMPORT GENBANK
# =========================
if menu == "Importer gène GenBank":

    st.subheader("🔎 Import automatique depuis GenBank (NCBI)")

    gene = st.text_input("Nom du gène (ex: EPAS1, BRCA1, TP53)")

    if st.button("Importer"):
        result = fetch_gene_from_ncbi(gene)

        if result:
            cursor.execute("""
                INSERT INTO genes (nom, organisme, chromosome, start, end, sequence)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                result["nom"],
                result["organisme"],
                result["chromosome"],
                result["start"],
                result["end"],
                result["sequence"]
            ))
            conn.commit()
            st.success(f"Gène {gene} importé 👍")
        else:
            st.error("Gène introuvable")

# =========================
# BASE
# =========================
elif menu == "Voir base":

    st.subheader("📋 Base de données")

    df = pd.read_sql_query("SELECT * FROM genes", conn)
    st.dataframe(df)

# =========================
# NAVIGATEUR CHROMOSOME
# =========================
elif menu == "Navigateur chromosome":

    st.subheader("🧬 Navigation chromosomique")

    chroms = pd.read_sql_query(
        "SELECT DISTINCT chromosome FROM genes",
        conn
    )

    if len(chroms) == 0:
        st.warning("Aucun gène dans la base")
    else:
        chrom_selected = st.selectbox(
            "Chromosome",
            chroms["chromosome"]
        )

        genes = pd.read_sql_query(
            "SELECT * FROM genes WHERE chromosome = ?",
            conn,
            params=(chrom_selected,)
        )

        st.write("### Gènes sur chromosome :", chrom_selected)

        # visualisation simple chromosome
        st.progress(50)

        for i, row in genes.iterrows():

            if st.button(f"🧬 {row['nom']}"):
                st.write("## Détails gène")
                st.write("Nom :", row["nom"])
                st.write("Organisme :", row["organisme"])
                st.write("Chromosome :", row["chromosome"])
                st.write("Position :", row["start"], "-", row["end"])
                st.code(row["sequence"])