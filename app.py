from pathlib import Path

import streamlit as st

from src.context_builder import build_context
from src.docx_renderer import render_ordre_mission
from src.forms import mission_inputs, missionnaire_inputs, signature_inputs
from src.forms import trajet_inputs
from src.mission_type_loader import load_mission_types
from src.profile_loader import load_profiles


ROOT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = ROOT_DIR / "templates" / "ordre_mission_template.docx"
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

if selected_profile_name == "Aucun":
    selected_profile = {}
else:
    selected_profile = profiles.get(selected_profile_name, {})

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

with st.form("om_form"):
    missionnaire = missionnaire_inputs(selected_profile)
    mission = mission_inputs(selected_mission_type)

    st.header("3. Trajet aller")
    aller_1 = trajet_inputs("aller_1", "Aller 1", "Bruz", "Rennes")
    aller_2 = trajet_inputs("aller_2", "Aller 2", "Rennes", "")

    st.header("4. Trajet retour")
    retour_1 = trajet_inputs("retour_1", "Retour 1", "", "Rennes")
    retour_2 = trajet_inputs("retour_2", "Retour 2", "Rennes", "Bruz")

    st.header("5. Convenances personnelles")
    perso_1 = trajet_inputs("perso_1", "Période personnelle 1")
    perso_2 = trajet_inputs("perso_2", "Période personnelle 2")

    signature = signature_inputs(missionnaire["ville"])

    submitted = st.form_submit_button("Générer l'ordre de mission")

if submitted:
    context = build_context(
        missionnaire=missionnaire,
        mission=mission,
        signature=signature,
        trajets=[
            aller_1,
            aller_2,
            retour_1,
            retour_2,
            perso_1,
            perso_2,
        ],
    )

    GENERATED_DIR.mkdir(exist_ok=True)

    output_path = (
        GENERATED_DIR
        / f"OM_{context['nom']}_{context['prenom']}.docx"
    )

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