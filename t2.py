# Déterminer si la BD a un problème d'allocation
if [[ "$allocatedPercentage" -gt 100 ]]; then
    probleme="Oui - Allocation dépasse 100%"
elif [[ "$allocatedPercentage" -gt 90 ]]; then
    probleme="Oui - Allocation dépasse 90%"
else
    probleme="BD saine"
fi