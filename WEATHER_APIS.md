# Configuración de APIs Meteorológicas

## 🌤️ AEMET (Agencia Estatal de Meteorología)

AEMET es la fuente oficial de datos meteorológicos de España.

### Cómo obtener la API Key:

1. **Registro**: Ve a https://opendata.aemet.es/centrodedescargas/obtencionAPIKey
2. **Completa el formulario** con tus datos personales
3. **Acepta los términos** de uso de los datos
4. **Recibe la API Key** por email (puede tardar unos días)
5. **Agrega la clave** al archivo `.env`:
   ```
   AEMET_API_KEY=tu-clave-aemet-aqui
   ```

### Datos disponibles:
- ✅ Temperatura del aire
- ✅ Humedad
- ✅ Viento (velocidad y dirección)
- ✅ Presión atmosférica
- ✅ Visibilidad
- ✅ Precipitación
- ❌ Temperatura del agua (requiere datos marítimos)
- ❌ Oleaje (requiere datos marítimos)

## 🌍 OpenWeatherMap

Alternativa internacional con buena cobertura de España.

### Cómo obtener la API Key:

1. **Registro**: Ve a https://openweathermap.org/api
2. **Crea una cuenta** gratuita
3. **Ve a "API Keys"** en tu perfil
4. **Copia la clave** generada automáticamente
5. **Agrega la clave** al archivo `.env`:
   ```
   OPENWEATHER_API_KEY=tu-clave-openweather-aqui
   ```

### Plan gratuito:
- 60 llamadas/minuto
- 1,000,000 llamadas/mes
- Datos actuales y pronóstico
- Índice UV incluido

### Datos disponibles:
- ✅ Temperatura del aire
- ✅ Humedad
- ✅ Viento (velocidad y dirección)
- ✅ Presión atmosférica
- ✅ Visibilidad
- ✅ Índice UV
- ✅ Condiciones meteorológicas
- ❌ Temperatura del agua
- ❌ Oleaje

## 🌊 Datos Marítimos

Para datos específicos del mar (oleaje, temperatura del agua), necesitamos fuentes especializadas:

### Opciones disponibles:

1. **Puertos del Estado** (España)
   - URL: http://www.puertos.es/es-es/oceanografia/Paginas/portus.aspx
   - Datos oficiales de boyas oceanográficas
   - Gratuito pero requiere parsing manual

2. **WorldWeatherOnline Marine API**
   - URL: https://www.worldweatheronline.com/developer/api/docs/marine-weather-api.aspx
   - API comercial con datos marítimos
   - Plan gratuito: 500 llamadas/mes

3. **Stormglass.io**
   - URL: https://stormglass.io/
   - API premium para datos marítimos
   - Plan gratuito: 10 llamadas/día

## 📋 Configuración Paso a Paso

### 1. Copia el archivo de ejemplo:
```bash
cp backend/.env.example backend/.env
```

### 2. Edita el archivo `.env` con tus claves:
```bash
# Weather APIs
AEMET_API_KEY=eyJhbGciOiJIUzI1NiJ9...  # Tu clave de AEMET
OPENWEATHER_API_KEY=abcdef123456789...   # Tu clave de OpenWeatherMap
MARINE_API_KEY=tu-clave-marina...        # Opcional: para datos marítimos
```

### 3. Reinicia el servidor backend:
```bash
cd backend
python main.py
```

## 🧪 Pruebas

### Endpoints disponibles:

```bash
# Datos de una playa específica
GET /api/beach/1/weather

# Resumen meteorológico por provincia
GET /api/province/1/weather

# Alertas meteorológicas
GET /api/weather/alerts

# Múltiples playas a la vez
GET /api/beaches/batch/weather?beach_ids=1,2,3
```

### Respuesta de ejemplo:
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
  "pressure": 1015.2,
  "visibility": 10,
  "uv_index": 7,
  "timestamp": "2025-07-29T14:30:00Z",
  "source": "AEMET"
}
```

## ⚠️ Limitaciones y Fallbacks

- **Sin API Keys**: El sistema usará datos simulados realistas
- **Error en APIs**: Fallback automático entre AEMET → OpenWeatherMap → Simulación
- **Rate Limits**: Implementado caché automático para reducir llamadas
- **Datos Marítimos**: Simulación basada en ubicación geográfica

## 🔧 Próximas Mejoras

1. **Caché con Redis** para reducir llamadas a APIs
2. **Base de datos** para histórico de datos
3. **WebSockets** para actualizaciones en tiempo real
4. **Integración con Copernicus** (EU Earth Observation)
5. **Datos de satélite** para temperatura del agua
