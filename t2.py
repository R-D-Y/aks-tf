key_names = []
for line in lines:
    if line.startswith("Getting keys") or "name" in line.lower():
        continue
    # Extraire le premier mot (le nom de la clé)
    parts = line.split()
    if parts:
        key_names.append(parts[0])