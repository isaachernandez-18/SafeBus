import customtkinter as ctk
from tema import Paleta, FUENTE
from .base import BaseView

class MapView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ctk.CTkLabel(self.centro, text="Real-Time Map", font=(FUENTE, 22, "bold"),
                     text_color=Paleta.AZUL).pack(pady=(0, 14))

        mapa = ctk.CTkFrame(self.centro, fg_color=Paleta.TURQUESA, corner_radius=16, height=300)
        mapa.pack(fill="x")
        mapa.pack_propagate(False)
        ctk.CTkLabel(mapa, text="The map will go here later",
                     text_color=Paleta.AZUL).place(relx=0.5, rely=0.5, anchor="center")
