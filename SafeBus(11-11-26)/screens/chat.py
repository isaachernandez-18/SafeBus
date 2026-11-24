import customtkinter as ctk
from tema import Paleta, FUENTE
from .base import BaseView

class ChatView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ctk.CTkLabel(self.centro, text="Chat", font=(FUENTE, 22, "bold"),
                     text_color=Paleta.AZUL).pack(pady=(0, 14))

        caja = ctk.CTkFrame(self.centro, fg_color=Paleta.TURQUESA, corner_radius=16, height=200)
        caja.pack(fill="x")
        caja.pack_propagate(False)
        ctk.CTkLabel(caja, text="The chat will go here later",
                     text_color=Paleta.AZUL).place(relx=0.5, rely=0.5, anchor="center")
