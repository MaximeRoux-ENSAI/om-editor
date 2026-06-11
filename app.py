from pathlib import Path

import streamlit as st

from src.context_builder import build_context, complete_trajets
from src.docx_renderer import render_ordre_mission
from src.forms import (
    accommodation_inputs,
    airplane_inputs,
    dynamic_trajets_inputs,
    mission_inputs,
    missionnaire_inputs,
    signature_inputs,
    subscription_inputs,
    vehicle_inputs,
)
from src.mission_type_loader import load_mission_types
from src.profile_loader import load_profiles
from src.validators import validate_form


ROOT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT_DIR / "templates"
GENERATED_DIR = ROOT_DIR / "generated"
PROFILES_PATH = ROOT_DIR / "data" / "profils.yaml"
MISSION_TYPES_PATH = ROOT_DIR / "data" / "mission_types.yaml"

STATUT_LABELS = {
    "eleve": "Élève",
    "agent": "Agent",
}

RESIDENCE_LABELS = {
    "familiale": "Familiale",
    "administrative": "Administrative",
}

RESIDENCE_TEMPLATE_DIRS = {
    "familiale": "Familiale",
    "administrative": "Administrative",
}

TRANSPORT_LABELS = {
    "train": "Train",
    "abonnement": "Train avec carte d'abonnement",
    "voiture": "Voiture",
    "train_avion": "Train + avion",
}


def select_template(
    statut: str,
    transport: str,
    trajets_aller: list[dict[str, str]],
    trajets_retour: list[dict[str, str]],
    accommodation: dict,
) -> tuple[str, int]:
    """Select the appropriate DOCX template.

    Parameters
    ----------
    statut:
        Missionnaire status: `agent` or `eleve`.
    transport:
        Selected transport mode.
    trajets_aller:
        List of outbound trip segments.
    trajets_retour:
        List of return trip segments.
    accommodation:
        Accommodation information.

    Returns
    -------
    tuple[str, int]
        Template filename and number of trip lines expected by the template.
    """
    if transport == "voiture":
        return (
            f"ordre_mission_template_{statut}_voiture_3_lignes.docx",
            3,
        )

    if transport == "train_avion":
        return (
            f"ordre_mission_template_{statut}_train_avion_5_lignes.docx",
            5,
        )

    max_selected_trajets = max(
        len(trajets_aller),
        len(trajets_retour),
    )

    template_lines = 3 if max_selected_trajets <= 3 else 5
    hebergement_type = accommodation.get("hebergement_type", "aucun")

    if transport == "abonnement":
        if hebergement_type == "hotel":
            return (
                f"ordre_mission_template_{statut}_abonnement_hotel_"
                f"{template_lines}_lignes.docx",
                template_lines,
            )

        if hebergement_type == "autre":
            return (
                f"ordre_mission_template_{statut}_abonnement_hotel_autre_"
                f"{template_lines}_lignes.docx",
                template_lines,
            )

        return (
            f"ordre_mission_template_{statut}_abonnement_"
            f"{template_lines}_lignes.docx",
            template_lines,
        )

    if hebergement_type == "hotel":
        return (
            f"ordre_mission_template_{statut}_hotel_"
            f"{template_lines}_lignes.docx",
            template_lines,
        )

    if hebergement_type == "autre":
        return (
            f"ordre_mission_template_{statut}_hotel_autre_"
            f"{template_lines}_lignes.docx",
            template_lines,
        )

    return (
        f"ordre_mission_template_{statut}_{template_lines}_lignes.docx",
        template_lines,
    )


def get_template_path(residence: str, template_name: str) -> Path:
    """Build the template path for the selected residence type."""
    return TEMPLATES_DIR / RESIDENCE_TEMPLATE_DIRS[residence] / template_name


def load_local_data() -> tuple[dict, dict]:
    """Load local YAML configuration files.

    Returns
    -------
    tuple[dict, dict]
        Missionnaire profiles and mission type presets.
    """
    profiles = load_profiles(PROFILES_PATH)
    mission_types = load_mission_types(MISSION_TYPES_PATH)

    return profiles, mission_types


