import logging
import customtkinter as ctk
from rich.logging import RichHandler
from rich.traceback import install as rtbi
from rich.console import Console

# Rich-Traceback für schönere Fehlermeldungen bei Abstürzen
rtbi(show_locals=True)

# Konfiguration des Loggings mit RichHandler
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

logger = logging.getLogger("rich")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Logge den Start der Anwendung
        logger.info("Initialisiere [bold blue]CustomTkinter[/bold blue] Anwendung...", extra={"markup": True})

        self.title("CustomTkinter Rich Logging")
        self.geometry("600x500")

        # Variablen für die Abmessungen
        self.inner_frame_height = 40
        self.inner_frame_width = 150

        # Hauptcontainer
        self.main_container = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # Erzeuge Frames und logge den Fortschritt
        for i in range(1, 11):
            self.add_item_row(f"Element {i}")
            if i % 5 == 0:
                logger.info(f"{i} Elemente erfolgreich gerendert.")

    def add_item_row(self, text):
        # Äußerer Frame: padding 5, fensterbreit
        outer_frame = ctk.CTkFrame(self.main_container)
        outer_frame.pack(fill="x", padx=10, pady=5)

        # Innerer Frame: padding 1, feste Größe
        inner_frame = ctk.CTkFrame(
            outer_frame, 
            width=self.inner_frame_width, 
            height=self.inner_frame_height,
            fg_color="gray30"
        )
        inner_frame.pack(side="left", padx=1, pady=1)
        inner_frame.pack_propagate(False)

        label = ctk.CTkLabel(inner_frame, text=text)
        label.pack(expand=True)
        
        # Beispiel für ein Debug-Log
        logger.debug(f"Frame für '{text}' erstellt.")

if __name__ == "__main__":
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        app = App()
        logger.info("Mainloop wird gestartet.")
        app.mainloop()
    except Exception as e:
        logger.exception("Ein kritischer Fehler ist aufgetreten:")