import subprocess
import json

# GUIDs à renseigner
PCF_ORG_GUID = "your-org-guid"
PCF_SPACE_GUID = "your-space-guid"
PCF_INSTANCE_ID = "your-instance-id"

def get_cf_info(endpoint, guid):
    """Utilise 'cf curl' pour récupérer des informations depuis Cloud Foundry."""
    try:
        result = subprocess.run(["cf", "curl", f"/v3/{endpoint}/{guid}"], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        print(f"Erreur lors de la récupération des données pour {endpoint} {guid}")
        return None

# Récupérer les informations nécessaires
org_data = get_cf_info("organizations", PCF_ORG_GUID)
space_data = get_cf_info("spaces", PCF_SPACE_GUID)
instance_data = get_cf_info("service_instances", PCF_INSTANCE_ID)

if org_data and space_data and instance_data:
    org_name = org_data.get("name", "Inconnu")
    space_name = space_data.get("name", "Inconnu")
    instance_name = instance_data.get("name", "Inconnu")

    print(f"Instance '{instance_name}' de l'org '{org_name}' dans le space '{space_name}'")
else:
    print("Impossible de récupérer toutes les informations.")