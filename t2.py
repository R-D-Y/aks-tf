#!/bin/bash

# Fichiers
INPUT_FILE="input.txt"
ABO_FILE="abo.txt"
OUTPUT_FILE="output.txt"

# En-tête du fichier de sortie
echo "Nom,Existe,IP,RessourceGroup,deployment,job" > "$OUTPUT_FILE"

# Parcourir chaque IP du fichier input.txt (sans doublons)
while IFS= read -r ip; do
    echo "Recherche de l'IP : $ip"

    vm_name="N/A"
    exists="non"
    rg="N/A"
    deployment="N/A"
    job="N/A"
    
    # Parcourir chaque abonnement Azure jusqu'à trouver l'IP
    while IFS= read -r subscription && [[ "$exists" == "non" ]]; do
        echo "Vérification dans l'abonnement : $subscription"
        az account set --subscription "$subscription"

        # Rechercher la carte réseau associée à l'IP
        nic_id=$(az network nic list --query "[?ipConfigurations[0].privateIPAddress=='$ip'].id" -o tsv)

        if [[ -n "$nic_id" ]]; then
            # Récupérer le nom de la VM et le RG
            vm_name=$(az network nic show --ids "$nic_id" --query "virtualMachine.id" -o tsv | awk -F'/' '{print $9}')
            rg=$(az network nic show --ids "$nic_id" --query "resourceGroup" -o tsv)

            if [[ -n "$vm_name" ]]; then
                exists="oui"
                # Récupérer les tags deployment et job
                deployment=$(az vm show -g "$rg" -n "$vm_name" --query "tags.deployment" -o tsv 2>/dev/null || echo "N/A")
                job=$(az vm show -g "$rg" -n "$vm_name" --query "tags.job" -o tsv 2>/dev/null || echo "N/A")
            fi
        fi
    done < "$ABO_FILE"

    # Écrire les résultats dans le fichier de sortie
    echo "$vm_name,$exists,$ip,$rg,$deployment,$job" >> "$OUTPUT_FILE"

done < "$INPUT_FILE"

echo "Traitement terminé. Résultats enregistrés dans $OUTPUT_FILE."