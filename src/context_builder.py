from datetime import date


def format_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")

def empty_trajet(prefix: str, index: int) -> dict[str, str]:
    return {
        f"{prefix}_{index}_depart_ville": "",
        f"{prefix}_{index}_date_depart": "",
        f"{prefix}_{index}_heure_depart": "",
        f"{prefix}_{index}_arrivee_ville": "",
        f"{prefix}_{index}_date_arrivee": "",
        f"{prefix}_{index}_heure_arrivee": "",
    }


def complete_trajets(
    trajets: list[dict[str, str]],
    prefix: str,
    max_count: int,
) -> list[dict[str, str]]:
    completed = trajets.copy()

    for index in range(len(completed) + 1, max_count + 1):
        completed.append(empty_trajet(prefix, index))

    return completed

def build_context(
    missionnaire: dict,
    mission: dict,
    signature: dict,
    trajets: list[dict[str, str]],
) -> dict:
    context = {
        "nom": missionnaire["nom"],
        "prenom": missionnaire["prenom"],
        "date_naissance": format_date(missionnaire["date_naissance"]),
        "mail": missionnaire["mail"],
        "telephone": missionnaire["telephone"],
        "adresse": missionnaire["adresse"],
        "code_postal": missionnaire["code_postal"],
        "ville": missionnaire["ville"],
        "nationalite": missionnaire["nationalite"],
        "profession": missionnaire["profession"],
        "motif_mission": mission["motif_mission"],
        "date_depart_residence": format_date(
            mission["date_depart_residence"]
        ),
        "date_retour_residence": format_date(
            mission["date_retour_residence"]
        ),
        "fait_a": signature["fait_a"],
        "date_signature": format_date(signature["date_signature"]),
    }

    for trajet in trajets:
        context.update(trajet)

    return context