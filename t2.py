get_cf_names() {
    local instance_id="$1"
    local space_guid="$2"

    local service_name="notag"
    local space_name="notag"
    local service_plan="notag"

    # Récupérer le nom de l'instance de service et son plan
    if [[ "$instance_id" != "notag" ]]; then
        service_json=$(cf curl /v3/service_instances/"$instance_id")
        service_name=$(echo "$service_json" | jq -r '.name // "notag"')
        service_plan=$(echo "$service_json" | jq -r '.relationships.service_plan.data.guid // "notag"')
    fi

    # Récupérer le nom du space
    if [[ "$space_guid" != "notag" ]]; then
        space_name=$(cf curl /v3/spaces/"$space_guid" | jq -r '.name // "notag"')
    fi

    echo "$service_name|$space_name|$service_plan"
}



remplacer
cf_data=$(get_cf_names "$pcf_instance_id" "$pcf_space_guid")
service_instance_name=$(echo "$cf_data" | cut -d '|' -f1)
space_name=$(echo "$cf_data" | cut -d '|' -f2)

par
cf_data=$(get_cf_names "$pcf_instance_id" "$pcf_space_guid")
service_instance_name=$(echo "$cf_data" | cut -d '|' -f1)
space_name=$(echo "$cf_data" | cut -d '|' -f2)
service_plan_guid=$(echo "$cf_data" | cut -d '|' -f3)



ajouter cette boucle avant la principale

get_service_plan_name() {
    local plan_guid="$1"

    if [[ "$plan_guid" == "notag" ]]; then
        echo "notag"
        return
    fi

    # Récupérer le nom du plan de service
    plan_name=$(cf curl /v3/service_plans/"$plan_guid" | jq -r '.name // "notag"')

    echo "$plan_name"
}


ahouter ça dans la boucle principale

service_plan_name=$(get_service_plan_name "$service_plan_guid")





