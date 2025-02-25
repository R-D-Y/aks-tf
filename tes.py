for row in rows:
    if row[1] == "toto":  # Supposons que la colonne "Nom" est à l'index 1
        row[1] = f'<span style="background-color:pink;">{row[1]}</span>'