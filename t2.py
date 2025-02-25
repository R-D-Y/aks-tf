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

def main():
    # Demander le GUID de l'instance en problème
    service_instance_guid = input("Quelle est le GUID de l’instance de service qui ne marche pas ? ").strip()

    # Récupérer les informations de l'instance
    instance_data = get_cf_info("service_instances", service_instance_guid)
    if not instance_data:
        print("Impossible de récupérer les informations de l’instance.")
        return

    # Récupérer les détails
    instance_name = instance_data.get("name", "Inconnu")
    instance_state = instance_data.get("last_operation", {}).get("state", "Inconnu")
    
    # Récupérer le space GUID et son nom
    space_guid = instance_data.get("relationships", {}).get("space", {}).get("data", {}).get("guid")
    space_name = "Inconnu"
    
    if space_guid:
        space_data = get_cf_info("spaces", space_guid)
        if space_data:
            space_name = space_data.get("name", "Inconnu")
    
    # Récupérer le org GUID et son nom
    org_guid = space_data.get("relationships", {}).get("organization", {}).get("data", {}).get("guid") if space_data else None
    org_name = "Inconnu"

    if org_guid:
        org_data = get_cf_info("organizations", org_guid)
        if org_data:
            org_name = org_data.get("name", "Inconnu")

    # Affichage des résultats
    print(f"Le service instance en problème est le suivant :")
    print(f"Instance de service '{instance_name}' du space '{space_name}' de l'org '{org_name}' est dans l’état '{instance_state}'.")
    
if __name__ == "__main__":
    main()