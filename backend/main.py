"""
Beach Monitor Spain - FastAPI Backend
Real-time monitoring of Spanish beaches by provinces
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv
from services.weather_service import WeatherServiceManager

# Load environment variables
load_dotenv()

# Initialize services
weather_manager = WeatherServiceManager()

# Initialize FastAPI app
app = FastAPI(
    title="Beach Monitor Spain API",
    description="API para monitorear el estado en tiempo real de las playas de España",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Beach Monitor Spain API está funcionando"}

@app.get("/api/provinces")
async def get_provinces():
    """Obtener todas las provincias costeras de España"""
    provinces = [
        {"id": 1, "name": "Andalucía", "beaches_count": 145},
        {"id": 2, "name": "Valencia", "beaches_count": 89},
        {"id": 3, "name": "Cataluña", "beaches_count": 112},
        {"id": 4, "name": "Galicia", "beaches_count": 126},
        {"id": 5, "name": "Murcia", "beaches_count": 67},
        {"id": 6, "name": "Asturias", "beaches_count": 78},
        {"id": 7, "name": "Cantabria", "beaches_count": 56},
        {"id": 8, "name": "País Vasco", "beaches_count": 45},
        {"id": 9, "name": "Islas Baleares", "beaches_count": 95},
        {"id": 10, "name": "Islas Canarias", "beaches_count": 134}
    ]
    return {"provinces": provinces}

@app.get("/api/beaches/{province_id}")
async def get_beaches_by_province(province_id: int):
    """Obtener playas por provincia"""
    # Datos de ejemplo - en producción vendrían de la base de datos
    if province_id == 1:  # Andalucía
        beaches = [
            {
                "id": 1,
                "name": "Playa de La Malagueta",
                "province": "Málaga",
                "coordinates": {"lat": 36.7196, "lng": -4.4214},
                "temperature_water": 22,
                "temperature_air": 28,
                "wave_height": 0.8,
                "wind_speed": 15,
                "flag_status": "green",
                "occupancy": 65,
                "quality_rating": 4.5
            },
            {
                "id": 2,
                "name": "Playa de Bolonia",
                "province": "Cádiz",
                "coordinates": {"lat": 36.0858, "lng": -5.7708},
                "temperature_water": 21,
                "temperature_air": 26,
                "wave_height": 1.2,
                "wind_speed": 20,
                "flag_status": "yellow",
                "occupancy": 45,
                "quality_rating": 4.8
            }
        ]
    else:
        beaches = []
    
    return {"beaches": beaches, "province_id": province_id}

@app.get("/api/beach/{beach_id}/weather")
async def get_beach_weather(beach_id: int):
    """Obtener condiciones meteorológicas detalladas de una playa"""
    
    # Datos de ejemplo de coordenadas de playas españolas
    beach_coordinates = {
        1: {"lat": 36.7196, "lng": -4.4214, "province_code": "6155A"},  # Málaga
        2: {"lat": 36.0858, "lng": -5.7708, "province_code": "5960"},   # Cádiz
        3: {"lat": 41.3851, "lng": 2.1734, "province_code": "0076"},    # Barcelona
        4: {"lat": 43.4647, "lng": -3.8044, "province_code": "1109"},   # Santander
        5: {"lat": 39.4699, "lng": 2.7388, "province_code": "0149"},    # Palma de Mallorca
    }
    
    if beach_id not in beach_coordinates:
        # Usar coordenadas por defecto
        coordinates = {"lat": 36.7196, "lng": -4.4214, "province_code": "6155A"}
    else:
        coordinates = beach_coordinates[beach_id]
    
    try:
        # Obtener datos meteorológicos reales de múltiples fuentes
        weather_data = await weather_manager.get_complete_weather_data(
            lat=coordinates["lat"],
            lon=coordinates["lng"],
            province_code=coordinates.get("province_code")
        )
        
        # Agregar información adicional de la playa
        weather_data["beach_id"] = beach_id
        weather_data["coordinates"] = {
            "lat": coordinates["lat"],
            "lng": coordinates["lng"]
        }
        
        return weather_data
        
    except Exception as e:
        # En caso de error, devolver datos de ejemplo
        print(f"Error fetching weather data: {e}")
        return {
            "beach_id": beach_id,
            "timestamp": "2025-07-29T10:00:00Z",
            "temperature": {
                "air": 28,
                "water": 22,
                "feels_like": 31
            },
            "wind": {
                "speed": 15,
                "direction": "SW",
                "gusts": 22
            },
            "waves": {
                "height": 0.8,
                "period": 6,
                "direction": "W"
            },
            "visibility": 10,
            "humidity": 68,
            "uv_index": 8,
            "conditions": "Soleado",
            "source": "Error - usando datos de ejemplo"
        }

@app.get("/api/province/{province_id}/weather")
async def get_province_weather_summary(province_id: int):
    """Obtener resumen meteorológico de una provincia"""
    
    # Coordenadas centrales de cada provincia costera
    province_coordinates = {
        1: {"lat": 36.5, "lng": -5.5, "name": "Andalucía", "code": "6155A"},
        2: {"lat": 39.5, "lng": -0.5, "name": "Valencia", "code": "8414A"},
        3: {"lat": 41.8, "lng": 2.5, "name": "Cataluña", "code": "0076"},
        4: {"lat": 42.8, "lng": -8.5, "name": "Galicia", "code": "1387"},
        5: {"lat": 37.8, "lng": -1.1, "name": "Murcia", "code": "7178I"},
        6: {"lat": 43.5, "lng": -6.0, "name": "Asturias", "code": "1249I"},
        7: {"lat": 43.4, "lng": -4.0, "name": "Cantabria", "code": "1109"},
        8: {"lat": 43.3, "lng": -2.5, "name": "País Vasco", "code": "1025"},
        9: {"lat": 39.6, "lng": 3.0, "name": "Islas Baleares", "code": "0149"},
        10: {"lat": 28.1, "lng": -15.4, "name": "Islas Canarias", "code": "C427X"}
    }
    
    if province_id not in province_coordinates:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    
    coords = province_coordinates[province_id]
    
    try:
        weather_data = await weather_manager.get_complete_weather_data(
            lat=coords["lat"],
            lon=coords["lng"],
            province_code=coords["code"]
        )
        
        weather_data["province_id"] = province_id
        weather_data["province_name"] = coords["name"]
        
        return weather_data
        
    except Exception as e:
        print(f"Error fetching province weather: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo datos meteorológicos")

@app.get("/api/weather/alerts")
async def get_weather_alerts():
    """Obtener alertas meteorológicas activas"""
    
    # Simulación de alertas - en producción integrar con AEMET alertas
    alerts = [
        {
            "id": 1,
            "type": "wind",
            "level": "yellow",
            "title": "Aviso por viento",
            "description": "Vientos de hasta 60 km/h en costa mediterránea",
            "provinces": ["Valencia", "Murcia"],
            "start_time": "2025-07-29T14:00:00Z",
            "end_time": "2025-07-29T20:00:00Z",
            "source": "AEMET"
        },
        {
            "id": 2,
            "type": "waves",
            "level": "orange",
            "title": "Aviso por oleaje",
            "description": "Oleaje de hasta 3 metros en costa cantábrica",
            "provinces": ["Asturias", "Cantabria"],
            "start_time": "2025-07-29T12:00:00Z",
            "end_time": "2025-07-30T06:00:00Z",
            "source": "AEMET"
        }
    ]
    
    return {"alerts": alerts, "total": len(alerts)}

@app.get("/api/beaches/batch/weather")
async def get_multiple_beaches_weather(beach_ids: str):
    """Obtener datos meteorológicos de múltiples playas"""
    
    try:
        # Parsear IDs de playas
        ids = [int(id.strip()) for id in beach_ids.split(',') if id.strip()]
        
        if len(ids) > 10:  # Limitar a 10 playas por petición
            raise HTTPException(status_code=400, detail="Máximo 10 playas por petición")
        
        results = []
        
        for beach_id in ids:
            try:
                # Reutilizar la lógica del endpoint individual
                weather_data = await get_beach_weather(beach_id)
                results.append(weather_data)
            except Exception as e:
                results.append({
                    "beach_id": beach_id,
                    "error": f"Error obteniendo datos: {str(e)}"
                })
        
        return {"beaches": results, "total": len(results)}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="IDs de playa inválidos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando petición: {str(e)}")

@app.get("/api/system/status")
async def get_system_status():
    """Obtener estado del sistema y fuentes de datos"""
    
    status = {
        "aemet": {
            "status": "active" if os.getenv('AEMET_API_KEY') else "warning",
            "name": "AEMET (Oficial España)",
            "description": "Agencia Estatal de Meteorología",
            "configured": bool(os.getenv('AEMET_API_KEY')),
            "last_check": datetime.now().isoformat(),
            "data_types": ["Temperatura", "Viento", "Predicción", "Alertas"]
        },
        "openweather": {
            "status": "active" if os.getenv('OPENWEATHER_API_KEY') else "warning",
            "name": "OpenWeatherMap",
            "description": "Fuente alternativa internacional",
            "configured": bool(os.getenv('OPENWEATHER_API_KEY')),
            "last_check": datetime.now().isoformat(),
            "data_types": ["Temperatura", "Viento", "UV", "Humedad"]
        },
        "marine": {
            "status": "simulated",
            "name": "Datos Marítimos",
            "description": "Simulación inteligente por región",
            "configured": True,
            "last_check": datetime.now().isoformat(),
            "data_types": ["Temperatura agua", "Oleaje", "Condiciones mar"]
        }
    }
    
    # Determinar estado general del sistema
    active_sources = sum(1 for source in status.values() if source["status"] == "active")
    total_sources = len(status)
    
    system_health = {
        "overall_status": "healthy" if active_sources >= 1 else "degraded",
        "active_sources": active_sources,
        "total_sources": total_sources,
        "primary_source": "AEMET" if status["aemet"]["status"] == "active" else "Fallback",
        "data_quality": "official" if status["aemet"]["status"] == "active" else "simulated",
        "last_update": datetime.now().isoformat()
    }
    
    return {
        "system": system_health,
        "sources": status
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
