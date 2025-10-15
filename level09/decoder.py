# Lire le fichier token
try:
    with open('token', 'rb') as file:
        file_bytes = file.read()
    
    print(f"Contenu du fichier (bytes): {file_bytes}")
    
    # Convertir chaque byte en valeur
    byte_values = list(file_bytes)
    print("Valeurs des bytes:")
    print(byte_values)
    
    # Afficher chaque byte avec sa valeur
    print("\nDétail byte par byte:")
    for i, byte_val in enumerate(byte_values):
        if 32 <= byte_val <= 126:  # Caractères imprimables ASCII
            print(f"Position {i}: {byte_val} ('{chr(byte_val)}')")
        else:
            print(f"Position {i}: {byte_val} (non-imprimable)")
    
    print(f"\nNombre total de bytes: {len(file_bytes)}")

    new_token = str()
    for i in range(len(file_bytes)):
        new_token += chr(byte_values[i] - 1)

    print(f"Nouveau token: {new_token}")

except FileNotFoundError:
    print("Fichier 'token' non trouvé")
except Exception as e:
    print(f"Erreur lors de la lecture: {e}")
