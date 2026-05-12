from datetime import date
from pathlib import Path

import streamlit as st

from src.docx_renderer import render_ordre_mission


ROOT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = ROOT_DIR / "templates" / "ordre_mission_template.docx"
GENERATED_DIR = ROOT_DIR / "generated"

st.set_page_config(page_title="OM Editor", page_icon="📄")

st.title("📄 OM Editor")


def format_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def trajet_inputs(prefix: str, title: str, default_depart: str = "", default_arrivee: str = ""):
    st.markdown(f"### {title}")

    col1, col2 = st.columns(2)

    with col1:
        depart_ville = st.text_input(
            f"{title} - Ville de départ",
            value=default_depart,
            key=f"{prefix}_depart_ville",
        )
        date_depart = st.text_input(
            f"{title} - Date de départ (jj/mm/aa)",
            key=f"{prefix}_date_depart",
        )
        heure_depart = st.text_input(
            f"{title} - Heure de départ",
            key=f"{prefix}_heure_depart",
        )

    with col2:
        arrivee_ville = st.text_input(
            f"{title} - Ville d'arrivée",
            value=default_arrivee,
            key=f"{prefix}_arrivee_ville",
        )
        date_arrivee = st.text_input(
            f"{title} - Date d'arrivée (jj/mm/aa)",
            key=f"{prefix}_date_arrivee",
        )
        heure_arrivee = st.text_input(
            f"{title} - Heure d'arrivée",
            key=f"{prefix}_heure_arrivee",
        )

    return {
        f"{prefix}_depart_ville": depart_ville,
        f"{prefix}_date_depart": date_depart,
        f"{prefix}_heure_depart": heure_depart,
        f"{prefix}_arrivee_ville": arrivee_ville,
        f"{prefix}_date_arrivee": date_arrivee,
        f"{prefix}_heure_arrivee": heure_arrivee,
    }


with st.form("om_form"):
    st.header("1. Missionnaire")

    col1, col2 = st.columns(2)

    with col1:
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        date_naissance = st.date_input("Date de naissance", value=date(2000, 1, 1))
        mail = st.text_input("Mail")
        telephone = st.text_input("Téléphone portable")

    with col2:
        adresse = st.text_input("Adresse personnelle")
        code_postal = st.text_input("Code postal")
        ville = st.text_input("Ville")
        nationalite = st.text_input("Nationalité", value="Française")
        profession = st.text_input("Profession / qualité")

    st.header("2. Mission")

    motif_mission = st.text_area("Motif détaillé de la mission")

    col1, col2 = st.columns(2)
    with col1:
        date_depart_residence = st.date_input("Date de départ de la résidence")
    with col2:
        date_retour_residence = st.date_input("Date de retour à la résidence")

    st.header("3. Trajet aller")

    aller_1 = trajet_inputs("aller_1", "Aller 1", "Bruz", "Rennes")
    aller_2 = trajet_inputs("aller_2", "Aller 2", "Rennes", "")

    st.header("4. Trajet retour")

    retour_1 = trajet_inputs("retour_1", "Retour 1", "", "Rennes")
    retour_2 = trajet_inputs("retour_2", "Retour 2", "Rennes", "Bruz")

    st.header("5. Convenances personnelles")

    perso_1 = trajet_inputs("perso_1", "Période personnelle 1")
    perso_2 = trajet_inputs("perso_2", "Période personnelle 2")

    st.header("6. Signature")

    col1, col2 = st.columns(2)

    with col1:
        fait_a = st.text_input("Fait à", value=ville)
    with col2:
        date_signature = st.date_input("Date de signature", value=date.today())

    submitted = st.form_submit_button("Générer l'ordre de mission")


if submitted:
    context = {
        "nom": nom,
        "prenom": prenom,
        "date_naissance": format_date(date_naissance),
        "mail": mail,
        "telephone": telephone,
        "adresse": adresse,
        "code_postal": code_postal,
        "ville": ville,
        "nationalite": nationalite,
        "profession": profession,
        "motif_mission": motif_mission,
        "date_depart_residence": format_date(date_depart_residence),
        "date_retour_residence": format_date(date_retour_residence),
        "fait_a": fait_a,
        "date_signature": format_date(date_signature),
    }

    context.update(aller_1)
    context.update(aller_2)
    context.update(retour_1)
    context.update(retour_2)
    context.update(perso_1)
    context.update(perso_2)

    GENERATED_DIR.mkdir(exist_ok=True)

    output_path = GENERATED_DIR / f"OM_{nom}_{prenom}.docx"

    render_ordre_mission(
        template_path=TEMPLATE_PATH,
        output_path=output_path,
        context=context,
    )

    st.success("Ordre de mission généré.")

    with open(output_path, "rb") as file:
        st.download_button(
            label="Télécharger le document",
            data=file,
            file_name=output_path.name,
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),
        )