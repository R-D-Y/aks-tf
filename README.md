# aks-tf


for row in rows:
    numero, nom = row

    # Vérifier si le nom est "toto"
    if nom.strip().lower() == "toto":
        nom_cell = Cell(nom, background="#FFC0CB")  # Couleur rose
    else:
        nom_cell = Cell(nom)

    t.add_row([numero, nom_cell])