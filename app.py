from pathlib import Path

import streamlit as st

from src.context_builder import build_context, complete_trajets
from src.docx_renderer import render_ordre_mission
from src.forms import dynamic_trajets_inputs
from src.forms import mission_inputs, missionnaire_inputs, signature_inputs
from src.forms import subscription_inputs, vehicle_inputs
from src.mission_type_loader import load_mission_types
from src.profile_loader import load_profiles
from src.validators import validate_form


ROOT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT_DIR / "templates"
GENERATED_DIR = ROOT_DIR / "generated"
PROFILES_PATH = ROOT_DIR / "data" / "profils.yaml"
MISSION_TYPES_PATH = ROOT_DIR / "data" / "mission_types.yaml"

profiles = load_profiles(PROFILES_PATH)
mission_types = load_mission_types(MISSION_TYPES_PATH)

st.set_page_config(page_title="OM Editor", page_icon="📄")
st.title("📄 OM Editor")

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
    ["agent", "eleve"],
    format_func=lambda value: "Agent" if value == "agent" else "Élève",
    horizontal=True,
)

transport = st.radio(
    "Mode de transport",
    ["train", "abonnement", "voiture"],
    format_func=lambda value: {
        "train": "Train",
        "abonnement": "Train avec carte d'abonnement",
        "voiture": "Voiture",
    }[value],
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

    if transport == "voiture":
        vehicle = vehicle_inputs()

    if transport == "abonnement":
        subscription = subscription_inputs()

    signature = signature_inputs(missionnaire["ville"])

    submitted = st.form_submit_button("Générer l'ordre de mission")

if submitted:
    if transport == "voiture":
        template_lines = 3
        template_name = (
            f"ordre_mission_template_{statut}_voiture_3_lignes.docx"
        )

    elif transport == "abonnement":
        max_selected_trajets = max(
            len(trajets_aller),
            len(trajets_retour),
        )

        if max_selected_trajets <= 3:
            template_lines = 3
            template_name = (
                f"ordre_mission_template_{statut}_abonnement_3_lignes.docx"
            )
        else:
            template_lines = 5
            template_name = (
                f"ordre_mission_template_{statut}_abonnement_5_lignes.docx"
            )

    else:
        max_selected_trajets = max(
            len(trajets_aller),
            len(trajets_retour),
        )

        if max_selected_trajets <= 3:
            template_lines = 3
            template_name = (
                f"ordre_mission_template_{statut}_3_lignes.docx"
            )
        else:
            template_lines = 5
            template_name = (
                f"ordre_mission_template_{statut}_5_lignes.docx"
            )

    template_path = TEMPLATES_DIR / template_name

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
    )

    GENERATED_DIR.mkdir(exist_ok=True)

    output_path = GENERATED_DIR / (
        f"OM_{context['nom']}_{context['prenom']}_{statut}_{transport}.docx"
    )

    render_ordre_mission(
        template_path=template_path,
        output_path=output_path,
        context=context,
    )

    st.success(f"Ordre de mission généré avec le template : `{template_name}`")

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