import os
from tema import BASE

os.chdir(BASE)  # así "icons/..." siempre se busca dentro de la carpeta del proyecto

from app import SafeBusApp

if __name__ == "__main__":
    app = SafeBusApp()
    app.mainloop()