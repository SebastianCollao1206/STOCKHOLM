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

#### **2. 📦 Instalar Dependencias**
```bash
# Instalar las dependencias requeridas
pip install -r requirements.txt
```

#### **3. 🗄️ Configurar Base de Datos**
- Abre tu editor SQL 
- Crea una nueva base de datos:
  ```sql
  CREATE DATABASE stock_holm;
  ```

#### **4. ⚙️ Configurar Credenciales de la Base de Datos**
- Navega a la carpeta `app/config/`
- Abre el archivo `config.py`
- Actualiza las siguientes variables con tus credenciales:
  ```python
  DB_USER = os.getenv('DB_USER', 'tu_usuario')
  DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', 'tu_contraseña')) 
  DB_NAME = os.getenv('DB_NAME', 'nombre_de_tu_bd')
  ```

> 💡 **Nota:** Reemplaza `'tu_usuario'`, `'tu_contraseña'` y `'nombre_de_tu_bd'` con tus datos reales de MySQL.

#### **5. 📊 Importar Estructura de la Base de Datos**
- Localiza el archivo `stock_holmDB.sql` en el directorio del proyecto
- Importa este archivo en tu base de datos
- ✅ Verifica que todas las tablas se hayan creado correctamente

#### **6. 🌱 Cargar Datos Iniciales**
- Ejecuta el contenido del archivo `datos_iniciales.sql`
- Esto proporcionará datos de ejemplo para empezar a usar la aplicación

#### **7. ▶️ Ejecutar la Aplicación**
```bash
# Navega al directorio del proyecto
cd stockholm
# Ejecuta la aplicación
python run.py
```

#### **8. 🌐 Acceder a la Aplicación**
- Copia la URL que aparece en la terminal
- Pégala en tu navegador web
- 🎉 ¡La interfaz estará lista para usar!

#### **9. 👤 Primer Uso**
1. **Regístrate** como nuevo usuario
2. **Inicia sesión** con tus credenciales
3. **Explora** todas las funcionalidades disponibles

---

## 📖 Documentación Adicional

Para obtener información detallada sobre todas las funcionalidades disponibles, consulta el archivo de documentación del proyecto (no incluido en el repositorio de Git).

---

## 🛠️ Tecnologías Utilizadas
- **Backend:** Flask (Python)
- **Base de Datos:** MySQL
- **Frontend:** HTML, CSS, JavaScript
