import os
import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class AppController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Restaurante App")
        self.root.geometry("800x600")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_prod = os.path.join(base_dir, "datos", "productos.json")
        ruta_usr = os.path.join(base_dir, "datos", "usuarios.json")
        ruta_ven = os.path.join(base_dir, "datos", "ventas.json")

        self.restaurante_servicio = RestauranteServicio(ruta_prod, ruta_usr, ruta_ven)

        self.login_view = LoginView(self.root, self.restaurante_servicio, self.mostrar_main)
        self.main_view = MainView(self.root, self.restaurante_servicio, self.mostrar_login)

        self.mostrar_login()

    def mostrar_login(self) -> None:
        self.main_view.pack_forget()
        self.login_view.pack(fill="both", expand=True)

    def mostrar_main(self) -> None:
        self.login_view.pack_forget()
        self.main_view.refrescar_datos()
        self.main_view.pack(fill="both", expand=True)

def main():
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()

if __name__ == "__main__":
    main()