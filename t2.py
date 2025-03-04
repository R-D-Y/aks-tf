#!/bin/bash

# Fichier d'entrée contenant les IPs
INPUT_FILE="input.txt"
ABO_FILE="abo.txt"
OUTPUT_FILE="output.txt"

# En-tête du fichier de sortie
echo "Nom,Existe,IP,RessourceGroup,deployment,job" > "$OUTPUT_FILE"

# Parcourir chaque abonnement Azure
while IFS= read -r subscription; do
    echo "Changement d'abonnement : $subscription"
    az account set --subscription "$subscription"

    # Parcourir chaque IP du fichier input.txt
    while IFS= read -r ip; do
        echo "Recherche de l'IP : $ip"

        # Rechercher l'interface réseau associée à l'IP
        nic_id=$(az network nic list --query "[?ipConfigurations[0].privateIPAddress=='$ip'].id" -o tsv)

        if [[ -n "$nic_id" ]]; then
            # Récupérer le nom de la VM associée à cette carte réseau
            vm_name=$(az network nic show --ids "$nic_id" --query "virtualMachine.id" -o tsv | awk -F'/' '{print $9}')
            rg=$(az network nic show --ids "$nic_id" --query "resourceGroup" -o tsv)

            if [[ -n "$vm_name" ]]; then
                # Vérifier si la VM existe
                exists="oui"
                # Récupérer les tags deployment et job
                deployment=$(az vm show -g "$rg" -n "$vm_name" --query "tags.deployment" -o tsv 2>/dev/null || echo "N/A")
                job=$(az vm show -g "$rg" -n "$vm_name" --query "tags.job" -o tsv 2>/dev/null || echo "N/A")
            else
                exists="non"
                vm_name="N/A"
                deployment="N/A"
                job="N/A"
            fi
        else
            vm_name="N/A"
            exists="non"
            rg="N/A"
            deployment="N/A"
            job="N/A"
        fi

        # Écrire les résultats dans le fichier de sortie
        echo "$vm_name,$exists,$ip,$rg,$deployment,$job" >> "$OUTPUT_FILE"

    done < "$INPUT_FILE"

done < "$ABO_FILE"

echo "Traitement terminé. Résultats enregistrés dans $OUTPUT_FILE."