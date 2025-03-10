import requests
import random

# URL del endpoint
url = "http://localhost:5000/set_emotion_goal"

# Generar valores aleatorios para cada clave del emotion_goal
keys = [
    "lps",
    "letl_a", "letl_b", "letl_c",
    "lebl_a", "lebl_b", "lebl_c",
    "rps",
    "retl_a", "retl_b", "retl_c",
    "rebl_a", "rebl_b", "rebl_c",
    "tl_a", "tl_b", "tl_c", "tl_d", "tl_e",
    "bl_a", "bl_b", "bl_c", "bl_d", "bl_e"
]

# Crear un diccionario con valores aleatorios
data = {key: random.randint(0, 100) for key in keys}
print(data)
# Enviar la solicitud POST con los valores aleatorios
response = requests.post(url, json=data)

# Verificar la respuesta
if response.status_code == 200:
    print("Éxito:", response.json())
else:
    print("Error:", response.json())
