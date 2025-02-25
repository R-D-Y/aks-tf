import subprocess
import json

def get_cf_info(endpoint, guid):
    """Utilise 'cf curl' pour récupérer des informations depuis Cloud Foundry."""
    try:
        result = subprocess.run(["cf", "curl", f"/v3/{endpoint}/{guid}"], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        print(f"Erreur lors de la récupération des données pour {endpoint} {guid}")
        return None

# Demande à l'utilisateur le GUID de l'instance problématique
service_instance_guid = input("Quelle est le GUID de l’instance de service qui ne marche pas ? ").strip()

# Récupérer les informations de l'instance
instance_data = get_cf_info("service_instances", service_instance_guid)

if instance_data:
    instance_name = instance_data.get("name", "Inconnu")
    instance_state = instance_data.get("last_operation", {}).get("state", "Inconnu")

    # Récupérer le nom du space
    space_guid = instance_data.get("relationships", {}).get("space", {}).get("data", {}).get("guid")
    space_name = "Inconnu"
    if space_guid:
        space_data = get_cf_info("spaces", space_guid)
        if space_data:
            space_name = space_data.get("name", "Inconnu")

    # Récupérer le nom de l'organisation
    org_guid = space_data.get("relationships", {}).get("organization", {}).get("data", {}).get("guid") if space_data else None
    org_name = "Inconnu"
    if org_guid:
        org_data = get_cf_info("organizations", org_guid)
        if org_data:
            org_name = org_data.get("name", "Inconnu")

    # Affichage des résultats
    print(f"\n🔴 Le service instance en problème est le suivant :")
    print(f"   - Instance de service : '{instance_name}'")
    print(f"   - Space : '{space_name}'")
    print(f"   - Organisation : '{org_name}'")
    print(f"   - État actuel : '{instance_state}'")
else:
    print("❌ Impossible de récupérer les informations de cette instance.")