def main() -> None:
    """Run the Streamlit application."""
    profiles, mission_types = load_local_data()

    st.set_page_config(
        page_title="OM Editor",
        page_icon="📄",
        layout="wide",
    )

    st.title("📄 OM Editor")
    st.caption(
        "Génération automatique d'ordres de mission ENSAI / GENES"
    )

    profile_names = ["Aucun"] + list(profiles.keys())

    selected_profile_name = st.selectbox(
        "Profil missionnaire",
        profile_names,
    )

    selected_profile = (
        {}
        if selected_profile_name == "Aucun"
        else profiles.get(selected_profile_name, {})
    )

    mission_type_options = {
        key: value.get("label", key)
        for key, value in mission_types.items()
    }

    selected_mission_type_key = st.selectbox(
        "Type de mission",
        list(mission_type_options.keys()),
        format_func=lambda key: mission_type_options[key],
    )

    selected_mission_type = mission_types.get(
        selected_mission_type_key,
        {},
    )

    statut = st.radio(
        "Statut",
        list(STATUT_LABELS),
        index=0,
        format_func=lambda value: STATUT_LABELS[value],
        horizontal=True,
    )

    residence = st.radio(
        "Résidence de départ et de retour",
        list(RESIDENCE_LABELS),
        index=0,
        format_func=lambda value: RESIDENCE_LABELS[value],
        horizontal=True,
    )

    transport = st.radio(
        "Mode de transport",
        list(TRANSPORT_LABELS),
        format_func=lambda value: TRANSPORT_LABELS[value],
        horizontal=True,
    )

    with st.form("om_form"):
        missionnaire = missionnaire_inputs(selected_profile)
        mission = mission_inputs(selected_mission_type)

        if transport == "voiture":
            max_trajets = 3
            default_trajets = 1
        else:
            max_trajets = 5
            default_trajets = 2

        trajets_aller = dynamic_trajets_inputs(
            prefix="aller",
            title="Trajet aller",
            min_value=1,
            max_value=max_trajets,
            default_value=default_trajets,
        )

        trajets_retour = dynamic_trajets_inputs(
            prefix="retour",
            title="Trajet retour",
            min_value=1,
            max_value=max_trajets,
            default_value=default_trajets,
        )

        periodes_perso = dynamic_trajets_inputs(
            prefix="perso",
            title="Convenances personnelles",
            min_value=0,
            max_value=3,
            default_value=0,
        )

        vehicle = {}
        subscription = {}
        airplane = {}
        accommodation = {}

        if transport == "voiture":
            vehicle = vehicle_inputs()

        if transport == "abonnement":
            subscription = subscription_inputs()

        if transport == "train_avion":
            airplane = airplane_inputs()

        if transport != "voiture":
            accommodation = accommodation_inputs()

        signature = signature_inputs(missionnaire["ville"])

        submitted = st.form_submit_button(
            "Générer l'ordre de mission"
        )

    if not submitted:
        return

    template_name, template_lines = select_template(
        statut=statut,
        transport=transport,
        trajets_aller=trajets_aller,
        trajets_retour=trajets_retour,
        accommodation=accommodation,
    )

    template_path = get_template_path(
        residence=residence,
        template_name=template_name,
    )
    template_relative_path = template_path.relative_to(ROOT_DIR)

    if not template_path.exists():
        st.error(
            "Le template attendu est introuvable : "
            f"`{template_relative_path}`"
        )
        st.stop()

    trajets = []
    trajets.extend(
        complete_trajets(
            trajets_aller,
            prefix="aller",
            max_count=template_lines,
        )
    )
    trajets.extend(
        complete_trajets(
            trajets_retour,
            prefix="retour",
            max_count=template_lines,
        )
    )
    trajets.extend(
        complete_trajets(
            periodes_perso,
            prefix="perso",
            max_count=3,
        )
    )

    if not validate_form(
        missionnaire=missionnaire,
        mission=mission,
        trajets=trajets,
        vehicle=vehicle,
        subscription=subscription,
    ):
        st.stop()

    context = build_context(
        missionnaire=missionnaire,
        mission=mission,
        signature=signature,
        trajets=trajets,
        vehicle=vehicle,
        subscription=subscription,
        airplane=airplane,
        accommodation=accommodation,
    )

    GENERATED_DIR.mkdir(exist_ok=True)

    output_path = GENERATED_DIR / (
        f"OM_{context['nom']}_{context['prenom']}_"
        f"{statut}_{residence}_{transport}.docx"
    )

    render_ordre_mission(
        template_path=template_path,
        output_path=output_path,
        context=context,
    )

    st.success(
        "Ordre de mission généré avec le template : "
        f"`{template_relative_path}`"
    )

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


if __name__ == "__main__":
    main()
