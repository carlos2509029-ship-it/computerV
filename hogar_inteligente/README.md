# 🏠 Hogar Inteligente con Reconocimiento Facial

**Autor:** Carlos Eduardo Lozoya López
**Materia:** Inteligencia Artificial, Unidad 5: Visión por computadora (Hybridge)

Sistema que reconoce a la persona que llega a casa a partir de una foto y ajusta el ambiente (luces, música y temperatura) según el perfil de cada residente. Si la persona no es residente, emite una alerta de seguridad. Las acciones del hogar están simuladas con mensajes en pantalla.

## ¿Cómo funciona?

1. Cada residente tiene una o más fotos en `residentes/` y un perfil de preferencias en `hogar.py`.
2. El programa revisa cada foto de `llegadas/` y la compara contra los residentes con `DeepFace.find` (modelo **Facenet**).
3. Según el resultado:
   - **Residente reconocido:** bienvenida y ajuste del ambiente (modo infantil si es niño).
   - **Persona desconocida:** alerta de seguridad.
   - **Foto sin rostro detectable:** aviso, sin que el programa se detenga.

## Instalación

Requiere **Python 3** (probado en Ubuntu/WSL).

```bash
git clone https://github.com/carlos2509029-ship-it/computerV.git
cd computerV
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta `computerV`:

```bash
python hogar_inteligente/hogar.py
```

La primera ejecución descarga el modelo Facenet (~90 MB) y genera un archivo de huellas faciales (`.npz`) dentro de `residentes/`.

## Cómo agregar residentes

1. Guarda la foto en `residentes/` con el nombre de la persona: `maria.jpg`. Para varias fotos de la misma persona: `maria_v-2.jpg`, `maria_v-3.jpg`.
2. Agrega su perfil al diccionario `PERFILES` en `hogar.py`, con la clave igual al nombre (`"maria"`).

Las fotos deben mostrar el rostro de frente y con buena iluminación.

## Ejemplo de salida

```
Procesando: llegada_5.jpg
⚠️ Persona no reconocida: enviando alerta de seguridad al propietario

Procesando: llegada_6.jpg
No se detectó un rostro en llegada_6.jpg

Procesando: llegada_7.jpg
Bienvenido, Carlos
  → Encendiendo luces cálidas al 40%
  → Reproduciendo jazz suave
  → Ajustando temperatura a 22 °C
```

## Hallazgo durante las pruebas: falso positivo y ajuste del umbral

Con la configuración por defecto de DeepFace (umbral de distancia **0.40**), el sistema confundió a un niño desconocido (`llegada_5.jpg`) con el residente Pablito y le "abrió la puerta". La distancia medida fue **0.381**, apenas debajo del límite.

|           Comparación        |   Distancia   |
|------------------------------|---------------|
| Carlos vs. sus propias fotos | 0.085 a 0.142 |
| Niño desconocido vs. Pablito | 0.381         |

Se fijó un umbral propio de **0.25** (`UMBRAL_DISTANCIA`), que deja un margen amplio: los residentes pasan con holgura y el desconocido queda bloqueado. Este caso muestra que en un sistema real de acceso no basta con el valor por defecto: el umbral debe calibrarse con datos y, en aplicaciones de seguridad, complementarse con una segunda verificación.

## Nota sobre las imágenes

Los rostros de los residentes y visitantes (excepto el autor) fueron **generados por IA** y no corresponden a personas reales.