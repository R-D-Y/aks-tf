probleme=""

# Vérifier si l'allocation dépasse les seuils et concaténer les problèmes
if [[ "$allocatedPercentage" -gt 100 ]]; then
    probleme="Oui - Allocation dépasse 100%"
elif [[ "$allocatedPercentage" -gt 90 ]]; then
    probleme="Oui - Allocation dépasse 90%"
fi

# Vérifier la correspondance entre le plan CF et le plan Azure
if [[ "$service_plan_name" != "notag" && "$service_plan_name" != "$detailed_sku" ]]; then
    if [[ -z "$probleme" ]]; then
        probleme="Oui - plan non correspondant à Azure"
    else
        probleme="$probleme | Oui - plan non correspondant à Azure"
    fi
fi

# Si aucun problème détecté, marquer la BD comme "BD saine"
if [[ -z "$probleme" ]]; then
    probleme="BD saine"
fi