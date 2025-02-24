# aks-tf

def get_instance_credentials(instance_guid: str, org_name: str, space_name: str) -> Dict:
    """Get RabbitMQ credentials from app binding (VCAP_SERVICES)"""

    run_command(['cf', 'target', '-o', org_name, '-s', space_name])

    try:
        # Liste toutes les applications bindées à ce service instance
        bindings_output = run_command(['cf', 'curl', f'/v3/service_credential_bindings?service_instance_guids={instance_guid}&type=app'])
        bindings = json.loads(bindings_output)

        if not bindings['resources']:
            print(f"No apps bound to service instance {instance_guid}")
            return {}

        # Prends la première application bindée disponible
        app_guid = bindings['resources'][0]['relationships']['app']['data']['guid']

        # Récupère les variables d'environnement de l'app sélectionnée
        env_output = run_command(['cf', 'curl', f'/v3/apps/{app_guid}/env'])
        env_json = json.loads(env_output)

        vcap_services = env_json.get('system_env_json', {}).get('VCAP_SERVICES', {})
        rabbitmq_services = vcap_services.get('p.rabbitmq', [])

        if not rabbitmq_services:
            print("No RabbitMQ credentials found in VCAP_SERVICES")
            return {}

        credentials = rabbitmq_services[0]['credentials']
        
        # Retourne les credentials nécessaires
        return {
            'http_api_uri': credentials.get('http_api_uri'),
            'username': credentials.get('username'),
            'password': credentials.get('password'),
            'vhost': credentials.get('vhost')
        }

    except Exception as e:
        print(f"Error retrieving credentials from app binding: {e}")
        return {}