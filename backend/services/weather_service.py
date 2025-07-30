"""
Weather services for Beach Monitor Spain
Integrates with AEMET and OpenWeatherMap APIs for real-time weather data
"""

import os
import requests
import asyncio
import aiohttp
from typing import Dict, Optional, List
from datetime import datetime
import json
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class WeatherData:
    temperature_air: float
    temperature_water: Optional[float]
    humidity: int
    wind_speed: float
    wind_direction: str
    wave_height: Optional[float]
    visibility: float
    uv_index: int
    conditions: str
    pressure: float
    timestamp: datetime

class AEMETService:
    """
    Servicio para integrar con la API de AEMET (Agencia Estatal de Meteorología)
    """
    
    def __init__(self):
        self.api_key = os.getenv('AEMET_API_KEY')
        self.base_url = 'https://opendata.aemet.es/opendata/api'
        
    async def get_coastal_weather(self, province_code: str) -> Optional[WeatherData]:
        """
        Obtiene datos meteorológicos costeros de AEMET
        """
        if not self.api_key:
            print("Warning: AEMET API key not configured")
            return None
            
        try:
            async with aiohttp.ClientSession() as session:
                # Usamos el endpoint de observación convencional más reciente
                url = f"{self.base_url}/observacion/convencional/datos/estacion/{province_code}"
                headers = {'api_key': self.api_key}
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'datos' in data:
                            # Obtenemos los datos reales con content-type específico
                            datos_url = data['datos']
                            async with session.get(datos_url) as data_response:
                                if data_response.status == 200:
                                    # AEMET puede devolver text/plain, manejamos ambos casos
                                    try:
                                        weather_data = await data_response.json()
                                        return self._parse_aemet_data(weather_data)
                                    except:
                                        # Si no es JSON válido, usamos texto
                                        text_data = await data_response.text()
                                        try:
                                            import json
                                            weather_data = json.loads(text_data)
                                            return self._parse_aemet_data(weather_data)
                                        except:
                                            print(f"AEMET data parsing error for station {province_code}")
                                            return None
                        else:
                            print(f"AEMET API response missing 'datos' field")
                            return None
                    elif response.status == 404:
                        print(f"AEMET station {province_code} not found, trying alternative")
                        # Intentar con estación alternativa o datos generales
                        return await self._get_alternative_aemet_data(session)
                    else:
                        print(f"AEMET API error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"Error fetching AEMET data: {e}")
            return None
    
    async def _get_alternative_aemet_data(self, session: aiohttp.ClientSession) -> Optional[WeatherData]:
        """
        Obtiene datos meteorológicos generales cuando la estación específica no está disponible
        """
        try:
            # Usar el endpoint de predicción por municipios como alternativa
            url = f"{self.base_url}/prediccion/especifica/municipio/diaria/29067"  # Málaga como ejemplo
            headers = {'api_key': self.api_key}
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'datos' in data:
                        async with session.get(data['datos']) as data_response:
                            if data_response.status == 200:
                                try:
                                    pred_data = await data_response.json()
                                    return self._parse_aemet_prediction_data(pred_data)
                                except:
                                    text_data = await data_response.text()
                                    import json
                                    pred_data = json.loads(text_data)
                                    return self._parse_aemet_prediction_data(pred_data)
            return None
        except Exception as e:
            print(f"Error fetching alternative AEMET data: {e}")
            return None
    
    def _parse_aemet_prediction_data(self, data: List[Dict]) -> Optional[WeatherData]:
        """
        Parsea datos de predicción de AEMET
        """
        if not data or not isinstance(data, list) or len(data) == 0:
            return None
            
        prediction = data[0]
        prediccion = prediction.get('prediccion', {})
        dia = prediccion.get('dia', [{}])
        if dia:
            today = dia[0]
            
            # Extraer temperatura (puede venir en diferentes formatos)
            temp_max = 25  # valor por defecto
            temp_min = 18
            
            if 'temperatura' in today:
                temp_data = today['temperatura']
                if 'maxima' in temp_data:
                    temp_max = int(temp_data['maxima']) if temp_data['maxima'] != '' else 25
                if 'minima' in temp_data:
                    temp_min = int(temp_data['minima']) if temp_data['minima'] != '' else 18
            
            temp_actual = (temp_max + temp_min) / 2
            
            # Viento
            wind_speed = 10  # por defecto
            wind_dir = 'SW'
            
            if 'viento' in today:
                viento = today['viento']
                if isinstance(viento, list) and len(viento) > 0:
                    viento_data = viento[0]
                    if 'velocidad' in viento_data:
                        wind_speed = int(viento_data['velocidad'][0]) if viento_data['velocidad'] else 10
                    if 'direccion' in viento_data:
                        wind_dir = viento_data['direccion'][0] if viento_data['direccion'] else 'SW'
            
            return WeatherData(
                temperature_air=temp_actual,
                temperature_water=None,
                humidity=65,  # AEMET predicción no incluye humedad específica
                wind_speed=wind_speed,
                wind_direction=wind_dir,
                wave_height=None,
                visibility=10,
                uv_index=0,
                conditions=self._get_sky_description(today.get('estadoCielo', [])),
                pressure=1013,  # No disponible en predicción
                timestamp=datetime.now()
            )
        
        return None
    
    def _get_sky_description(self, estado_cielo) -> str:
        """
        Convierte códigos de estado del cielo de AEMET a descripción
        """
        if not estado_cielo or not isinstance(estado_cielo, list):
            return "Despejado"
            
        # Tomar el primer estado del día
        if len(estado_cielo) > 0 and 'descripcion' in estado_cielo[0]:
            return estado_cielo[0]['descripcion']
        
        return "Despejado"
    
    def _parse_aemet_data(self, data: List[Dict]) -> Optional[WeatherData]:
        """
        Parsea los datos de respuesta de AEMET
        """
        if not data:
            return None
            
        latest = data[-1]  # Datos más recientes
        
        return WeatherData(
            temperature_air=float(latest.get('ta', 0)),
            temperature_water=None,  # AEMET no proporciona temp del agua
            humidity=int(latest.get('hr', 0)),
            wind_speed=float(latest.get('vv', 0)) * 3.6,  # m/s a km/h
            wind_direction=latest.get('dv', 'N'),
            wave_height=None,  # Requiere datos marítimos específicos
            visibility=float(latest.get('vis', 0)),
            uv_index=0,  # No disponible en datos básicos
            conditions=self._translate_weather_state(latest.get('prec', '')),
            pressure=float(latest.get('pres', 0)),
            timestamp=datetime.now()
        )
    
    def _translate_weather_state(self, state: str) -> str:
        """
        Traduce códigos de estado meteorológico de AEMET
        """
        translations = {
            '': 'Despejado',
            'Ip': 'Lluvia débil',
            'L': 'Lluvia',
            'Ll': 'Lluvia fuerte',
            'N': 'Nieve',
            'T': 'Tormenta'
        }
        return translations.get(state, 'Despejado')

class OpenWeatherMapService:
    """
    Servicio para integrar con OpenWeatherMap API como alternativa
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        
    async def get_weather_by_coordinates(self, lat: float, lon: float) -> Optional[WeatherData]:
        """
        Obtiene datos meteorológicos por coordenadas
        """
        if not self.api_key:
            print("Warning: OpenWeatherMap API key not configured")
            return None
            
        try:
            async with aiohttp.ClientSession() as session:
                # Datos actuales
                current_url = f"{self.base_url}/weather"
                params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': self.api_key,
                    'units': 'metric',
                    'lang': 'es'
                }
                
                async with session.get(current_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # También obtenemos datos UV
                        uv_data = await self._get_uv_index(session, lat, lon)
                        
                        return self._parse_openweather_data(data, uv_data)
                    else:
                        print(f"OpenWeatherMap API error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"Error fetching OpenWeatherMap data: {e}")
            return None
    
    async def _get_uv_index(self, session: aiohttp.ClientSession, lat: float, lon: float) -> Optional[Dict]:
        """
        Obtiene índice UV
        """
        try:
            uv_url = f"{self.base_url}/uvi"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            async with session.get(uv_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except:
            return None
    
    def _parse_openweather_data(self, data: Dict, uv_data: Optional[Dict] = None) -> WeatherData:
        """
        Parsea los datos de respuesta de OpenWeatherMap
        """
        main = data.get('main', {})
        wind = data.get('wind', {})
        weather = data.get('weather', [{}])[0]
        
        # Convertir dirección del viento de grados a cardinal
        wind_direction = self._degrees_to_cardinal(wind.get('deg', 0))
        
        return WeatherData(
            temperature_air=main.get('temp', 0),
            temperature_water=None,  # OpenWeatherMap no tiene temp del agua
            humidity=main.get('humidity', 0),
            wind_speed=wind.get('speed', 0) * 3.6,  # m/s a km/h
            wind_direction=wind_direction,
            wave_height=None,  # Requiere datos marítimos específicos
            visibility=data.get('visibility', 0) / 1000,  # metros a km
            uv_index=int(uv_data.get('value', 0)) if uv_data else 0,
            conditions=weather.get('description', 'Despejado'),
            pressure=main.get('pressure', 0),
            timestamp=datetime.now()
        )
    
    def _degrees_to_cardinal(self, degrees: float) -> str:
        """
        Convierte grados a dirección cardinal
        """
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]

class MarineWeatherService:
    """
    Servicio especializado para datos marítimos (oleaje, temperatura del agua)
    """
    
    def __init__(self):
        self.marine_api_key = os.getenv('MARINE_API_KEY')
        # Puente Navegante español para datos marítimos
        self.base_url = 'https://api.puertos.es/v1'
        
    async def get_sea_conditions(self, lat: float, lon: float) -> Dict:
        """
        Obtiene condiciones del mar (oleaje, temperatura del agua)
        """
        try:
            # Simulamos datos realistas basados en coordenadas españolas
            return self._simulate_sea_conditions(lat, lon)
        except Exception as e:
            print(f"Error fetching marine data: {e}")
            return self._simulate_sea_conditions(lat, lon)
    
    def _simulate_sea_conditions(self, lat: float, lon: float) -> Dict:
        """
        Simula condiciones del mar basadas en la ubicación
        Para demo - reemplazar con API real
        """
        import random
        
        # Diferentes condiciones según región
        if lat > 43:  # Costa norte (Cantábrico)
            water_temp = random.uniform(15, 19)
            wave_height = random.uniform(0.8, 2.5)
        elif lat < 36:  # Sur (Andalucía)
            water_temp = random.uniform(19, 24)
            wave_height = random.uniform(0.3, 1.2)
        else:  # Mediterráneo
            water_temp = random.uniform(18, 26)
            wave_height = random.uniform(0.2, 1.0)
            
        return {
            'water_temperature': round(water_temp, 1),
            'wave_height': round(wave_height, 1),
            'wave_period': random.randint(4, 8),
            'wave_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        }

class WeatherServiceManager:
    """
    Gestor principal que coordina todos los servicios meteorológicos
    """
    
    def __init__(self):
        self.aemet = AEMETService()
        self.openweather = OpenWeatherMapService()
        self.marine = MarineWeatherService()
        
    async def get_complete_weather_data(self, lat: float, lon: float, province_code: str = None) -> Dict:
        """
        Obtiene datos meteorológicos completos combinando múltiples fuentes
        """
        try:
            # Intentar AEMET primero (fuente oficial española)
            weather_data = None
            if province_code:
                weather_data = await self.aemet.get_coastal_weather(province_code)
            
            # Si AEMET no está disponible, usar OpenWeatherMap
            if not weather_data:
                weather_data = await self.openweather.get_weather_by_coordinates(lat, lon)
            
            # Obtener datos marítimos
            sea_data = await self.marine.get_sea_conditions(lat, lon)
            
            # Combinar todos los datos
            if weather_data:
                return {
                    'temperature': {
                        'air': weather_data.temperature_air,
                        'water': sea_data.get('water_temperature', 20),
                        'feels_like': weather_data.temperature_air + 2  # Aproximación
                    },
                    'wind': {
                        'speed': weather_data.wind_speed,
                        'direction': weather_data.wind_direction,
                        'gusts': weather_data.wind_speed * 1.3  # Aproximación
                    },
                    'waves': {
                        'height': sea_data.get('wave_height', 0.5),
                        'period': sea_data.get('wave_period', 6),
                        'direction': sea_data.get('wave_direction', 'W')
                    },
                    'conditions': weather_data.conditions,
                    'humidity': weather_data.humidity,
                    'pressure': weather_data.pressure,
                    'visibility': weather_data.visibility,
                    'uv_index': weather_data.uv_index,
                    'timestamp': weather_data.timestamp.isoformat(),
                    'source': 'AEMET' if province_code else 'OpenWeatherMap'
                }
            else:
                # Datos de fallback
                return self._get_fallback_data(sea_data)
                
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return self._get_fallback_data({})
    
    def _get_fallback_data(self, sea_data: Dict) -> Dict:
        """
        Datos de respaldo cuando las APIs no están disponibles
        """
        return {
            'temperature': {
                'air': 22,
                'water': sea_data.get('water_temperature', 20),
                'feels_like': 24
            },
            'wind': {
                'speed': 15,
                'direction': 'SW',
                'gusts': 20
            },
            'waves': {
                'height': sea_data.get('wave_height', 0.8),
                'period': sea_data.get('wave_period', 6),
                'direction': sea_data.get('wave_direction', 'W')
            },
            'conditions': 'Datos no disponibles',
            'humidity': 65,
            'pressure': 1013,
            'visibility': 10,
            'uv_index': 6,
            'timestamp': datetime.now().isoformat(),
            'source': 'Fallback'
        }
