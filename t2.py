# Fallback logic if credentials are nested or named differently
if not api_uri:
    api_uri = credentials.get('http_api_uris', [None])[0]  # list -> first item

if not username:
    username = credentials.get('username') or credentials.get('protocols', {}).get('amqp', {}).get('username')

if not password:
    password = credentials.get('password') or credentials.get('protocols', {}).get('amqp', {}).get('password')

if not vhost:
    vhost = credentials.get('vhost') or credentials.get('protocols', {}).get('amqp', {}).get('vhost')