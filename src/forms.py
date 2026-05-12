from datetime import date, datetime

import streamlit as st


def trajet_inputs(
    prefix: str,
    title: str,
    default_depart: str = "",
    default_arrivee: str = "",
) -> dict[str, str]:
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


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def missionnaire_inputs(profile: dict | None = None) -> dict:
    profile = profile or {}

    st.header("1. Missionnaire")

    col1, col2 = st.columns(2)

    with col1:
        nom = st.text_input("Nom", value=profile.get("nom", ""))
        prenom = st.text_input("Prénom", value=profile.get("prenom", ""))
        date_naissance = st.date_input(
            "Date de naissance",
            value=parse_date(
                profile.get("date_naissance", "2000-01-01")
            ),
        )
        mail = st.text_input("Mail", value=profile.get("mail", ""))
        telephone = st.text_input(
            "Téléphone portable",
            value=profile.get("telephone", ""),
        )

    with col2:
        adresse = st.text_input(
            "Adresse personnelle",
            value=profile.get("adresse", ""),
        )
        code_postal = st.text_input(
            "Code postal",
            value=profile.get("code_postal", ""),
        )
        ville = st.text_input("Ville", value=profile.get("ville", ""))
        nationalite = st.text_input(
            "Nationalité",
            value=profile.get("nationalite", "Française"),
        )
        profession = st.text_input(
            "Profession / qualité",
            value=profile.get("profession", ""),
        )

    return locals()


def mission_inputs() -> dict:
    st.header("2. Mission")

    motif_mission = st.text_area("Motif détaillé de la mission")

    col1, col2 = st.columns(2)
    with col1:
        date_depart_residence = st.date_input(
            "Date de départ de la résidence"
        )
    with col2:
        date_retour_residence = st.date_input(
            "Date de retour à la résidence"
        )

    return locals()


def signature_inputs(ville_default: str = "") -> dict:
    st.header("6. Signature")

    col1, col2 = st.columns(2)

    with col1:
        fait_a = st.text_input("Fait à", value=ville_default)
    with col2:
        date_signature = st.date_input(
            "Date de signature",
            value=date.today(),
        )

    return locals()