# aks-tf


for row in rows:
    numero, nom = row

    # Vérifier si le nom est "toto"
    if nom.strip().lower() == "toto":
        nom_cell = Cell(nom, background="#FFC0CB")  # Couleur rose
    else:
        nom_cell = Cell(nom)

    t.add_row([numero, nom_cell])


ou alors


for row in rows:
    if row[1] == "toto":  # Supposons que la colonne "Nom" est à l'index 1
        row[1] = f'<span style="background-color:pink;">{row[1]}</span>'
