import customtkinter as ctk

from PIL import Image

from tema import FUENTE, Paleta

from screens import (
    LoginView,
    DashboardView,
    MapView,
    ChatView,
    ProfileView,
    SettingsView,
    EditParentView,
    EditStudentView,
)

class SafeBusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Tamaño de celular ---
        self.title("SafeBus")
        self.geometry("420x700")
        self.minsize(380, 600)

        self.alto_barra = 72
        self.alto_panel = 230
        self.panel_abierto = False

        # Fila 0: pantallas (se estira) · Fila 1: barra de abajo (alto fijo)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color= Paleta.HUESO, corner_radius=0)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Diccionario para almacenar las pantallas
        self.frames = {}
        for F in (LoginView, DashboardView, MapView, ChatView, ProfileView, SettingsView, EditParentView, EditStudentView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # --- Barra de navegación de abajo ---
        self.barra = ctk.CTkFrame(self, height=self.alto_barra, corner_radius=0, fg_color=Paleta.AZUL)
        self.barra.grid(row=1, column=0, sticky="ew")
        self.barra.grid_propagate(False)
        self.barra.grid_rowconfigure(0, weight=1)
        self.barra.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="nav")

        self.nav = {}
        botones = [
            ("DashboardView", "Menu", "home"),
            ("MapView", "Map", "map"),
            ("ChatView", "Chat", "chat"),
            ("ProfileView", "Profile", "perfil"),
        ]
        for col, (pagina, texto, tipo) in enumerate(botones):
            b = self._boton_nav(texto, tipo, lambda p=pagina: self.show_frame(p))
            b.grid(row=0, column=col, sticky="nsew", padx=3, pady=8)
            self.nav[pagina] = b

        self.btn_mas = self._boton_nav("More", "...", self.alternar_panel)
        self.btn_mas.grid(row=0, column=4, sticky="nsew", padx=3, pady=8)
        self.nav["SettingsView"] = self.btn_mas  # "Más" se resalta cuando estás en Configuración

                # --- Panel que sube desde la barra (con animación) ---
        self.alto_panel = 200   # parte visible del panel
        self.extra_panel = 20   # parte que queda escondida detrás de la barra
        self._y_oculto = -self.alto_barra + self.alto_panel + self.extra_panel
        self._y_visible = -self.alto_barra + self.extra_panel
        self._y_actual = self._y_oculto
        self._anim_id = None

        self.panel = ctk.CTkFrame(self, height=self.alto_panel + self.extra_panel, corner_radius=16,
                                  fg_color=Paleta.AZUL, border_width=1, border_color=Paleta.TURQUESA)
        self.panel.grid_propagate(False)
        self.panel.grid_columnconfigure((0, 1), weight=1, uniform="op")
        self.panel.grid_rowconfigure(99, weight=1)  # empuja los botones hacia arriba

        opciones = [
            ("Settings", "config", lambda: self.show_frame("SettingsView")),
            ("Alerts", "alertas", lambda: self._pendiente("Alerts")),
            ("Route History", "historial", lambda: self._pendiente("Route History")),
            ("Logout", "salir", lambda: self.confirmar_cierre_sesion()),
        ]
        for i, (texto, tipo, cmd) in enumerate(opciones):
            fila, col = divmod(i, 2)
            # el amarillo de tu paleta se usa solo en el ícono de alertas
            color = Paleta.MOSTAZA if tipo == "alertas" else Paleta.HUESO
            ctk.CTkButton(
                self.panel, text=texto, image=self._dibujar_icono(tipo, color, 30),
                compound="top", width=10, height=80, corner_radius=14,
                fg_color=Paleta.AZUL_OSCURO, hover_color=Paleta.AZUL_SUAVE, text_color=	Paleta.HUESO,
                font=(FUENTE, 13, "bold"), command=cmd,
            ).grid(row=fila, column=col, sticky="ew", padx=8,
                   pady=(16, 6) if fila == 0 else (6, 12))

        self.show_frame("LoginView")

    # ---------------------------------------------------------- BARRA Y PANEL
    def _dibujar_icono(self, tipo, color="#e2cea1", size=24):
        """Dibuja los íconos con código, así no dependes de archivos."""
        from PIL import ImageDraw
        s = size * 4
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        if tipo == "home":
            d.polygon([(s*0.5, s*0.10), (s*0.95, s*0.50), (s*0.05, s*0.50)], fill=color)
            d.rectangle((s*0.18, s*0.48, s*0.82, s*0.90), fill=color)
            d.rectangle((s*0.42, s*0.62, s*0.58, s*0.90), fill=(0, 0, 0, 0))
        elif tipo == "map":
            d.ellipse((s*0.20, s*0.06, s*0.80, s*0.66), fill=color)
            d.polygon([(s*0.27, s*0.50), (s*0.73, s*0.50), (s*0.5, s*0.95)], fill=color)
            d.ellipse((s*0.39, s*0.25, s*0.61, s*0.47), fill=(0, 0, 0, 0))
        elif tipo == "chat":
            d.rounded_rectangle((s*0.06, s*0.12, s*0.94, s*0.72), radius=s*0.18, fill=color)
            d.polygon([(s*0.22, s*0.66), (s*0.22, s*0.94), (s*0.50, s*0.68)], fill=color)
        elif tipo == "perfil":
            d.ellipse((s*0.31, s*0.08, s*0.69, s*0.46), fill=color)
            d.ellipse((s*0.12, s*0.56, s*0.88, s*1.30), fill=color)
        elif tipo == "config":  # engranaje
            import math
            c = s / 2
            for k in range(8):
                a = math.radians(k * 45)
                d.line([(c + s*0.30*math.cos(a), c + s*0.30*math.sin(a)),
                        (c + s*0.44*math.cos(a), c + s*0.44*math.sin(a))],
                       fill=color, width=int(s*0.16))
            d.ellipse((s*0.20, s*0.20, s*0.80, s*0.80), fill=color)
            d.ellipse((s*0.37, s*0.37, s*0.63, s*0.63), fill=(0, 0, 0, 0))
        elif tipo == "alertas":  # triángulo con "!"
            d.polygon([(s*0.50, s*0.08), (s*0.96, s*0.88), (s*0.04, s*0.88)], fill=color)
            d.rectangle((s*0.46, s*0.36, s*0.54, s*0.62), fill=(0, 0, 0, 0))
            d.ellipse((s*0.45, s*0.68, s*0.55, s*0.78), fill=(0, 0, 0, 0))
        elif tipo == "historial":  # reloj
            d.ellipse((s*0.08, s*0.08, s*0.92, s*0.92), fill=color)
            d.ellipse((s*0.18, s*0.18, s*0.82, s*0.82), fill=(0, 0, 0, 0))
            d.line([(s*0.50, s*0.50), (s*0.50, s*0.28)], fill=color, width=int(s*0.08))
            d.line([(s*0.50, s*0.50), (s*0.68, s*0.58)], fill=color, width=int(s*0.08))
        elif tipo == "salir":  # puerta con flecha
            d.rectangle((s*0.10, s*0.10, s*0.55, s*0.90), outline=color, width=int(s*0.09))
            d.line([(s*0.36, s*0.50), (s*0.74, s*0.50)], fill=color, width=int(s*0.09))
            d.polygon([(s*0.70, s*0.28), (s*0.94, s*0.50), (s*0.70, s*0.72)], fill=color)
        else:  # "mas" = tres rayitas
            for y in (0.20, 0.44, 0.68):
                d.rounded_rectangle((s*0.12, s*y, s*0.88, s*(y + 0.13)), radius=s*0.06, fill=color)
        return ctk.CTkImage(img, size=(size, size))

    def _boton_nav(self, texto, tipo, comando):
        return ctk.CTkButton(
            self.barra, text=texto, image=self._dibujar_icono(tipo),
            compound="top", width=10, height=56, corner_radius=12,
            fg_color="transparent", hover_color=Paleta.AZUL_OSCURO,
            text_color=	Paleta.HUESO, font=(FUENTE, 11, "bold"),
            command=comando,
        )

    def alternar_panel(self):
        if self.panel_abierto:
            self._cerrar_panel()
        else:
            self._abrir_panel()

    def _abrir_panel(self):
        self.panel_abierto = True
        self.panel.place(x=0, rely=1.0, y=int(self._y_actual), relwidth=1, anchor="sw")
        self.panel.lower(self.barra)  # queda detrás de la barra: parece que sale de ella
        self._animar(self._y_visible)

    def _cerrar_panel(self, animar=True):
        if animar:
            if not self.panel_abierto:
                return
            self.panel_abierto = False
            self._animar(self._y_oculto, self.panel.place_forget)
        else:  # cierre inmediato, sin animación
            if self._anim_id is not None:
                self.after_cancel(self._anim_id)
                self._anim_id = None
            self.panel_abierto = False
            self._y_actual = self._y_oculto
            self.panel.place_forget()

    def _animar(self, hasta, al_terminar=None):
        """Mueve el panel hacia 'hasta' frenando suave al llegar."""
        if self._anim_id is not None:
            self.after_cancel(self._anim_id)
            self._anim_id = None

        def paso():
            falta = hasta - self._y_actual
            if abs(falta) < 2:
                self._y_actual = hasta
                self.panel.place(y=hasta)
                self._anim_id = None
                if al_terminar:
                    al_terminar()
                return
            self._y_actual += falta * 0.3  # sube el 0.3 para más rápido, bájalo para más lento
            self.panel.place(y=int(self._y_actual))
            self._anim_id = self.after(15, paso)

        paso()

    def _pendiente(self, nombre):
        from tkinter import messagebox
        self._cerrar_panel()
        # espera a que termine la animación antes de mostrar el aviso
        self.after(260, lambda: messagebox.showinfo("SafeBus", f"{nombre}: Coming Soon!"))

    def confirmar_cierre_sesion(self):
        """Muestra una tarjeta de confirmación antes de cerrar la sesión."""
        self._cerrar_panel(animar=False)
        if getattr(self, "confirmacion", None) is None:
            self._crear_confirmacion()
        self.confirmacion.place(x=0, y=0, relwidth=1, relheight=1)
        self.confirmacion.tkraise()

    def _crear_confirmacion(self):
        # Fondo oscuro que cubre toda la ventana (así no se toca nada de atrás)
        self.confirmacion = ctk.CTkFrame( self, fg_color=Paleta.AZUL_OSCURO corner_radius=0 )

        tarjeta = ctk.CTkFrame(self.confirmacion, width=320, height=300, corner_radius=24,
                               fg_color=	Paleta.TURQUESA)
        tarjeta.pack_propagate(False)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        # Ícono de salida dentro de un círculo azul petróleo
        circulo = ctk.CTkFrame(tarjeta, width=64, height=64, corner_radius=32, fg_color=Paleta.AZUL)
        circulo.pack(pady=(26, 10))
        ctk.CTkLabel(circulo, text="", image=self._dibujar_icono("salir", 	Paleta.HUESO, 30)
                     ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(tarjeta, text="Log out?", font=(FUENTE, 20, "bold"),
                     text_color=Paleta.AZUL).pack()
        ctk.CTkLabel(tarjeta, text="Are you sure you want to log out of SafeBus?",
                     font=(FUENTE, 13), text_color=Paleta.TEXTO_SEC, wraplength=260,
                     justify="center").pack(padx=24, pady=(8, 0))

        botones = ctk.CTkFrame(tarjeta, fg_color="transparent")
        botones.pack(side="bottom", fill="x", padx=20, pady=(0, 24))
        botones.grid_columnconfigure((0, 1), weight=1, uniform="conf")
        ctk.CTkButton(botones, text="Cancel", width=10, height=46, corner_radius=12,
                      fg_color=	Paleta.AZUL, hover_color=Paleta.AZUL_SUAVE, text_color=	Paleta.HUESO,
                      font=(FUENTE, 14, "bold"),
                      command=self._cancelar_cierre).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(botones, text="Yes, log out", width=10, height=46, corner_radius=12,
                      fg_color=Paleta.MOSTAZA, hover_color=	Paleta.MOSTAZA_OSCURO, text_color=	Paleta.AZUL,
                      font=(FUENTE, 14, "bold"),
                      command=self._confirmar_cierre).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def _cancelar_cierre(self):
        self.confirmacion.place_forget()

    def _confirmar_cierre(self):
        self.confirmacion.place_forget()
        self.frames["LoginView"].entry_pass.delete(0, "end")
        self.show_frame("LoginView")

        def show_frame(self, page_name):
            """Muestra la pantalla seleccionada."""
            self._cerrar_panel(animar=(page_name != "LoginView"))

            if page_name == "LoginView":
                self.barra.grid_remove()
            else:
                self.barra.grid()

            if page_name == "DashboardView":
                self.frames[page_name].actualizar_datos()

            self.frames[page_name].tkraise()

            # Resalta el botón de la pantalla actual
            for nombre, boton in self.nav.items():
                activo = (nombre == page_name)
                boton.configure(
                    fg_color="#091720" if activo else "transparent",
                    text_color="#add6d1" if activo else "#e2cea1"
                )

        # Resalta el botón de la pantalla actual
        for nombre, boton in self.nav.items():
            activo = (nombre == page_name)
            boton.configure(fg_color=	Paleta.AZUL_OSCURO if activo else "transparent",
                            text_color=	Paleta.TURQUESA if activo else Paleta.HUESO)
