from deepface import DeepFace

resultado = DeepFace.find(
    img_path="hogar_inteligente/llegadas/llegada_5.jpg",
    db_path="hogar_inteligente/residentes",
    model_name="Facenet"
)

# print(type(resultado))
# print(resultado)

tabla = resultado[0]
print(tabla[["identity", "distance", "threshold"]])