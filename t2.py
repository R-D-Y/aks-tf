def get_instance_credentials(instance_guid: str, org_name: str, space_name: str) -> Dict:
    """Obtenir les credentials RabbitMQ à partir d'une service key ou des variables d'environnement d'une application liée"""

    # Cibler le bon org et espace
    run_command(['cf', 'target', '-o', org_name, '-s', space_name])

    # Obtenir les informations de l'instance de service
    service_info = json.loads(run_command(['cf', 'curl', f'/v3/service_instances/{instance_guid}']))
    service_name = service_info['name']

    print(f"DEBUG: Recherche des credentials pour le service: {service_name} dans {org_name}/{space_name}")

    # 1️⃣ **Essayer d'obtenir une service key**
    credentials = get_credentials_from_service_key(service_name)
    
    if credentials:
        print(f"✅ Credentials trouvés via une service key pour {service_name}")
        return credentials
    else:
        print(f"⚠️ Aucune service key trouvée pour {service_name}, tentative via les bindings...")

    # 2️⃣ **Essayer d'obtenir les credentials via les bindings (cf env)**
    credentials = get_credentials_from_env(service_name)

    if credentials:
        print(f"✅ Credentials trouvés via une application liée pour {service_name}")
        return credentials

    # 3️⃣ **Si aucun credential trouvé**
    print(f"❌ Aucun credentials trouvés pour {service_name} dans {org_name}/{space_name}")
    return {}


def get_credentials_from_service_key(service_name: str) -> Dict:
    """Essayer d'obtenir les credentials à partir d'une service key"""
    try:
        keys_output = run_command(['cf', 'service-keys', service_name], exit_on_error=False)
        lines = [line.strip() for line in keys_output.splitlines() if line.strip()]
        key_names = [line for line in lines if not line.startswith("Getting keys") and not line.lower() == "name"]

        if key_names:
            service_key_name = key_names[0]
            key_output = run_command(['cf', 'service-key', service_name, service_key_name], exit_on_error=False)

            json_lines = []
            started = False

            for line in key_output.splitlines():
                if '{' in line:
                    started = True
                if started:
                    json_lines.append(line)

            if json_lines:
                json_content = '\n'.join(json_lines)
                try:
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    print(f"❌ Erreur de parsing JSON de la service key pour {service_name}")
    
    except subprocess.CalledProcessError:
        print(f"⚠️ Aucune service key disponible pour {service_name}")

    return {}


def get_credentials_from_env(instance_name: str) -> Dict:
    """Essayer d'obtenir les credentials via les variables d'environnement d'une application liée"""
    try:
        # Récupérer la liste des applications
        apps_output = run_command(['cf', 'apps'])
        app_lines = [line.strip() for line in apps_output.splitlines()]
        bound_apps = [line.split()[0] for line in app_lines if instance_name in line]  # Extraire les noms d'applications liées
        
        for app_name in bound_apps:
            print(f"🔎 Tentative de récupération des credentials depuis l'environnement de l'app: {app_name}")
            env_output = run_command(['cf', 'env', app_name], exit_on_error=False)

            # Trouver la section VCAP_SERVICES
            vcap_services_index = env_output.find("VCAP_SERVICES:")
            if vcap_services_index == -1:
                continue  # Pas de VCAP_SERVICES, essayer l'app suivante

            json_start = env_output.find("{", vcap_services_index)
            json_end = env_output.rfind("}") + 1
            if json_start == -1 or json_end == -1:
                continue  # Pas de JSON détecté

            try:
                vcap_services = json.loads(env_output[json_start:json_end])
                for service_type in vcap_services:
                    for service in vcap_services[service_type]:
                        if service.get("name") == instance_name:
                            return service.get("credentials", {})

            except json.JSONDecodeError:
                continue  # Si parsing échoue, passer à l'application suivante

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des credentials depuis les bindings pour {instance_name}: {e}")

    return {}
    
    
    def main():
    if not check_cf_auth():
        sys.exit(1)

    # Sauvegarde de la cible actuelle
    original_target = get_current_target()
    print("🔍 Analyse des instances RabbitMQ...")

    try:
        instances = get_service_instances()
        results = []
        instances_without_credentials = []
        total_instances = len(instances)

        for instance in instances:
            print(f"\n➡️ Vérification de l'instance : {instance['name']} dans {instance['org_name']}/{instance['space_name']}")
            
            try:
                credentials = get_instance_credentials(instance['guid'], instance['org_name'], instance['space_name'])

                if not credentials:
                    print(f"❌ Aucun credentials trouvés pour {instance['name']}")
                    instances_without_credentials.append(instance)
                    continue

                api_uri = credentials.get('http_api_uri')
                username = credentials.get('username')
                password = credentials.get('password')
                vhost = credentials.get('vhost')

                if not all([api_uri, username, password, vhost]):
                    print(f"⚠️ Informations d'identification incomplètes pour {instance['name']}")
                    continue

                # 🔎 Vérification des queues en mirroring
                mirrored_queues = check_queue_mirroring(api_uri, vhost, username, password)

                if mirrored_queues:
                    print(f"✅ L'instance {instance['name']} utilise le mirroring classique.")
                    results.append({
                        'service_instance': instance['name'],
                        'organization': instance['org_name'],
                        'space': instance['space_name'],
                        'mirrored_queues': mirrored_queues
                    })
                else:
                    print(f"⚠️ Aucune queue en mirroring détectée pour {instance['name']}")

            except Exception as e:
                print(f"❌ Erreur lors du traitement de {instance['name']} : {e}")
                continue

        # 📝 Résumé des résultats
        if results:
            print("\n🔍 Instances utilisant le mirroring de queues classiques :")
            print(json.dumps(results, indent=2))
            print("\n📊 Résumé :")
            for result in results:
                print(f"\n📌 Instance : {result['service_instance']} ({result['organization']}/{result['space']})")
                print("  📥 Files d'attente avec mirroring :")
                for queue in result['mirrored_queues']:
                    print(f"    🔸 Queue: {queue['name']}")
                    print(f"      🔹 Politique: {queue['policy']}")
                    print(f"      🔹 Miroirs: {queue['mirrors']} ({queue['synchronized_mirrors']} synchronisés)")
        else:
            print("\n❌ Aucune instance trouvée utilisant le mirroring de queues classiques.")

        print(f"\n📊 Statistiques globales :")
        print(f"✔️ Total des instances analysées : {total_instances}")
        print(f"✔️ Instances avec des queues en mirroring : {len(results)}")
        print(f"⚠️ Instances sans credentials récupérables : {len(instances_without_credentials)}")

        if instances_without_credentials:
            print("\n❗ Instances sans credentials disponibles :")
            for instance in instances_without_credentials:
                print(f"  🔹 {instance['name']} ({instance['org_name']}/{instance['space_name']})")

    finally:
        # Rétablir la cible initiale
        restore_target(original_target)


if __name__ == '__main__':
    main()
    
    