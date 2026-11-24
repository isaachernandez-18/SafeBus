import customtkinter as ctk
from tkinter import messagebox
from tema import Paleta, FUENTE
from datos import PERFILES, CAMPOS


class FormView(ctk.CTkFrame):
    """Pantalla de edición reutilizable. Las pantallas hijas solo definen `clave` y `titulo`."""
    clave = "padre"
    titulo = "Edit profile"

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Paleta.HUESO, corner_radius=0)
        self.controller = controller
        self.campos = {}  # clave del dato -> (widget, ¿varias líneas?)

        scroll = ctk.CTkScrollableFrame(self, fg_color=Paleta.HUESO, corner_radius=0)
        scroll.pack(fill="both", expand=True)

        # --- Encabezado azul con botón de volver ---
        h = ctk.CTkFrame(scroll, fg_color=Paleta.AZUL, corner_radius=0)
        h.pack(fill="x")
        ctk.CTkButton(h, text="Back", width=70, height=32, corner_radius=10,
                      fg_color=Paleta.AZUL_SUAVE, hover_color=Paleta.AZUL_OSCURO,
                      text_color=Paleta.HUESO, font=(FUENTE, 12, "bold"),
                      command=self._volver).pack(anchor="w", padx=20, pady=(18, 0))
        ctk.CTkLabel(h, text=self.titulo, font=(FUENTE, 22, "bold"),
                     text_color=Paleta.HUESO).pack(anchor="w", padx=20, pady=(10, 20))

        # --- Campos ---
        tarjeta = ctk.CTkFrame(scroll, fg_color=Paleta.TURQUESA, corner_radius=16)
        tarjeta.pack(fill="x", padx=20, pady=(20, 0))
        for clave, etiqueta, ayuda, varias in CAMPOS[self.clave]:
            ctk.CTkLabel(tarjeta, text=etiqueta, font=(FUENTE, 12, "bold"),
                         text_color=Paleta.AZUL).pack(anchor="w", padx=18, pady=(14, 4))
            if varias:
                w = ctk.CTkTextbox(tarjeta, height=90, corner_radius=12, fg_color=Paleta.BLANCO,
                                   border_color=Paleta.AZUL, border_width=1,
                                   text_color=Paleta.AZUL, font=(FUENTE, 13))
            else:
                w = ctk.CTkEntry(tarjeta, placeholder_text=ayuda, height=42, corner_radius=12,
                                 fg_color=Paleta.BLANCO, border_color=Paleta.AZUL, border_width=1,
                                 text_color=Paleta.AZUL, placeholder_text_color="#6b7c85",
                                 font=(FUENTE, 13))
            w.pack(fill="x", padx=18)
            self.campos[clave] = (w, varias)
        ctk.CTkFrame(tarjeta, height=16, fg_color="transparent").pack()

        # --- Botones: Cancel (secundario) y Save changes (principal, mostaza) ---
        botones = ctk.CTkFrame(scroll, fg_color="transparent")
        botones.pack(fill="x", padx=20, pady=(16, 24))
        botones.grid_columnconfigure((0, 1), weight=1, uniform="bt")
        ctk.CTkButton(botones, text="Cancel", height=46, corner_radius=12,
                      fg_color=Paleta.AZUL, hover_color=Paleta.AZUL_SUAVE,
                      text_color=Paleta.HUESO, font=(FUENTE, 14, "bold"),
                      command=self._volver).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(botones, text="Save changes", height=46, corner_radius=12,
                      fg_color=Paleta.MOSTAZA, hover_color=Paleta.MOSTAZA_OSCURO,
                      text_color=Paleta.AZUL, font=(FUENTE, 14, "bold"),
                      command=self._guardar).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    # ---------------------------------------------------------- LÓGICA
    def cargar(self):
        """Rellena el formulario con los datos actuales del perfil."""
        datos = PERFILES[self.clave]
        for clave, (w, varias) in self.campos.items():
            valor = datos.get(clave, "")
            if varias:
                w.delete("1.0", "end")
                w.insert("1.0", valor)
            else:
                w.delete(0, "end")
                w.insert(0, valor)

    def _leer(self, clave):
        w, varias = self.campos[clave]
        return (w.get("1.0", "end-1c") if varias else w.get()).strip()

    def _guardar(self):
        nuevos = {clave: self._leer(clave) for clave in self.campos}
        if not nuevos.get("nombre"):
            messagebox.showwarning("SafeBus", "Full name is required.")
            return
        if nuevos.get("email") and "@" not in nuevos["email"]:
            messagebox.showwarning("SafeBus", "Please enter a valid email address.")
            return
        PERFILES[self.clave].update(nuevos)
        self.controller.frames["ProfileView"].mostrar(self.clave)
        self.controller.show_frame("ProfileView")

    def _volver(self):
        self.controller.show_frame("ProfileView")