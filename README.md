# Restaurante App - Sistema de Gestión (Semana 16)

Aplicación de escritorio construida con **Python** y **Tkinter** para la gestión modular de un restaurante.

## Novedades de la Semana 16
- **Control de Acceso por Roles**: Asignación de roles (`Administrador`, `Empleado`, `Cliente`) en la entidad `Usuario`.
- **Manejo Avanzado de Eventos (`bind`)**:
  - `<<TreeviewSelect>>`: Carga automatizada de datos desde la tabla hacia el formulario.
  - `<Return>`: Atajo de teclado para la confirmación rápida del formulario.
  - `<Escape>`: Limpieza del formulario y cancelación de selecciones en la tabla.
  - `<<ComboboxSelected>>`: Evento para responder dinámicamente al cambio de rol.
- **Persistencia Extendida**: Almacenamiento continuo de usuarios con atributo de rol en `datos/usuarios.json`.

## Estructura del Proyecto
```text
restaurante_app/
├── assets/             # Recursos visuales (logo.png, icono.png)
├── datos/              # Archivos JSON de persistencia
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/            # Clases y modelos del sistema
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/          # Capa de lógica de negocio y persistencia
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/                 # Vistas e interfaz gráfica Tkinter
│   ├── login_view.py
│   └── main_view.py
├── main.py             # Punto de entrada de la aplicación
└── README.md
