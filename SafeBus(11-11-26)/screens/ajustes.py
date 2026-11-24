import customtkinter as ctk
from tema import Paleta, FUENTE
from .base import BaseView

class SettingsView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ctk.CTkLabel(self.centro, text="Settings", font=(FUENTE, 22, "bold"),
                     text_color=Paleta.AZUL).pack(pady=(0, 16))

        tarjeta = ctk.CTkFrame(self.centro, fg_color=Paleta.TURQUESA, corner_radius=16)
        tarjeta.pack(fill="x")
        self.switch_notif = ctk.CTkSwitch(
            tarjeta, text="Enable Notifications", text_color=Paleta.AZUL,
            font=(FUENTE, 14, "bold"), fg_color=Paleta.TURQUESA_OSCURO,
            progress_color=Paleta.AZUL, button_color=Paleta.BLANCO,
            button_hover_color=Paleta.BLANCO)
        self.switch_notif.pack(anchor="w", padx=18, pady=18)

        ctk.CTkButton(
            self.centro, text="Back to Dashboard", height=44, corner_radius=12,
            fg_color=Paleta.AZUL, hover_color=Paleta.AZUL_SUAVE,
            text_color=Paleta.HUESO, font=(FUENTE, 14, "bold"),
            command=lambda: controller.show_frame("DashboardView"),
        ).pack(fill="x", pady=(20, 0))
