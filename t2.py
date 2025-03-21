# Extraire le bon dictionnaire des credentials
if 'credentials' in credentials and isinstance(credentials['credentials'], dict):
    credentials = credentials['credentials']

# Récupérer les bonnes valeurs
api_uri = credentials.get('http_api_uri') or credentials.get('http_api_uris', [None])[0]
username = credentials.get('username') or credentials.get('protocols', {}).get('amqp', {}).get('username')
password = credentials.get('password') or credentials.get('protocols', {}).get('amqp', {}).get('password')
vhost = credentials.get('vhost') or credentials.get('protocols', {}).get('amqp', {}).get('vhost')

# Afficher les valeurs récupérées pour debug
print(f"DEBUG: api_uri={api_uri}, username={username}, password=******, vhost={vhost}")

# Vérification avant de continuer
if not all([api_uri, username, password, vhost]):
    print(f"ERROR: Missing required credential information for {instance['name']}")
    return {}