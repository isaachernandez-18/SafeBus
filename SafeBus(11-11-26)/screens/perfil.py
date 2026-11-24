import customtkinter as ctk
from tema import Paleta, FUENTE
from datos import PERFILES, CAMPOS, iniciales


class ProfileView(ctk.CTkFrame):
    """Perfil del padre/madre y del estudiante, con selector arriba y botón para editar."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Paleta.HUESO, corner_radius=0)
        self.controller = controller
        self.actual = "padre"  # "padre" o "hijo"

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=Paleta.HUESO, corner_radius=0)
        self.scroll.pack(fill="both", expand=True)

        # --- Encabezado azul: avatar, nombre y rol ---
        h = ctk.CTkFrame(self.scroll, fg_color=Paleta.AZUL, corner_radius=0)
        h.pack(fill="x")
        ctk.CTkLabel(h, text="PROFILE", font=(FUENTE, 13, "bold"),
                     text_color=Paleta.TURQUESA).pack(anchor="w", padx=20, pady=(18, 0))

        avatar = ctk.CTkFrame(h, width=96, height=96, corner_radius=48, fg_color=Paleta.TURQUESA)
        avatar.pack(pady=(12, 10))
        self.lbl_iniciales = ctk.CTkLabel(avatar, text="", font=(FUENTE, 30, "bold"),
                                          text_color=Paleta.AZUL)
        self.lbl_iniciales.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_nombre = ctk.CTkLabel(h, text="", font=(FUENTE, 22, "bold"),
                                       text_color=Paleta.HUESO)
        self.lbl_nombre.pack()
        self.lbl_rol = ctk.CTkLabel(h, text="", font=(FUENTE, 13), text_color=Paleta.TURQUESA)
        self.lbl_rol.pack(pady=(2, 22))

        # --- Selector Parent | Student ---
        selector = ctk.CTkFrame(self.scroll, fg_color=Paleta.TURQUESA, corner_radius=16)
        selector.pack(fill="x", padx=20, pady=(20, 4))
        selector.grid_columnconfigure((0, 1), weight=1, uniform="sel")
        self.botones_sel = {}
        for col, (clave, texto) in enumerate((("padre", "Parent"), ("hijo", "Student"))):
            b = ctk.CTkButton(selector, text=texto, height=38, corner_radius=12,
                              font=(FUENTE, 13, "bold"), fg_color="transparent",
                              hover_color=Paleta.TURQUESA_OSCURO, text_color=Paleta.AZUL,
                              command=lambda c=clave: self.mostrar(c))
            b.grid(row=0, column=col, sticky="ew", padx=4, pady=4)
            self.botones_sel[clave] = b

        # --- Zona que se redibuja al cambiar de perfil o al guardar ---
        self.contenido = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.contenido.pack(fill="x", padx=20, pady=(12, 24))

        self.mostrar("padre")

    # ---------------------------------------------------------- LÓGICA
    def mostrar(self, clave):
        """Muestra el perfil 'padre' o 'hijo'. También se usa después de guardar cambios."""
        self.actual = clave
        for k, b in self.botones_sel.items():
            activo = (k == clave)
            b.configure(fg_color=Paleta.AZUL if activo else "transparent",
                        text_color=Paleta.HUESO if activo else Paleta.AZUL)
        self._dibujar()

    def editar(self, clave):
        """Abre la pantalla de edición del perfil indicado, con sus datos actuales."""
        nombre_vista = "EditParentView" if clave == "padre" else "EditStudentView"
        self.controller.frames[nombre_vista].cargar()
        self.controller.show_frame(nombre_vista)

    def _dibujar(self):
        datos = PERFILES[self.actual]
        self.lbl_iniciales.configure(text=iniciales(datos["nombre"]))
        self.lbl_nombre.configure(text=datos["nombre"])
        if self.actual == "padre":
            self.lbl_rol.configure(text="Parent / Guardian")
        else:
            partes = [datos.get("grado"), datos.get("colegio")]
            self.lbl_rol.configure(text=" · ".join(p for p in partes if p) or "Student")

        for w in self.contenido.winfo_children():
            w.destroy()

        tarjeta = ctk.CTkFrame(self.contenido, fg_color=Paleta.TURQUESA, corner_radius=16)
        tarjeta.pack(fill="x")
        for clave, etiqueta, _ayuda, _varias in CAMPOS[self.actual]:
            valor = datos.get(clave, "") or "—"
            ctk.CTkLabel(tarjeta, text=etiqueta.upper(), font=(FUENTE, 11, "bold"),
                         text_color=Paleta.TEXTO_SEC).pack(anchor="w", padx=18, pady=(14, 0))
            ctk.CTkLabel(tarjeta, text=valor, font=(FUENTE, 14, "bold"), text_color=Paleta.AZUL,
                         justify="left", anchor="w", wraplength=300).pack(anchor="w", padx=18, pady=(0, 2))
        ctk.CTkFrame(tarjeta, height=12, fg_color="transparent").pack()

        ctk.CTkButton(self.contenido, text="Edit profile", height=46, corner_radius=12,
                      fg_color=Paleta.MOSTAZA, hover_color=Paleta.MOSTAZA_OSCURO,
                      text_color=Paleta.AZUL, font=(FUENTE, 15, "bold"),
                      command=lambda: self.editar(self.actual)).pack(fill="x", pady=(16, 0))