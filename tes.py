get_cf_names() {
    local instance_id="$1"
    local space_guid="$2"

    local service_name space_name service_plan_guid service_plan_name

    # Récupérer le nom de l'instance de service et son plan GUID
    if [[ -n "$instance_id" ]]; then
        service_data=$(cf curl /v3/service_instances/"$instance_id")
        service_name=$(echo "$service_data" | jq -r '.name // empty')
        service_plan_guid=$(echo "$service_data" | jq -r '.relationships.service_plan.data.guid // empty')
    fi

    # Récupérer le nom du space
    if [[ -n "$space_guid" ]]; then
        space_name=$(cf curl /v3/spaces/"$space_guid" | jq -r '.name // empty')
    fi

    # Récupérer le nom du plan de l'instance de service
    if [[ -n "$service_plan_guid" ]]; then
        service_plan_name=$(cf curl /v3/service_plans/"$service_plan_guid" | jq -r '.name // empty')
    fi

    echo "$service_name|$space_name|$service_plan_name"
}



# Récupérer les tags pour obtenir les GUID de l'instance et du space
tags=$(get_tags "$rg" "$server" "$name")
pcf_instance_id=$(echo "$tags" | cut -d '|' -f1)
pcf_space_guid=$(echo "$tags" | cut -d '|' -f2)

# Récupérer les noms et le plan à partir des GUID Cloud Foundry
cf_data=$(get_cf_names "$pcf_instance_id" "$pcf_space_guid")
service_instance_name=$(echo "$cf_data" | cut -d '|' -f1)
space_name=$(echo "$cf_data" | cut -d '|' -f2)
service_plan_name=$(echo "$cf_data" | cut -d '|' -f3)

