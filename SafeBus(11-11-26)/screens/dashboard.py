import os
import customtkinter as ctk
from PIL import Image
from tema import Paleta, FUENTE, BASE

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Paleta.HUESO, corner_radius=0)
        self.controller = controller

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Paleta.HUESO, corner_radius=0)
        self.scroll.pack(fill="both", expand=True)

        self._crear_encabezado()
        self._crear_rastreo()
        self._crear_estudiante()
        self._crear_horarios()
        self._crear_conductor()
        self._crear_alertas()
        self._crear_accesos()

    # ---------------------------------------------------------- AYUDAS
    def _texto(self, parent, texto, size=13, bold=False, color=None, **kw):
        return ctk.CTkLabel(parent, text=texto, text_color=color or Paleta.AZUL,
                            font=(FUENTE, size, "bold" if bold else "normal"), **kw)

    def _titulo(self, texto, color=None, size=13):
        self._texto(self.scroll, texto, size, True, color).pack(anchor="w", padx=20, pady=(20, 8))

    def _tarjeta(self):
        card = ctk.CTkFrame(self.scroll, fg_color=Paleta.TURQUESA, corner_radius=16)
        card.pack(fill="x", padx=20)
        return card

    def _boton(self, parent, texto, comando, principal=False, **kw):
        if principal:  # acción principal: mostaza con texto azul
            fg, hover, txt = Paleta.MOSTAZA, Paleta.MOSTAZA_OSCURO, Paleta.AZUL
        else:          # acción secundaria: azul con texto hueso
            fg, hover, txt = Paleta.AZUL, Paleta.AZUL_SUAVE, Paleta.HUESO
        return ctk.CTkButton(parent, text=texto, command=comando, fg_color=fg,
                             hover_color=hover, text_color=txt,
                             font=(FUENTE, 13, "bold"), height=34, corner_radius=10, **kw)

    def _avatar(self, parent, iniciales, size=60, radio=30):
        av = ctk.CTkFrame(parent, width=size, height=size, corner_radius=radio, fg_color=Paleta.AZUL)
        self._texto(av, iniciales, 18, True, Paleta.HUESO).place(relx=0.5, rely=0.5, anchor="center")
        return av

    def _circulo(self, color, size=30):
        from PIL import ImageDraw
        s = size * 4
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(img).ellipse((0, 0, s - 1, s - 1), fill=color)
        return ctk.CTkImage(img, size=(size, size))

    def _icono(self, ruta, size=30):
        """Carga un ícono desde la carpeta del proyecto (no depende de dónde ejecutes el programa)."""
        ruta_completa = os.path.join(BASE, ruta)
        try:
            return ctk.CTkImage(Image.open(ruta_completa), size=(size, size))
        except (FileNotFoundError, OSError):
            print(f"[Iconos] No se encontró: {ruta_completa}")
            vacio = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            return ctk.CTkImage(vacio, size=(size, size))

    def _icono_alerta(self, size=34):
        from PIL import ImageDraw
        s = size * 4
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.polygon([(s / 2, 2), (s - 2, s - 4), (2, s - 4)], fill=Paleta.MOSTAZA, outline=Paleta.AZUL)
        d.rectangle((s / 2 - 6, s * 0.35, s / 2 + 6, s * 0.65), fill=Paleta.AZUL)
        d.ellipse((s / 2 - 7, s * 0.72, s / 2 + 7, s * 0.86), fill=Paleta.AZUL)
        return ctk.CTkImage(img, size=(size, size))

    def _pendiente(self, nombre):
        from tkinter import messagebox
        messagebox.showinfo("SafeBus", f"{nombre}: Coming Soon!")

    def _saludo(self):
        from datetime import datetime
        ahora = datetime.now()
        if ahora.hour < 12:
            s = "Good Morning"
        elif ahora.hour < 16:
            s = "Good Afternoon"
        elif ahora.hour < 19:
            s = "Good Evening"
        else:
            s = "Good Night"
        return f"{s} {ahora.strftime('%H:%M')}"

    # ---------------------------------------------------------- SECCIONES
    def _crear_encabezado(self):
        h = ctk.CTkFrame(self.scroll, fg_color=Paleta.AZUL, corner_radius=0)
        h.pack(fill="x")

        fila = ctk.CTkFrame(h, fg_color="transparent")
        fila.pack(fill="x", padx=20, pady=(18, 8))
        fila.grid_columnconfigure(0, weight=1)

        saludo = ctk.CTkFrame(fila, fg_color="transparent")
        saludo.grid(row=0, column=0, sticky="w")
        self._texto(saludo, self._saludo(), 13, color=Paleta.TURQUESA).pack(anchor="w")
        self._texto(saludo, "María García", 20, True, Paleta.HUESO).pack(anchor="w")

        avatar = ctk.CTkFrame(fila, width=56, height=56, corner_radius=28, fg_color=Paleta.TURQUESA)
        avatar.grid(row=0, column=1, sticky="e")
        self._texto(avatar, "MG", 16, True, Paleta.AZUL).place(relx=0.5, rely=0.5, anchor="center")
        # punto de notificación importante: mostaza
        ctk.CTkFrame(avatar, width=14, height=14, corner_radius=7,
                     fg_color=Paleta.MOSTAZA).place(relx=0.88, rely=0.12, anchor="center")

        estado = ctk.CTkFrame(h, fg_color=Paleta.TURQUESA, corner_radius=14)
        estado.pack(fill="x", padx=20, pady=(4, 20))
        ctk.CTkFrame(estado, width=12, height=12, corner_radius=6,
                     fg_color=Paleta.AZUL).pack(side="left", padx=(14, 10), pady=14)
        info = ctk.CTkFrame(estado, fg_color="transparent")
        info.pack(side="left", pady=8)
        self._texto(info, "Bus on the Chorrera-West route", 13, True, Paleta.AZUL).pack(anchor="w")
        self._texto(info, "La Salle School · Estimated arrival", 12, color=Paleta.TEXTO_SEC).pack(anchor="w")

    def _crear_rastreo(self):
        self._titulo("REAL-TIME TRACKING")
        mapa = ctk.CTkFrame(self.scroll, fg_color=Paleta.TURQUESA, corner_radius=16, height=200)
        mapa.pack(fill="x", padx=20)
        mapa.pack_propagate(False)
        self._texto(mapa, "The real-time map will go here", 14, color=Paleta.AZUL).place(
            relx=0.5, rely=0.5, anchor="center")
        ctk.CTkButton(mapa, text="↗  Expand", width=95, height=34, corner_radius=10,
                      fg_color=Paleta.AZUL, hover_color=Paleta.AZUL_SUAVE,
                      text_color=Paleta.HUESO, font=(FUENTE, 12, "bold"),
                      command=lambda: self.controller.show_frame("MapView")
                      ).place(relx=0.97, rely=0.06, anchor="ne")

    def _crear_estudiante(self):
        self._titulo("MY STUDENT")
        card = self._tarjeta()
        card.grid_columnconfigure(1, weight=1)

        self._avatar(card, "SG", 60, 14).grid(row=0, column=0, padx=14, pady=14)

        datos = ctk.CTkFrame(card, fg_color="transparent")
        datos.grid(row=0, column=1, sticky="w")
        self._texto(datos, "Sebastián García", 16, True).pack(anchor="w")
        self._texto(datos, "La Salle School · 6th Grade", 12, color=Paleta.TEXTO_SEC).pack(anchor="w")
        ctk.CTkLabel(datos, text="On board", fg_color=Paleta.AZUL, text_color=Paleta.TURQUESA,
                     corner_radius=8, width=70, height=22,
                     font=(FUENTE, 12, "bold")).pack(anchor="w", pady=(4, 0))

        self._boton(card, "Edit", lambda: self.controller.frames["ProfileView"].editar("hijo"),
                    width=80).grid(row=0, column=2, padx=14)

    def _crear_horarios(self):
        self._titulo("TODAY'S SCHEDULE")
        fila = ctk.CTkFrame(self.scroll, fg_color="transparent")
        fila.pack(fill="x", padx=20)
        fila.grid_columnconfigure((0, 1), weight=1, uniform="horarios")

        datos = [("icons/sunrise.png", "6:45 AM", "Pickup · Home"),
                 ("icons/sunset.png", "1:30 PM", "Estimated return")]
        for col, (icono, hora, desc) in enumerate(datos):
            c = ctk.CTkFrame(fila, fg_color=Paleta.TURQUESA, corner_radius=16)
            c.grid(row=0, column=col, sticky="nsew", padx=(0, 8) if col == 0 else (8, 0))
            ctk.CTkLabel(c, text="", image=self._icono(icono, 36)).pack(pady=(14, 4))
            self._texto(c, hora, 18, True).pack()
            self._texto(c, desc, 12, color=Paleta.TEXTO_SEC).pack(pady=(0, 14))

    def _crear_conductor(self):
        self._titulo("ASSIGNED DRIVER")
        card = self._tarjeta()
        card.grid_columnconfigure(1, weight=1)

        self._avatar(card, "JM", 60, 30).grid(row=0, column=0, padx=14, pady=14)

        datos = ctk.CTkFrame(card, fg_color="transparent")
        datos.grid(row=0, column=1, sticky="w")
        self._texto(datos, "José R. Martínez", 16, True).pack(anchor="w")
        self._texto(datos, "Unit #CH-047 · AAB-1234", 12, color=Paleta.TEXTO_SEC).pack(anchor="w")
        # estrellas en mostaza sobre un fondo azul (sobre turquesa casi no se verían)
        rating = ctk.CTkFrame(datos, fg_color=Paleta.AZUL, corner_radius=8)
        rating.pack(anchor="w", pady=(4, 0))
        self._texto(rating, "★★★★★", 13, color=Paleta.MOSTAZA).pack(side="left", padx=(8, 0), pady=2)
        self._texto(rating, " 4.9", 13, True, Paleta.HUESO).pack(side="left", padx=(0, 8), pady=2)

        botones = ctk.CTkFrame(card, fg_color="transparent")
        botones.grid(row=0, column=2, padx=14)
        self._boton(botones, "Call", lambda: self._pendiente("Call Driver"),
                    principal=True, width=90).pack(pady=(0, 6))
        self._boton(botones, "Report", lambda: self._pendiente("Report Issue"), width=90).pack()

    def _crear_alertas(self):
        self._titulo("Active Alerts")
        self.alerta = self._tarjeta()
        self.alerta.configure(border_width=2, border_color=Paleta.MOSTAZA)

        self.alerta_contenido = ctk.CTkFrame(self.alerta, fg_color="transparent")
        self.alerta_contenido.pack(fill="x")

        cab = ctk.CTkFrame(self.alerta_contenido, fg_color="transparent")
        cab.pack(fill="x", padx=14, pady=(14, 4))
        ctk.CTkLabel(cab, text="", image=self._icono_alerta()).pack(side="left")
        self._texto(cab, "Minor delay — Heavy traffic", 14, True).pack(side="left", padx=10)

        detalle = self._texto(
            self.alerta_contenido,
            "Congestion on the Pan-American Highway, km 35. Estimated delay: 8 min. Alternate route active.",
            12, justify="left", anchor="w")
        detalle.pack(fill="x", padx=14)

        # El texto se reacomoda al cambiar el ancho de la ventana
        ultimo = {"w": 0}

        def ajustar(e):
            if e.width != ultimo["w"]:
                ultimo["w"] = e.width
                detalle.configure(wraplength=max(200, e.width - 40))

        self.alerta_contenido.bind("<Configure>", ajustar)

        self._texto(self.alerta_contenido, "Reported 5 min ago · Driver: José Martínez", 11,
                    color=Paleta.TEXTO_SEC).pack(anchor="w", padx=14, pady=8)

        fila = ctk.CTkFrame(self.alerta_contenido, fg_color="transparent")
        fila.pack(fill="x", padx=14, pady=(0, 14))
        self._boton(fila, "Understood/Confirmed", self._confirmar_alerta,
                    principal=True).pack(side="left", padx=(0, 10))
        self._boton(fila, "See more", lambda: self._pendiente("Alert Details")).pack(side="left")

    def _confirmar_alerta(self):
        self.alerta_contenido.destroy()
        self.alerta.configure(border_width=0)
        self._texto(self.alerta, "No active alerts", 14, True).pack(padx=14, pady=24)

    def _icono_color(self, nombre, color, size=32):
        """Carga icons/<nombre>.png y lo pinta del color indicado (conserva la forma y la transparencia)."""
        from PIL import ImageOps
        ruta = os.path.join(BASE, "icons", nombre + ".png")
        try:
            img = Image.open(ruta).convert("RGBA")
        except (FileNotFoundError, OSError):
            print(f"[Iconos] No se encontró: {ruta}")
            return self._circulo(color)  # si falta el archivo, usa el círculo de antes
        mascara = img.getchannel("A")
        if mascara.getextrema()[0] == 255:  # sin transparencia: ícono oscuro sobre fondo blanco
            mascara = ImageOps.invert(img.convert("L"))
        pintado = Image.new("RGBA", img.size, color)
        pintado.putalpha(mascara)
        return ctk.CTkImage(pintado, size=(size, size))

    def _crear_accesos(self):
        self._titulo("QUICK ACCESS", Paleta.AZUL, 16)
        grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        grid.pack(fill="x", padx=20, pady=(0, 24))
        grid.grid_columnconfigure((0, 1), weight=1, uniform="accesos")

        # (texto, nombre del ícono en icons/, color del ícono, acción)
        accesos = [
            ("Route History", "history", Paleta.AZUL, lambda: self._pendiente("Route History")),
            ("Notifications", "notifications", Paleta.MOSTAZA, lambda: self._pendiente("Notifications")),
            ("Emergency\nContacts", "contact_emergency", Paleta.AZUL, lambda: self._pendiente("Emergency contacts")),
            ("Calendar", "calendar", Paleta.AZUL, lambda: self._pendiente("Calendar")),
            ("Chat", "chat", Paleta.AZUL, lambda: self.controller.show_frame("ChatView")),
        ]
        for i, (texto, icono, color, cmd) in enumerate(accesos):
            btn = ctk.CTkButton(grid, text=texto, image=self._icono_color(icono, color), compound="top",
                                height=96, corner_radius=18, fg_color=Paleta.TURQUESA,
                                hover_color=Paleta.TURQUESA_OSCURO, text_color=Paleta.AZUL,
                                font=(FUENTE, 13, "bold"), command=cmd)
            if i < 4:
                btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=6, pady=6)
            else:  # el último (Chat) va centrado en la tercera fila
                btn.configure(width=200)
                btn.grid(row=2, column=0, columnspan=2, padx=6, pady=6)