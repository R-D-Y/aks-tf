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