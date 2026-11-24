import os
import customtkinter as ctk
from PIL import Image
from tema import Paleta, FUENTE, BASE
from .base import BaseView

class LoginView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # --- Columna centrada de ancho fijo (~380 px) ---
        self.centro.place_forget()
        self.centro.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkFrame(self.centro, width=380, height=1, fg_color="transparent").pack()

        # --- Logo ---
        ruta_logo = os.path.join(BASE, "icons", "logo.png")
        try:
            img = Image.open(ruta_logo).convert("RGBA")

            # --- Esquinas redondeadas ---
            from PIL import ImageDraw, ImageChops
            radio = int(img.width * 0.12)   # 0.12 = nivel de redondeo; súbelo para más redondeado
            esc = 4                         # la máscara se dibuja 4 veces más grande y se reduce: bordes suaves
            mascara = Image.new("L", (img.width * esc, img.height * esc), 0)
            ImageDraw.Draw(mascara).rounded_rectangle(
                (0, 0, img.width * esc - 1, img.height * esc - 1), radius=radio * esc, fill=255)
            mascara = mascara.resize(img.size, Image.LANCZOS)
            img.putalpha(ImageChops.multiply(img.getchannel("A"), mascara))
            ancho = 200                                    # cambia este número para agrandar o achicar el logo
            alto = int(ancho * img.height / img.width)     # mantiene la proporción de la imagen
            logo = ctk.CTkImage(img, size=(ancho, alto))
            ctk.CTkLabel(self.centro, text="", image=logo).pack(pady=(0, 14))
        except (FileNotFoundError, OSError):
            print(f"[Logo] No se encontró: {ruta_logo}")
            ctk.CTkLabel(self.centro, text="SafeBus", font=(FUENTE, 30, "bold"),
                         text_color=Paleta.AZUL).pack(pady=(0, 14))

        # --- Eslogan (franja azul petróleo) ---
        banda = ctk.CTkFrame(self.centro, fg_color=Paleta.AZUL, corner_radius=14)
        banda.pack(fill="x", pady=(0, 14))
        eslogan = ctk.CTkFrame(banda, fg_color="transparent")
        eslogan.pack(pady=12)
        ctk.CTkLabel(eslogan, text="Su Seguridad. Tu Tranquilidad.", font=(FUENTE, 14, "bold"),
                     text_color=Paleta.TURQUESA).pack(side="left")
        ctk.CTkLabel(eslogan, text=" Siempre.", font=(FUENTE, 14, "bold"),
                     text_color=Paleta.MOSTAZA).pack(side="left")
            
        ctk.CTkLabel(self.centro, text="LogIn to Continue:", font=(FUENTE, 14),
                     text_color=Paleta.TEXTO_SEC).pack(pady=(2, 24))
        
        estilo = dict(height=44, corner_radius=12, fg_color=Paleta.BLANCO,
                      border_color=Paleta.AZUL, border_width=1,
                      text_color=Paleta.AZUL, placeholder_text_color="#6b7c85")

        self.entry_user = ctk.CTkEntry(self.centro, placeholder_text="E-mail Address:", **estilo)
        self.entry_user.pack(fill="x", pady=8)

        self.entry_pass = ctk.CTkEntry(self.centro, placeholder_text="Password:", show="*", **estilo)
        self.entry_pass.pack(fill="x", pady=8)

        ctk.CTkButton(
            self.centro, text="LogIn", height=46, corner_radius=12,
            fg_color=Paleta.MOSTAZA, hover_color=Paleta.MOSTAZA_OSCURO,
            text_color=Paleta.AZUL, font=(FUENTE, 15, "bold"),
            command=lambda: controller.show_frame("DashboardView"),
        ).pack(fill="x", pady=(22, 0))