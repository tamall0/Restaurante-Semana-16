import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from PIL import Image, ImageTk

class MainView(ttk.Frame):
    def __init__(self, parent: tk.Widget, restaurante_servicio, on_logout: Callable[[], None]):
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.on_logout = on_logout

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        # Encabezado
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")

        dir_ui = os.path.dirname(os.path.abspath(__file__))
        dir_raiz = os.path.dirname(dir_ui)
        ruta_icono = os.path.join(dir_raiz, "assets", "icono.png")

        if os.path.exists(ruta_icono):
            try:
                img_pil = Image.open(ruta_icono)
                img_pil.thumbnail((32, 32))
                self.icono_img = ImageTk.PhotoImage(img_pil)

                lbl_icon = ttk.Label(header, image=self.icono_img)
                lbl_icon.image = self.icono_img
                lbl_icon.pack(side="left", padx=(0, 10))
            except Exception as e:
                print(f"Error al renderizar el icono: {e}")

        usr_actual = self.restaurante_servicio.obtener_usuario_actual()
        info_usr = f"Usuario: {usr_actual.nombre} ({usr_actual.rol})" if usr_actual else ""

        ttk.Label(header, text="Panel Principal - Restaurante App", font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Label(header, text=info_usr, font=("Helvetica", 10, "italic")).pack(side="left", padx=20)
        ttk.Button(header, text="Cerrar Sesión", command=self.on_logout).pack(side="right")

        # Control de Pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_productos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_productos, text="Productos")

        # Restricción de acceso: Solo 'Administrador' ve la pestaña de Usuarios
        if usr_actual and usr_actual.rol == "Administrador":
            self.tab_usuarios = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.tab_usuarios, text="Gestión de Usuarios")
            self._construir_pestana_usuarios()

        self.tab_ventas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_ventas, text="Ventas")

        self._construir_pestana_productos()
        self._construir_pestana_ventas()

    def _construir_pestana_productos(self) -> None:
        for widget in self.tab_productos.winfo_children():
            widget.destroy()

        productos = self.restaurante_servicio.obtener_productos()
        ttk.Label(self.tab_productos, text=f"Total Productos Registrados: {len(productos)}", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))

        listbox = tk.Listbox(self.tab_productos, font=("Consolas", 10))
        listbox.pack(fill="both", expand=True)

        for p in productos:
            listbox.insert(tk.END, str(p))

    def _construir_pestana_usuarios(self) -> None:
        # Formulario
        frame_form = ttk.LabelFrame(self.tab_usuarios, text=" Datos del Usuario ", padding=10)
        frame_form.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="ID Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_usr_id = ttk.Entry(frame_form, width=20)
        self.txt_usr_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_usr_nombre = ttk.Entry(frame_form, width=25)
        self.txt_usr_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Contraseña:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_usr_clave = ttk.Entry(frame_form, width=20, show="*")
        self.txt_usr_clave.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Rol:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.combo_usr_rol = ttk.Combobox(frame_form, values=["Administrador", "Empleado", "Cliente"], state="readonly", width=22)
        self.combo_usr_rol.current(2)
        self.combo_usr_rol.grid(row=1, column=3, padx=5, pady=5)

        # Botones mediante command=
        frame_botones = ttk.Frame(frame_form)
        frame_botones.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        btn_registrar = ttk.Button(frame_botones, text="Registrar", command=self._guardar_usuario)
        btn_registrar.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self._actualizar_usuario)
        btn_actualizar.pack(side="left", padx=5)

        btn_eliminar = ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_usuario)
        btn_eliminar.pack(side="left", padx=5)

        btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_formulario_usuarios)
        btn_limpiar.pack(side="left", padx=5)

        # Tabla Treeview
        frame_tabla = ttk.LabelFrame(self.tab_usuarios, text=" Usuarios Registrados ", padding=10)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "rol")
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        self.tree_usuarios.heading("id", text="ID Usuario")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("rol", text="Rol")

        self.tree_usuarios.column("id", width=120, anchor="center")
        self.tree_usuarios.column("nombre", width=250)
        self.tree_usuarios.column("rol", width=150, anchor="center")

        self.tree_usuarios.pack(fill="both", expand=True)

        # ASOCIACIÓN DE EVENTOS CON BIND()
        # 1. Seleccionar en la tabla -> <<TreeviewSelect>>
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_treeview_select)

        # 2. Atajo <Return> en los campos -> Confirmar Registro
        self.txt_usr_id.bind("<Return>", lambda e: self._guardar_usuario())
        self.txt_usr_nombre.bind("<Return>", lambda e: self._guardar_usuario())
        self.txt_usr_clave.bind("<Return>", lambda e: self._guardar_usuario())

        # 3. Atajo <Escape> en toda la pestaña -> Limpiar formulario
        self.tab_usuarios.bind_all("<Escape>", lambda e: self._limpiar_formulario_usuarios())

        # 4. Cambio de selección en Combobox -> <<ComboboxSelected>>
        self.combo_usr_rol.bind("<<ComboboxSelected>>", self._on_combobox_rol_selected)

        self._cargar_tabla_usuarios()

    def _cargar_tabla_usuarios(self) -> None:
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        for u in self.restaurante_servicio.obtener_usuarios():
            self.tree_usuarios.insert("", tk.END, values=(u.id_usuario, u.nombre, u.rol))

    # CALLBACKS Y EVENTOS
    def _on_treeview_select(self, event: tk.Event) -> None:
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return

        item = self.tree_usuarios.item(seleccion[0])
        id_usuario = item["values"][0]

        # Consultar objeto mediante RestauranteServicio
        usuario = self.restaurante_servicio.obtener_usuario_por_id(str(id_usuario))
        if usuario:
            self.txt_usr_id.delete(0, tk.END)
            self.txt_usr_id.insert(0, usuario.id_usuario)
            self.txt_usr_id.config(state="disabled")  # Deshabilitar ID para evitar cambios de clave primaria

            self.txt_usr_nombre.delete(0, tk.END)
            self.txt_usr_nombre.insert(0, usuario.nombre)

            self.txt_usr_clave.delete(0, tk.END)
            self.txt_usr_clave.insert(0, usuario.clave)

            self.combo_usr_rol.set(usuario.rol)

    def _on_combobox_rol_selected(self, event: tk.Event) -> None:
        rol_seleccionado = self.combo_usr_rol.get()
        print(f"Evento <<ComboboxSelected>>: Rol seleccionado -> {rol_seleccionado}")

    def _guardar_usuario(self) -> None:
        if self.txt_usr_id["state"] == "disabled":
            messagebox.showinfo("Información", "El usuario ya existe. Si desea modificar sus datos utilice el botón 'Actualizar'.")
            return

        id_u = self.txt_usr_id.get().strip()
        nom = self.txt_usr_nombre.get().strip()
        cla = self.txt_usr_clave.get().strip()
        rol = self.combo_usr_rol.get()

        exito, msg = self.restaurante_servicio.registrar_usuario(id_u, nom, cla, rol)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario_usuarios()
            self._cargar_tabla_usuarios()
            self.refrescar_datos()
        else:
            messagebox.showerror("Error", msg)

    def _actualizar_usuario(self) -> None:
        id_u = self.txt_usr_id.get().strip()
        nom = self.txt_usr_nombre.get().strip()
        cla = self.txt_usr_clave.get().strip()
        rol = self.combo_usr_rol.get()

        exito, msg = self.restaurante_servicio.actualizar_usuario(id_u, nom, cla, rol)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario_usuarios()
            self._cargar_tabla_usuarios()
            self.refrescar_datos()
        else:
            messagebox.showerror("Error", msg)

    def _eliminar_usuario(self) -> None:
        id_u = self.txt_usr_id.get().strip()
        if not id_u:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al usuario '{id_u}'?"):
            exito, msg = self.restaurante_servicio.eliminar_usuario(id_u)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self._limpiar_formulario_usuarios()
                self._cargar_tabla_usuarios()
                self.refrescar_datos()
            else:
                messagebox.showerror("Error", msg)

    def _limpiar_formulario_usuarios(self) -> None:
        self.txt_usr_id.config(state="normal")
        self.txt_usr_id.delete(0, tk.END)
        self.txt_usr_nombre.delete(0, tk.END)
        self.txt_usr_clave.delete(0, tk.END)
        self.combo_usr_rol.current(2)

        # Deseleccionar la tabla
        if hasattr(self, "tree_usuarios") and self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())

    def _construir_pestana_ventas(self) -> None:
        for widget in self.tab_ventas.winfo_children():
            widget.destroy()

        frame_form = ttk.LabelFrame(self.tab_ventas, text=" Registrar Nueva Venta ", padding=10)
        frame_form.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5)
        self.combo_usuarios = ttk.Combobox(frame_form, state="readonly", width=30)
        self.combo_usuarios.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Producto:").grid(row=0, column=2, sticky="w", padx=5)
        self.combo_productos = ttk.Combobox(frame_form, state="readonly", width=30)
        self.combo_productos.grid(row=0, column=3, padx=5, pady=5)

        btn_registrar = ttk.Button(frame_form, text="Registrar Venta", command=self._callback_registrar_venta)
        btn_registrar.grid(row=0, column=4, padx=10, pady=5)

        frame_tabla = ttk.LabelFrame(self.tab_ventas, text=" Ventas Registradas ", padding=10)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "usuario", "producto", "fecha", "total")
        self.tree_ventas = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        self.tree_ventas.heading("id", text="ID Venta")
        self.tree_ventas.heading("usuario", text="Usuario")
        self.tree_ventas.heading("producto", text="Producto ID")
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("id", width=70, anchor="center")
        self.tree_ventas.column("usuario", width=120)
        self.tree_ventas.column("producto", width=100, anchor="center")
        self.tree_ventas.column("fecha", width=150, anchor="center")
        self.tree_ventas.column("total", width=100, anchor="e")

        self.tree_ventas.pack(fill="both", expand=True)

    def _callback_registrar_venta(self) -> None:
        sel_usuario = self.combo_usuarios.get()
        sel_producto = self.combo_productos.get()

        if not sel_usuario or not sel_producto:
            messagebox.showwarning("Atención", "Debe seleccionar un usuario y un producto.")
            return

        try:
            # Extraer ID del usuario
            id_usuario = sel_usuario.split(" - ")[0].strip()
            
            # Extraer ID del producto como entero
            id_producto_raw = sel_producto.split(" - ")[0].strip()
            # Limpiar posible símbolo '#' si existiera
            id_producto_clean = id_producto_raw.replace("#", "")
            id_producto = int(id_producto_clean)

            exito, mensaje = self.restaurante_servicio.registrar_venta(id_usuario, id_producto)

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.refrescar_datos()  # Refresca la tabla inmediatamente
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error de Formato", f"No se pudo procesar la selección: {e}")

    def refrescar_datos(self) -> None:
        self._construir_pestana_productos()

        usuarios = self.restaurante_servicio.obtener_usuarios()
        productos = self.restaurante_servicio.obtener_productos()

        if hasattr(self, "combo_usuarios") and hasattr(self, "combo_productos"):
            self.combo_usuarios["values"] = [f"{u.id_usuario} - {u.nombre}" for u in usuarios]
            self.combo_productos["values"] = [f"{p.id_producto} - {p.nombre} (${p.precio:.2f})" for p in productos]

            if usuarios:
                self.combo_usuarios.current(0)
            if productos:
                self.combo_productos.current(0)

        if hasattr(self, "tree_ventas"):
            for item in self.tree_ventas.get_children():
                self.tree_ventas.delete(item)

            for v in self.restaurante_servicio.obtener_ventas():
                self.tree_ventas.insert("", tk.END, values=(v.id_venta, v.usuario_id, v.producto_id, v.fecha, f"${v.total:.2f}"))