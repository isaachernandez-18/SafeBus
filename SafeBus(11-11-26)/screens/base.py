import customtkinter as ctk
from tema import Paleta

class BaseView(ctk.CTkFrame):
    """Vista base: fondo hueso y un frame centrado (85% del ancho)."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Paleta.HUESO, corner_radius=0)
        self.controller = controller

        self.centro = ctk.CTkFrame(self, fg_color="transparent")
        self.centro.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85)
