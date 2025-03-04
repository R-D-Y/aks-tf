#!/bin/bash

# Fichiers d'entrée et de sortie
INPUT_FILE="input.txt"
SUBSCRIPTIONS_FILE="abo.txt"
OUTPUT_FILE="output.txt"

# En-tête du fichier de sortie
echo "Nom,Existe,IP,RessourceGroup,deployment,job" > "$OUTPUT_FILE"

# Parcourir chaque abonnement
while read -r SUB_ID; do
    echo "Traitement de l'abonnement : $SUB_ID"
    az account set --subscription "$SUB_ID"

    # Parcourir chaque IP
    while read -r IP; do
        # Rechercher la VM correspondant à l'IP
        VM_INFO=$(az vm list --query "[?networkProfile.networkInterfaces[].ipConfigurations[].privateIPAddress=='$IP']" -o json)

        if [[ "$VM_INFO" == "[]" ]]; then
            echo "N/A,Non,$IP,N/A,N/A,N/A" >> "$OUTPUT_FILE"
        else
            VM_NAME=$(echo "$VM_INFO" | jq -r '.[0].name')
            RG=$(echo "$VM_INFO" | jq -r '.[0].resourceGroup')
            TAG_DEPLOYMENT=$(echo "$VM_INFO" | jq -r '.[0].tags.deployment // "N/A"')
            TAG_JOB=$(echo "$VM_INFO" | jq -r '.[0].tags.job // "N/A"')

            echo "$VM_NAME,Oui,$IP,$RG,$TAG_DEPLOYMENT,$TAG_JOB" >> "$OUTPUT_FILE"
        fi
    done < "$INPUT_FILE"

done < "$SUBSCRIPTIONS_FILE"

echo "Traitement terminé. Résultats dans $OUTPUT_FILE."