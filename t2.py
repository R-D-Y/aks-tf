get_tags() {
    local resource_group="$1"
    local server="$2"
    local db_name="$3"

    # Récupérer les tags de la base de données
    local tags_json
    tags_json=$(az sql db show --resource-group "$resource_group" --server "$server" --name "$db_name" --query "tags" --output json)

    # Extraire les GUID des tags ou mettre "notag" si absent
    local pcf_instance_id pcf_space_guid
    pcf_instance_id=$(echo "$tags_json" | jq -r '.["pcf-instance-id"] // "notag"')
    pcf_space_guid=$(echo "$tags_json" | jq -r '.["pcf-space-guid"] // "notag"')

    echo "$pcf_instance_id|$pcf_space_guid"
}


get_cf_names() {
    local instance_id="$1"
    local space_guid="$2"

    local service_name="notag"
    local space_name="notag"

    # Récupérer le nom de l'instance de service
    if [[ "$instance_id" != "notag" ]]; then
        service_name=$(cf curl /v3/service_instances/"$instance_id" | jq -r '.name // "notag"')
    fi

    # Récupérer le nom du space
    if [[ "$space_guid" != "notag" ]]; then
        space_name=$(cf curl /v3/spaces/"$space_guid" | jq -r '.name // "notag"')
    fi

    echo "$service_name|$space_name"
}


# Récupérer les tags pour obtenir les GUID de l'instance et du space
tags=$(get_tags "$rg" "$server" "$name")
pcf_instance_id=$(echo "$tags" | cut -d '|' -f1)
pcf_space_guid=$(echo "$tags" | cut -d '|' -f2)

# Récupérer les noms à partir des GUID Cloud Foundry
cf_data=$(get_cf_names "$pcf_instance_id" "$pcf_space_guid")
service_instance_name=$(echo "$cf_data" | cut -d '|' -f1)
space_name=$(echo "$cf_data" | cut -d '|' -f2)




