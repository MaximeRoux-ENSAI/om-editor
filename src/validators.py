from datetime import datetime

import streamlit as st


def is_empty(value: object) -> bool:
    """Return True if a value should be considered empty."""
    return value is None or str(value).strip() == ""


def validate_required_fields(
    missionnaire: dict,
    mission: dict,
) -> bool:
    """Validate required missionnaire and mission fields."""
    required_fields = {
        "Nom": missionnaire.get("nom"),
        "Prénom": missionnaire.get("prenom"),
        "Mail": missionnaire.get("mail"),
        "Motif détaillé de la mission": mission.get("motif_mission"),
    }

    errors = [
        f"Le champ « {label} » est obligatoire."
        for label, value in required_fields.items()
        if is_empty(value)
    ]

    for error in errors:
        st.error(error)

    return not errors


def validate_mission_dates(mission: dict) -> bool:
    """Validate chronological consistency of mission dates."""
    date_depart = mission.get("date_depart_residence")
    date_retour = mission.get("date_retour_residence")

    if date_depart and date_retour and date_retour < date_depart:
        st.error(
            "La date de retour à la résidence ne peut pas être "
            "antérieure à la date de départ."
        )
        return False

    return True


def validate_hour(value: str, label: str) -> bool:
    """Validate one hour field formatted as HH:MM."""
    if is_empty(value):
        return True

    try:
        datetime.strptime(value, "%H/%M")
    except ValueError:
        st.error(
            f"L'heure « {label} » doit être au format HH/MM "
            "(exemple : 17/09)."
        )
        return False

    return True


def validate_trajets(trajets: list[dict[str, str]]) -> bool:
    """Validate trip segment hours."""
    valid = True

    for trajet in trajets:
        for key, value in trajet.items():
            if key.endswith("_heure_depart") or key.endswith("_heure_arrivee"):
                valid = validate_hour(value, key) and valid

    return valid


def validate_vehicle(vehicle: dict) -> bool:
    """Validate vehicle fields when car transport is selected."""
    if not vehicle:
        return True

    required_fields = {
        "Type de véhicule": vehicle.get("type_vehicule"),
        "Motif d'utilisation du véhicule": vehicle.get("motif_vehicule"),
        "Kilométrage prévu": vehicle.get("kilometrage_vehicule"),
    }

    errors = [
        f"Le champ « {label} » est obligatoire pour un trajet en voiture."
        for label, value in required_fields.items()
        if is_empty(value)
    ]

    if vehicle.get("type_vehicule") == "personnel" and is_empty(
        vehicle.get("immatriculation_vehicule")
    ):
        errors.append(
            "L'immatriculation est obligatoire pour un véhicule personnel."
        )

    for error in errors:
        st.error(error)

    return not errors


def validate_subscription(subscription: dict) -> bool:
    """Validate subscription fields when a transport card is selected."""
    if not subscription:
        return True

    required_fields = {
        "Nom de la carte": subscription.get("nom_carte_abonnement"),
        "Numéro de carte": subscription.get("numero_carte_abonnement"),
        "Début de validité": subscription.get(
            "debut_validite_carte_abonnement"
        ),
        "Fin de validité": subscription.get(
            "fin_validite_carte_abonnement"
        ),
    }

    errors = [
        f"Le champ « {label} » est obligatoire pour une carte d'abonnement."
        for label, value in required_fields.items()
        if is_empty(value)
    ]

    for error in errors:
        st.error(error)

    return not errors


def validate_form(
    missionnaire: dict,
    mission: dict,
    trajets: list[dict[str, str]],
    vehicle: dict | None = None,
    subscription: dict | None = None,
) -> bool:
    """Run all form validations before document generation."""
    validations = [
        validate_required_fields(missionnaire, mission),
        validate_mission_dates(mission),
        validate_trajets(trajets),
        validate_vehicle(vehicle or {}),
        validate_subscription(subscription or {}),
    ]

    return all(validations)