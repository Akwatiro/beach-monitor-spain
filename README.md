# Beach Monitor Spain 🏖️

Aplicación web para monitorear el estado en tiempo real de las playas de España por provincias.

## 🌊 Características

- **Mapa interactivo** con marcadores de playas por provincia
- **Datos en tiempo real** de condiciones meteorológicas y del mar
- **Estado de banderas** (verde, amarilla, roja)
- **Ocupación estimada** de playas
- **Calidad del agua** y certificaciones
- **Gráficos de tendencias** y datos históricos
- **Notificaciones** de cambios importantes

## 🛠️ Tecnologías

### Backend
- **Python** con FastAPI
- **SQLAlchemy** para base de datos
- **Celery** para tareas en background
- **Redis** para caché
- **PostgreSQL** como base de datos principal

### Frontend
- **React** con TypeScript
- **Material-UI** para componentes
- **Google Maps API** para mapas interactivos
- **React Query** para gestión de estado
- **Socket.IO** para actualizaciones en tiempo real

### Servicios de Google Cloud
- **Google Maps JavaScript API**
- **Google Places API**
- **Google Cloud Storage**
- **Google Cloud Run**
- **Firebase Hosting**

## 🚀 Instalación y Configuración

### Prerrequisitos
- Node.js (v18 o superior)
- Python (v3.9 o superior)
- PostgreSQL
- Redis

### Backend Setup

1. Navegar al directorio del backend:
```bash
cd backend
```

2. Crear un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. Ejecutar el servidor:
```bash
python main.py
```

### Frontend Setup

1. Navegar al directorio del frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus API keys
```

4. Ejecutar la aplicación:
```bash
npm start
```

## 📡 APIs Integradas

### AEMET (Agencia Estatal de Meteorología)
- Datos meteorológicos oficiales
- Predicciones del tiempo
- Estado del mar

### Google Cloud Services
- **Maps API**: Visualización de mapas
- **Places API**: Información de playas
- **Storage**: Imágenes y recursos

### Fuentes de Datos de Playas
- Banderas azules
- Calidad del agua (Ministerio de Sanidad)
- Webcams de playas
- Datos de ocupación

## 🗺️ Estructura del Proyecto

```
beach-monitor-spain/
├── backend/                 # API Python FastAPI
│   ├── main.py             # Punto de entrada
│   ├── requirements.txt    # Dependencias Python
│   └── .env.example       # Variables de entorno
├── frontend/               # React TypeScript App
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas principales
│   │   └── services/      # Servicios API
│   ├── package.json       # Dependencias Node.js
│   └── .env.example      # Variables de entorno
└── README.md              # Documentación
```

## 🌐 Endpoints API

### Provincias
- `GET /api/provinces` - Obtener todas las provincias costeras

### Playas
- `GET /api/beaches/{province_id}` - Obtener playas por provincia
- `GET /api/beach/{beach_id}/weather` - Condiciones meteorológicas de una playa

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

1. **Backend** (Puerto 8000):
```bash
cd backend
python main.py
```

2. **Frontend** (Puerto 3000):
```bash
cd frontend
npm start
```

### Testing
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📊 Funcionalidades Planificadas

- [ ] Integración completa con AEMET API
- [ ] Sistema de alertas por SMS/Email
- [ ] App móvil React Native
- [ ] Dashboard administrativo
- [ ] Machine Learning para predicciones
- [ ] Integración con webcams en tiempo real
- [ ] API pública para desarrolladores

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [TuGitHub](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- AEMET por proporcionar datos meteorológicos oficiales
- Google Cloud Platform por sus servicios
- Comunidades autónomas por datos de calidad de playas
