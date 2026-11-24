import customtkinter as ctk
from PIL import Image

# Configuración inicial de la apariencia
ctk.set_appearance_mode("Light")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Temas: "blue", "green", "dark-blue"

import os
from PIL import ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))  # carpeta donde está tu .py


def cargar_fuentes(nombre_carpeta="fonts"):
    """Carga todas las fuentes (.ttf/.otf) de la carpeta y devuelve el nombre real de la familia."""
    carpeta = os.path.join(BASE, nombre_carpeta)
    if not os.path.isdir(carpeta):
        print(f"[Fuentes] ERROR: no existe la carpeta {carpeta}")
        return None

    archivos = []
    for raiz, _, nombres in os.walk(carpeta):
        for n in nombres:
            if n.lower().endswith((".ttf", ".otf")):
                archivos.append(os.path.join(raiz, n))
    if not archivos:
        print(f"[Fuentes] ERROR: no hay archivos .ttf/.otf dentro de {carpeta}")
        return None

    familia = None
    for ruta in sorted(archivos):
        try:
            nombre, estilo = ImageFont.truetype(ruta, 12).getname()  # nombre real dentro del archivo
        except Exception as e:
            print(f"[Fuentes] ERROR leyendo {os.path.basename(ruta)}: {e}")
            continue
        ok = ctk.FontManager.load_font(ruta)
        print(f"[Fuentes] {'OK' if ok else 'ERROR'}: {os.path.basename(ruta)} -> familia '{nombre}' ({estilo})")
        if ok and familia is None:
            familia = nombre
    return familia


FUENTE = cargar_fuentes() or "Arial"  # si algo falla, usa Arial para que la app siga viéndose bien
print(f"[Fuentes] Fuente en uso: {FUENTE}")
try:
    ctk.ThemeManager.theme["CTkFont"]["family"] = FUENTE
except Exception as e:
    print(f"[Fuentes] No se pudo fijar la fuente por defecto: {e}")

class Paleta:
    """Paleta SafeBus: 60% azul petróleo · 30% hueso + turquesa · 10% mostaza."""
    AZUL = "#112634"
    HUESO = "#e2cea1"
    TURQUESA = "#add6d1"
    MOSTAZA = "#d59a1a"
    # tonos derivados (solo para hover y texto secundario)
    AZUL_OSCURO = "#091720"
    AZUL_SUAVE = "#1b3a4d"
    TURQUESA_OSCURO = "#8fbdb7"
    MOSTAZA_OSCURO = "#bf8715"
    TEXTO_SEC = "#2b4655"
    BLANCO = "#ffffff"
