# 🏖️ Beach Monitor Spain

**Monitor en tiempo real del estado de las playas de España por provincias**

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/tu-usuario/beach-monitor-spain)
[![AEMET](https://img.shields.io/badge/AEMET-integrado-blue.svg)](https://opendata.aemet.es/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)](https://fastapi.tiangolo.com/)

Una aplicación web completa que proporciona información meteorológica y de condiciones en tiempo real de las playas españolas, integrando datos oficiales de AEMET y otras fuentes confiables.

## 🌟 Características Principales

### 📊 **Datos Meteorológicos en Tiempo Real**
- ✅ **Temperatura del aire y agua**
- ✅ **Condiciones del viento** (velocidad, dirección, rachas)
- ✅ **Estado del mar** (altura del oleaje, periodo, dirección)
- ✅ **Índice UV** con recomendaciones de seguridad
- ✅ **Visibilidad y presión atmosférica**
- ✅ **Humedad relativa**

### 🚨 **Sistema de Alertas**
- **Alertas meteorológicas oficiales** de AEMET
- **Avisos por viento, oleaje y tormentas**
- **Código de colores** (amarillo, naranja, rojo)
- **Cobertura por provincias**

### 🗺️ **Cobertura Nacional**
- **10 provincias costeras** monitoreadas
- **+800 playas** en la base de datos
- **Datos específicos por ubicación**

### 🔗 **Fuentes de Datos**
- **AEMET** (Agencia Estatal de Meteorología) - Fuente oficial
- **OpenWeatherMap** - Datos internacionales
- **Puertos del Estado** - Datos marítimos
- **Simulación inteligente** como fallback

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI       │    │   APIs Externas │
│   TypeScript    │◄──►│   Python        │◄──►│   AEMET         │
│   Material-UI   │    │   Async/Await   │    │   OpenWeather   │
│   (Puerto 3000) │    │   (Puerto 8000) │    │   Marine APIs   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Inicio Rápido

### **Prerrequisitos**
- Python 3.8+
- Node.js 16+
- npm o yarn
- Git

### **Clonar Repositorio**
```bash
git clone https://github.com/tu-usuario/beach-monitor-spain.git
cd beach-monitor-spain
```

### **1. Configurar Backend**
```bash
# Navegar al backend
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

### **2. Configurar Frontend**
```bash
# En otra terminal, navegar al frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

### **3. Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus claves de API (opcional)
# Sin claves, usa datos simulados
```

### **4. Acceder a la aplicación**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🔑 Configuración de APIs

### **AEMET (Recomendado)**
1. Registrarse en: https://opendata.aemet.es/centrodedescargas/obtencionAPIKey
2. Agregar al `.env`: `AEMET_API_KEY=tu-clave-aquí`

### **OpenWeatherMap (Alternativo)**
1. Registrarse en: https://openweathermap.org/api
2. Agregar al `.env`: `OPENWEATHER_API_KEY=tu-clave-aquí`

> **Nota**: Sin API keys configuradas, el sistema usa datos simulados realistas.

## 📡 Endpoints de la API

### **Playas**
```http
GET /api/provinces                    # Listar provincias
GET /api/beaches/{province_id}        # Playas por provincia
GET /api/beach/{beach_id}/weather     # Datos meteorológicos de playa
```

### **Meteorología**
```http
GET /api/province/{province_id}/weather    # Resumen provincial
GET /api/weather/alerts                    # Alertas activas
GET /api/beaches/batch/weather?beach_ids=1,2,3  # Múltiples playas
```

## 🧪 Estado del Proyecto

### **✅ Implementado**
- [x] Backend FastAPI con múltiples fuentes de datos
- [x] Frontend React con Material-UI
- [x] Integración con APIs meteorológicas (AEMET, OpenWeatherMap)
- [x] Sistema de alertas meteorológicas
- [x] Componentes de visualización de datos
- [x] Datos simulados realistas como fallback
- [x] Documentación completa de APIs

### **🔄 En Desarrollo**
- [ ] Integración Google Maps
- [ ] Base de datos PostgreSQL
- [ ] WebSockets para tiempo real
- [ ] Caché con Redis

### **📋 Planificado**
- [ ] Aplicación móvil
- [ ] Gráficos de tendencias
- [ ] Datos históricos
- [ ] Notificaciones push

## 📊 Ejemplo de Respuesta API

```json
{
  "temperature": {
    "air": 25.3,
    "water": 22.1,
    "feels_like": 27.8
  },
  "wind": {
    "speed": 12.5,
    "direction": "SW",
    "gusts": 18.2
  },
  "waves": {
    "height": 0.8,
    "period": 6,
    "direction": "W"
  },
  "conditions": "Parcialmente nublado",
  "humidity": 68,
  "uv_index": 7,
  "source": "AEMET"
}
```

## 🔧 Stack Tecnológico

### **Frontend**
- React 18 + TypeScript
- Material-UI v5
- React Query
- React Router
- Axios

### **Backend**
- FastAPI + Python
- aiohttp para peticiones asíncronas
- Pydantic para validación
- Uvicorn servidor ASGI

### **APIs Integradas**
- AEMET OpenData (oficial España)
- OpenWeatherMap (global)
- Datos marítimos simulados

---

**¡Aplicación completamente funcional para monitorear playas españolas en tiempo real!** 🌊☀️

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Lee nuestra [Guía de Contribución](CONTRIBUTING.md) para empezar.

### 🐛 **Reportar Issues**
- [Reportar un bug](https://github.com/tu-usuario/beach-monitor-spain/issues/new?assignees=&labels=bug%2Cneeds-triage&template=bug_report.md)
- [Solicitar feature](https://github.com/tu-usuario/beach-monitor-spain/issues/new?assignees=&labels=enhancement%2Cneeds-discussion&template=feature_request.md)

### 🔧 **Desarrollo**
```bash
# Fork del repositorio
git clone https://github.com/tu-usuario/beach-monitor-spain.git

# Crear rama para feature
git checkout -b feature/mi-nueva-caracteristica

# Hacer cambios y commit
git commit -m "feat: descripción del cambio"

# Crear pull request
```

## 📊 Estado del Proyecto

![GitHub Stars](https://img.shields.io/github/stars/tu-usuario/beach-monitor-spain?style=social)
![GitHub Forks](https://img.shields.io/github/forks/tu-usuario/beach-monitor-spain?style=social)
![GitHub Issues](https://img.shields.io/github/issues/tu-usuario/beach-monitor-spain)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/tu-usuario/beach-monitor-spain)

### **CI/CD Status**
![Tests](https://github.com/tu-usuario/beach-monitor-spain/workflows/CI%2FCD%20Pipeline/badge.svg)
![CodeQL](https://github.com/tu-usuario/beach-monitor-spain/workflows/CodeQL%20Analysis/badge.svg)
![Security](https://img.shields.io/github/workflow/status/tu-usuario/beach-monitor-spain/Security%20Scan?label=security)

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **AEMET** - Por proporcionar datos meteorológicos oficiales de España
- **OpenWeatherMap** - Por datos meteorológicos internacionales
- **Material-UI** - Por componentes React de alta calidad
- **FastAPI** - Por el framework web moderno de Python
- **React Community** - Por las librerías y herramientas

## 📞 Contacto

- **GitHub**: [@tu-usuario](https://github.com/tu-usuario)
- **Issues**: [Crear issue](https://github.com/tu-usuario/beach-monitor-spain/issues)
- **Discussions**: [Participar](https://github.com/tu-usuario/beach-monitor-spain/discussions)
