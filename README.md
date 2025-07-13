# 📦 STOCKHOLM

> **Sistema de gestión de inventario web desarrollado con Flask y Python**

Una aplicación web moderna y eficiente para la gestión completa de tu inventario, diseñada para ser fácil de usar y altamente funcional.

---

## 🚀 Manual de Instalación

### 📋 Requisitos Previos
- Python 3.7 o superior
- Editor SQL (MySQL)
- Editor de código (recomendado: Visual Studio Code)

### 🔧 Pasos de Instalación

#### **1. 📥 Clonar el Repositorio o Descargar el Proyecto desde Git**
```bash
git clone https://github.com/SebastianCollao1206/STOCKHOLM.git
cd STOCKHOLM
```

#### **2. 🗄️ Configurar Base de Datos**
- Abre tu editor SQL 
- Crea una nueva base de datos:
  ```sql
  CREATE DATABASE stock_holm;
  ```
> 💡 **Nota:** Puedes usar cualquier nombre para la base de datos, pero recuerda actualizar la configuración del proyecto, dentro de la carpeta config, en el archivo config.py, como tus credenciales.

#### **3. 📊 Importar Estructura de la Base de Datos**
- Localiza el archivo `stock_holmDB.sql` en el directorio del proyecto
- Importa este archivo en tu base de datos
- ✅ Verifica que todas las tablas se hayan creado correctamente

#### **4. 🌱 Cargar Datos Iniciales**
- Ejecuta el contenido del archivo `datos_iniciales.sql`
- Esto proporcionará datos de ejemplo para empezar a usar la aplicación

#### **5. ▶️ Ejecutar la Aplicación**
```bash
# Navega al directorio del proyecto
cd stockholm

# Ejecuta la aplicación
python run.py
```

#### **6. 🌐 Acceder a la Aplicación**
- Copia la URL que aparece en la terminal
- Pégala en tu navegador web
- 🎉 ¡La interfaz estará lista para usar!

#### **7. 👤 Primer Uso**
1. **Regístrate** como nuevo usuario
2. **Inicia sesión** con tus credenciales
3. **Explora** todas las funcionalidades disponibles

---

## 📖 Documentación Adicional

Para obtener información detallada sobre todas las funcionalidades disponibles, consulta el archivo `Documentacion_stock_holm.md` incluido en el proyecto.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask (Python)
- **Base de Datos:** SQL
- **Frontend:** HTML, CSS, JavaScript
