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

def get_bind_count(instance_id):
    """Compte le nombre d'applications liées à une instance de service."""
    try:
        result = subprocess.run(["cf", "curl", f"/v3/service_credential_bindings?service_instance_guids={instance_id}"],
                                capture_output=True, text=True, check=True)
        bindings_data = json.loads(result.stdout)
        return bindings_data.get("pagination", {}).get("total_results", 0)
    except subprocess.CalledProcessError:
        print(f"Erreur lors de la récupération des bindings pour l'instance {instance_id}")
        return 0

# Récupérer les informations nécessaires
org_data = get_cf_info("organizations", PCF_ORG_GUID)
space_data = get_cf_info("spaces", PCF_SPACE_GUID)
instance_data = get_cf_info("service_instances", PCF_INSTANCE_ID)

if org_data and space_data and instance_data:
    org_name = org_data.get("name", "Inconnu")
    space_name = space_data.get("name", "Inconnu")
    instance_name = instance_data.get("name", "Inconnu")
    
    # Récupérer le type de service
    service_plan_url = instance_data.get("relationships", {}).get("service_plan", {}).get("data", {}).get("guid")
    service_type = "Inconnu"
    
    if service_plan_url:
        service_plan_data = get_cf_info("service_plans", service_plan_url)
        if service_plan_data:
            service_type = service_plan_data.get("name", "Inconnu")

    # Récupérer le nombre de bindings
    bind_count = get_bind_count(PCF_INSTANCE_ID)

    # Affichage des résultats
    print(f"Instance '{instance_name}' ({service_type}) de l'org '{org_name}' dans le space '{space_name}', liée à {bind_count} application(s).")
else:
    print("Impossible de récupérer toutes les informations.")