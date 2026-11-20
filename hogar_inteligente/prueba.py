from deepface import DeepFace

resultado = DeepFace.find(
    img_path="hogar_inteligente/llegadas/llegada_7.jpg",
    db_path="hogar_inteligente/residentes",
    model_name="Facenet"
)

print(type(resultado))
print(resultado)