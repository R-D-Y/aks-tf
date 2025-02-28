clean_text() {
    echo "$1" | sed 's/[^a-zA-Z0-9_-]//g'
}


# Nettoyage des noms pour éviter les erreurs de caractères spéciaux
service_instance_name=$(clean_text "$service_instance_name")
space_name=$(clean_text "$space_name")









