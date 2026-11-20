# Hogar inteligente con reconocimiento facial (DeepFace)
# Autor: Carlos Eduardo Lozoya López

import os
from deepface import DeepFace
from deepface.modules.exceptions import FaceNotDetected

CARPETA_RESIDENTES = "hogar_inteligente/residentes"
CARPETA_LLEGADAS = "hogar_inteligente/llegadas"
UMBRAL_DISTANCIA = 0.25   # ajústalo según lo que midas

# Perfiles de los residentes: el nombre debe coincidir con el inicio del nombre de su foto
PERFILES = {
    "carlos":  {"tipo": "adulto", "luces": "cálidas al 40%",   "musica": "jazz suave",            "temperatura": 22},
    "anita":   {"tipo": "adulto", "luces": "blancas al 70%",   "musica": "boleros",               "temperatura": 23},
    "zahira":  {"tipo": "adulto", "luces": "neutras al 60%",   "musica": "pop en español",        "temperatura": 21},
    "lalito":  {"tipo": "niño",   "luces": "de colores al 80%", "musica": "canciones infantiles",  "temperatura": 23},
    "pablito": {"tipo": "niño",   "luces": "de colores al 80%", "musica": "música de videojuegos", "temperatura": 23},
}


def reconocer(ruta_foto):
    """Devuelve el nombre del residente reconocido, o None si no reconoce a nadie."""
    resultado = DeepFace.find(
        img_path=ruta_foto,
        db_path=CARPETA_RESIDENTES,
        model_name="Facenet",
        silent=True,
    )
    tabla = resultado[0]
    if tabla.empty:
        return None
    if tabla["distance"].iloc[0] > UMBRAL_DISTANCIA:
        return None
    ruta_coincidencia = tabla["identity"].iloc[0]       # .../residentes/carlos_v-5.jpg
    archivo = os.path.basename(ruta_coincidencia)       # carlos_v-5.jpg
    nombre = archivo.split(".")[0].split("_")[0]        # carlos
    return nombre


def aplicar_preferencias(nombre):
    """Imprime las acciones simuladas según el perfil del residente."""
    perfil = PERFILES[nombre]
    print(f"Bienvenido, {nombre.capitalize()}")
    print(f"  → Encendiendo luces {perfil['luces']}")
    print(f"  → Reproduciendo {perfil['musica']}")
    print(f"  → Ajustando temperatura a {perfil['temperatura']} °C")
    if perfil["tipo"] == "niño":
        print("  → Activando modo entretenimiento infantil")


def procesar_llegada(ruta_foto):
    """Reconoce a quien llega y decide qué hacer."""
    archivo = os.path.basename(ruta_foto)
    print(f"\nProcesando: {archivo}")
    try:
        nombre = reconocer(ruta_foto)
    except FaceNotDetected:
        print(f"No se detectó un rostro en {archivo}")
        return

    if nombre is None or nombre not in PERFILES:
        print("⚠️ Persona no reconocida: enviando alerta de seguridad al propietario")
    else:
        aplicar_preferencias(nombre)


def main():
    fotos = sorted(
        f for f in os.listdir(CARPETA_LLEGADAS)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    print("=== Sistema de hogar inteligente ===")
    for foto in fotos:
        procesar_llegada(os.path.join(CARPETA_LLEGADAS, foto))


if __name__ == "__main__":
    main()