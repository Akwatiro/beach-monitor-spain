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
    beaches_data = {
        1: [  # Andalucía - Coordenadas reales
            {
                "id": 1,
                "name": "Playa de La Malagueta",
                "province": "Málaga",
                "municipality": "Málaga",
                "coordinates": {"lat": 36.7196, "lng": -4.4214},  # Coordenadas reales
                "description": "Playa urbana emblemática de Málaga, arena oscura, 1.2km de longitud",
                "services": ["Socorrista", "Duchas", "Chiringuitos", "Acceso PMR"],
                "blue_flag": True,
                "length_km": 1.2,
                "width_m": 45,
                "sand_type": "Oscura",
                "aemet_station": "6155A"  # Estación AEMET Málaga
            },
            {
                "id": 2,
                "name": "Playa de Bolonia",
                "province": "Cádiz", 
                "municipality": "Tarifa",
                "coordinates": {"lat": 36.0858, "lng": -5.7708},  # Coordenadas reales
                "description": "Playa virgen con dunas, arena blanca fina, junto a las ruinas de Baelo Claudia",
                "services": ["Socorrista", "Parking", "Restaurantes"],
                "blue_flag": False,
                "length_km": 4.0,
                "width_m": 70,
                "sand_type": "Blanca fina",
                "aemet_station": "5960"  # Estación AEMET Tarifa
            },
            {
                "id": 3,
                "name": "Playa de Marbella (La Fontanilla)",
                "province": "Málaga",
                "municipality": "Marbella", 
                "coordinates": {"lat": 36.5108, "lng": -4.8850},  # Coordenadas reales
                "description": "Playa céntrica de Marbella, arena dorada, ambiente cosmopolita",
                "services": ["Socorrista", "Duchas", "Beach clubs", "Alquiler hamacas"],
                "blue_flag": True,
                "length_km": 0.8,
                "width_m": 25,
                "sand_type": "Dorada",
                "aemet_station": "6155A"
            },
            {
                "id": 4,
                "name": "Playa de los Lances Norte",
                "province": "Cádiz",
                "municipality": "Tarifa",
                "coordinates": {"lat": 36.0138, "lng": -5.6066},  # Coordenadas reales  
                "description": "Playa ideal para windsurf y kitesurf, vientos constantes",
                "services": ["Socorrista", "Escuelas de windsurf", "Parking"],
                "blue_flag": False,
                "length_km": 7.0,
                "width_m": 150,
                "sand_type": "Blanca gruesa",
                "aemet_station": "5960"
            },
            {
                "id": 5,
                "name": "Playa de la Barrosa",
                "province": "Cádiz",
                "municipality": "Chiclana de la Frontera",
                "coordinates": {"lat": 36.3275, "lng": -6.1953},  # Coordenadas reales
                "description": "8km de arena blanca fina, una de las mejores playas de Cádiz",
                "services": ["Socorrista", "Chiringuitos", "Parking", "Acceso PMR"],
                "blue_flag": True,
                "length_km": 8.0,
                "width_m": 50,
                "sand_type": "Blanca fina",
                "aemet_station": "5960"
            }
        ],
        2: [  # Valencia - Coordenadas y datos reales
            {
                "id": 11,
                "name": "Playa de la Malvarrosa",
                "province": "Valencia",
                "municipality": "Valencia",
                "coordinates": {"lat": 39.4817, "lng": -0.3250},  # Coordenadas reales
                "description": "Playa urbana histórica de Valencia, arena fina dorada, paseo marítimo",
                "services": ["Socorrista", "Duchas", "Volleyball", "Alquiler bicicletas"],
                "blue_flag": True,
                "length_km": 1.0,
                "width_m": 135,
                "sand_type": "Dorada fina",
                "aemet_station": "8414A"  # Estación AEMET Valencia
            },
            {
                "id": 12,
                "name": "Playa de Levante (Benidorm)",
                "province": "Alicante",
                "municipality": "Benidorm",
                "coordinates": {"lat": 38.5382, "lng": -0.1316},  # Coordenadas reales
                "description": "Playa urbana icónica, arena fina, ambiente animado, rascacielos",
                "services": ["Socorrista", "Duchas", "Chiringuitos", "Deportes acuáticos"],
                "blue_flag": True,
                "length_km": 2.0,
                "width_m": 40,
                "sand_type": "Dorada fina",
                "aemet_station": "8025"  # Estación AEMET Alicante
            },
            {
                "id": 13,
                "name": "Playa de las Arenas (Denia)",
                "province": "Alicante", 
                "municipality": "Denia",
                "coordinates": {"lat": 38.8408, "lng": 0.1042},  # Coordenadas reales
                "description": "Playa de arena fina en el puerto de Denia, aguas tranquilas",
                "services": ["Socorrista", "Parking", "Restaurantes", "Puerto deportivo"],
                "blue_flag": True,
                "length_km": 3.0,
                "width_m": 60,
                "sand_type": "Dorada fina",
                "aemet_station": "8025"
            },
            {
                "id": 14,
                "name": "Playa de Gandia",
                "province": "Valencia",
                "municipality": "Gandia",
                "coordinates": {"lat": 38.9667, "lng": -0.1667},  # Coordenadas reales
                "description": "Extensa playa de arena fina, ideal para familias, paseo marítimo",
                "services": ["Socorrista", "Duchas", "Acceso PMR", "Deportes de playa"],
                "blue_flag": True,
                "length_km": 7.0,
                "width_m": 80,
                "sand_type": "Dorada fina",
                "aemet_station": "8414A"
            }
        ],
        3: [  # Cataluña - Coordenadas y datos reales
            {
                "id": 21,
                "name": "Playa de la Barceloneta",
                "province": "Barcelona",
                "municipality": "Barcelona",
                "coordinates": {"lat": 41.3806, "lng": 2.1900},  # Coordenadas reales
                "description": "Playa urbana histórica de Barcelona, arena dorada, barrio marinero",
                "services": ["Socorrista", "Duchas", "Volleyball", "Chiringuitos"],
                "blue_flag": True,
                "length_km": 0.5,
                "width_m": 89,
                "sand_type": "Dorada",
                "aemet_station": "0076"  # Estación AEMET Barcelona
            },
            {
                "id": 22,
                "name": "Playa de Sitges",
                "province": "Barcelona",
                "municipality": "Sitges",
                "coordinates": {"lat": 41.2370, "lng": 1.8058},  # Coordenadas reales
                "description": "Playa bohemia y cosmopolita, arena dorada, ambiente cultural",
                "services": ["Socorrista", "Duchas", "Beach bars", "Eventos culturales"],
                "blue_flag": True,
                "length_km": 2.5,
                "width_m": 50,
                "sand_type": "Dorada fina",
                "aemet_station": "0076"
            },
            {
                "id": 23,
                "name": "Playa de Lloret de Mar",
                "province": "Girona",
                "municipality": "Lloret de Mar",
                "coordinates": {"lat": 41.6971, "lng": 2.8456},  # Coordenadas reales
                "description": "Playa principal de la Costa Brava, arena gruesa, ambiente juvenil",
                "services": ["Socorrista", "Deportes acuáticos", "Discotecas", "Hoteles"],
                "blue_flag": True,
                "length_km": 1.5,
                "width_m": 45,
                "sand_type": "Gruesa",
                "aemet_station": "0367"  # Estación AEMET Girona
            },
            {
                "id": 24,
                "name": "Cala Montjoi (Roses)",
                "province": "Girona",
                "municipality": "Roses",
                "coordinates": {"lat": 42.2667, "lng": 3.2333},  # Coordenadas reales
                "description": "Cala virgen en el Cabo de Creus, aguas cristalinas, antiguo El Bulli",
                "services": ["Parking", "Senderos naturales"],
                "blue_flag": False,
                "length_km": 0.2,
                "width_m": 15,
                "sand_type": "Grava y arena",
                "aemet_station": "0367"
            }
        ],
        4: [  # Galicia - Coordenadas y datos reales
            {
                "id": 31,
                "name": "Playa de Riazor",
                "province": "A Coruña",
                "municipality": "A Coruña",
                "coordinates": {"lat": 43.3713, "lng": -8.4079},  # Coordenadas reales
                "description": "Playa urbana emblemática de A Coruña, arena fina, paseo marítimo",
                "services": ["Socorrista", "Duchas", "Deportes", "Acceso PMR"],
                "blue_flag": True,
                "length_km": 1.4,
                "width_m": 200,
                "sand_type": "Fina blanca",
                "aemet_station": "1387"  # Estación AEMET A Coruña
            },
            {
                "id": 32,
                "name": "Playa de Rodas (Islas Cíes)",
                "province": "Pontevedra",
                "municipality": "Vigo",
                "coordinates": {"lat": 42.2167, "lng": -8.9000},  # Coordenadas reales
                "description": "Playa paradisíaca en Parque Nacional, arena blanca, aguas turquesas",
                "services": ["Información parque", "Rutas ecológicas", "Ferry"],
                "blue_flag": False,
                "length_km": 1.2,
                "width_m": 50,
                "sand_type": "Blanca fina",
                "aemet_station": "1484D"  # Estación AEMET Vigo
            },
            {
                "id": 33,
                "name": "Playa de Samil",
                "province": "Pontevedra",
                "municipality": "Vigo",
                "coordinates": {"lat": 42.2069, "lng": -8.7331},  # Coordenadas reales
                "description": "Playa familiar de Vigo, arena fina, vistas a las Islas Cíes",
                "services": ["Socorrista", "Parking", "Restaurantes", "Parque infantil"],
                "blue_flag": True,
                "length_km": 2.5,
                "width_m": 40,
                "sand_type": "Fina dorada",
                "aemet_station": "1484D"
            },
            {
                "id": 34,
                "name": "Playa de las Catedrales",
                "province": "Lugo",
                "municipality": "Ribadeo",
                "coordinates": {"lat": 43.5547, "lng": -7.1608},  # Coordenadas reales
                "description": "Monumento natural, arcos y cuevas de piedra, acceso con marea baja",
                "services": ["Parking", "Información turística", "Reserva obligatoria"],
                "blue_flag": False,
                "length_km": 1.5,
                "width_m": 50,
                "sand_type": "Fina con rocas",
                "aemet_station": "1505"  # Estación AEMET Lugo
            }
        ],
        5: [  # Murcia - Coordenadas y datos reales
            {
                "id": 41,
                "name": "Playa de la Manga del Mar Menor",
                "province": "Murcia",
                "municipality": "Cartagena",
                "coordinates": {"lat": 37.7167, "lng": -0.7333},  # Coordenadas reales
                "description": "Lengua de arena entre dos mares, aguas cálidas del Mar Menor",
                "services": ["Socorrista", "Deportes náuticos", "Thalasso", "Hoteles"],
                "blue_flag": True,
                "length_km": 21.0,
                "width_m": 300,
                "sand_type": "Fina dorada",
                "aemet_station": "7178I"  # Estación AEMET Murcia
            },
            {
                "id": 42,
                "name": "Playa de Mazarrón",
                "province": "Murcia",
                "municipality": "Mazarrón",
                "coordinates": {"lat": 37.5964, "lng": -1.3144},  # Coordenadas reales
                "description": "Playa de arena dorada, aguas cristalinas, ambiente tranquilo",
                "services": ["Socorrista", "Chiringuitos", "Parking", "Acceso PMR"],
                "blue_flag": True,
                "length_km": 2.5,
                "width_m": 40,
                "sand_type": "Dorada fina",
                "aemet_station": "7178I"
            },
            {
                "id": 43,
                "name": "Cala Cortina",
                "province": "Murcia",
                "municipality": "Cartagena",
                "coordinates": {"lat": 37.5833, "lng": -0.9667},  # Coordenadas reales
                "description": "Pequeña cala protegida, ideal para familias, aguas tranquilas",
                "services": ["Socorrista", "Bar-restaurante", "Parking"],
                "blue_flag": True,
                "length_km": 0.1,
                "width_m": 25,
                "sand_type": "Fina",
                "aemet_station": "7178I"
            }
        ],
        9: [  # Islas Baleares - Coordenadas y datos reales
            {
                "id": 91,
                "name": "Playa de Es Trenc",
                "province": "Mallorca",
                "municipality": "Campos",
                "coordinates": {"lat": 39.3561, "lng": 3.0206},  # Coordenadas reales
                "description": "Playa virgen de arena blanca, dunas naturales, aguas turquesas",
                "services": ["Parking natural", "Chiringuitos ecológicos"],
                "blue_flag": False,
                "length_km": 3.0,
                "width_m": 25,
                "sand_type": "Blanca fina",
                "aemet_station": "B278"  # Estación AEMET Palma
            },
            {
                "id": 92,
                "name": "Playa de Ses Illetes",
                "province": "Formentera",
                "municipality": "Formentera",
                "coordinates": {"lat": 38.7231, "lng": 1.4636},  # Coordenadas reales
                "description": "Playa paradisíaca, arena blanca, aguas cristalinas turquesas",
                "services": ["Chiringuitos", "Tumbonas", "Sombrillas"],
                "blue_flag": False,
                "length_km": 0.5,
                "width_m": 20,
                "sand_type": "Blanca fina",
                "aemet_station": "B964"  # Estación AEMET Formentera
            },
            {
                "id": 93,
                "name": "Cala Macarella",
                "province": "Menorca",
                "municipality": "Ciutadella",
                "coordinates": {"lat": 39.9333, "lng": 3.9333},  # Coordenadas reales
                "description": "Cala virgen con pinares, arena blanca, aguas turquesas cristalinas",
                "services": ["Parking", "Senderos naturales"],
                "blue_flag": False,
                "length_km": 0.1,
                "width_m": 15,
                "sand_type": "Blanca fina",
                "aemet_station": "B893"  # Estación AEMET Menorca
            },
            {
                "id": 94,
                "name": "Playa de Alcudia",
                "province": "Mallorca", 
                "municipality": "Alcudia",
                "coordinates": {"lat": 39.8500, "lng": 3.1000},  # Coordenadas reales
                "description": "Extensa playa familiar, arena fina, aguas poco profundas",
                "services": ["Socorrista", "Deportes acuáticos", "Hoteles", "Restaurantes"],
                "blue_flag": True,
                "length_km": 7.0,
                "width_m": 50,
                "sand_type": "Fina blanca",
                "aemet_station": "B278"
            }
        ],
        6: [  # Asturias - Coordenadas y datos reales
            {
                "id": 61,
                "name": "Playa de San Lorenzo",
                "province": "Asturias",
                "municipality": "Gijón",
                "coordinates": {"lat": 43.5319, "lng": -5.6672},  # Coordenadas reales
                "description": "Playa urbana de Gijón, arena fina dorada, 1.5km de longitud",
                "services": ["Socorrista", "Paseo marítimo", "Duchas", "Acceso PMR"],
                "blue_flag": True,
                "length_km": 1.5,
                "width_m": 100,
                "sand_type": "Dorada fina",
                "aemet_station": "1249I"  # Estación AEMET Gijón
            },
            {
                "id": 62,
                "name": "Playa de Gulpiyuri",
                "province": "Asturias",
                "municipality": "Llanes",
                "coordinates": {"lat": 43.4372, "lng": -4.8503},  # Coordenadas reales
                "description": "Playa interior única, rodeada de prados, Monumento Natural",
                "services": ["Parking", "Senderos", "Información turística"],
                "blue_flag": False,
                "length_km": 0.04,
                "width_m": 10,
                "sand_type": "Fina blanca",
                "aemet_station": "1249I"
            },
            {
                "id": 63,
                "name": "Playa de Rodiles",
                "province": "Asturias",
                "municipality": "Villaviciosa",
                "coordinates": {"lat": 43.5167, "lng": -5.3833},  # Coordenadas reales
                "description": "Playa salvaje ideal para surf, dunas naturales, reserva natural",
                "services": ["Parking", "Escuela surf", "Rutas naturales"],
                "blue_flag": False,
                "length_km": 3.0,
                "width_m": 150,
                "sand_type": "Fina blanca",
                "aemet_station": "1249I"
            }
        ],
        7: [  # Cantabria - Coordenadas y datos reales
            {
                "id": 71,
                "name": "Playa del Sardinero",
                "province": "Cantabria",
                "municipality": "Santander",
                "coordinates": {"lat": 43.4647, "lng": -3.8044},  # Coordenadas reales
                "description": "Playa urbana histórica de Santander, arena fina, ambiente elegante",
                "services": ["Socorrista", "Casino", "Hoteles", "Paseo marítimo"],
                "blue_flag": True,
                "length_km": 1.2,
                "width_m": 50,
                "sand_type": "Fina dorada",
                "aemet_station": "1109"  # Estación AEMET Santander
            },
            {
                "id": 72,
                "name": "Playa de los Locos",
                "province": "Cantabria",
                "municipality": "Suances",
                "coordinates": {"lat": 43.4331, "lng": -4.0331},  # Coordenadas reales
                "description": "Playa de surf famosa, olas consistentes, ambiente surfero",
                "services": ["Escuelas de surf", "Parking", "Chiringuitos"],
                "blue_flag": False,
                "length_km": 0.5,
                "width_m": 40,
                "sand_type": "Dorada",
                "aemet_station": "1109"
            }
        ],
        8: [  # País Vasco - Coordenadas y datos reales
            {
                "id": 81,
                "name": "Playa de la Concha",
                "province": "Guipúzcoa",
                "municipality": "San Sebastián",
                "coordinates": {"lat": 43.3198, "lng": -1.9894},  # Coordenadas reales
                "description": "Una de las playas urbanas más bellas del mundo, bahía perfecta",
                "services": ["Socorrista", "Paseo marítimo", "Hoteles", "Restaurantes"],
                "blue_flag": True,
                "length_km": 1.4,
                "width_m": 40,
                "sand_type": "Fina blanca",
                "aemet_station": "1025"  # Estación AEMET San Sebastián
            },
            {
                "id": 82,
                "name": "Playa de Sopelana",
                "province": "Vizcaya",
                "municipality": "Sopelana",
                "coordinates": {"lat": 43.3833, "lng": -2.9833},  # Coordenadas reales
                "description": "Playa de surf en acantilados, olas potentes, ambiente joven",
                "services": ["Escuelas de surf", "Parking", "Metro Bilbao"],
                "blue_flag": False,
                "length_km": 0.8,
                "width_m": 60,
                "sand_type": "Dorada gruesa",
                "aemet_station": "1025"
            },
            {
                "id": 83,
                "name": "Playa de Zarautz",
                "province": "Guipúzcoa", 
                "municipality": "Zarautz",
                "coordinates": {"lat": 43.2833, "lng": -2.1667},  # Coordenadas reales
                "description": "Playa de surf de 2.5km, capital europea del surf",
                "services": ["Escuelas de surf", "Campeonatos", "Restaurantes", "Hoteles"],
                "blue_flag": True,
                "length_km": 2.5,
                "width_m": 100,
                "sand_type": "Fina dorada",
                "aemet_station": "1025"
            }
        ],
        10: [  # Islas Canarias - Coordenadas y datos reales
            {
                "id": 101,
                "name": "Playa de las Canteras",
                "province": "Las Palmas",
                "municipality": "Las Palmas de Gran Canaria",
                "coordinates": {"lat": 28.1393, "lng": -15.4438},  # Coordenadas reales
                "description": "Playa urbana de arena dorada, La Barra natural protege del oleaje",
                "services": ["Socorrista", "Paseo marítimo", "Restaurantes", "Deportes"],
                "blue_flag": True,
                "length_km": 3.2,
                "width_m": 60,
                "sand_type": "Dorada fina",
                "aemet_station": "C427X"  # Estación AEMET Las Palmas
            },
            {
                "id": 102,
                "name": "Playa del Duque",
                "province": "Tenerife",
                "municipality": "Adeje",
                "coordinates": {"lat": 28.0916, "lng": -16.7446},  # Coordenadas reales
                "description": "Playa de lujo con arena dorada, Costa Adeje, hoteles 5 estrellas",
                "services": ["Socorrista", "Beach clubs", "Restaurantes gourmet", "Spa"],
                "blue_flag": True,
                "length_km": 0.7,
                "width_m": 50,
                "sand_type": "Dorada importada",
                "aemet_station": "C447A"  # Estación AEMET Tenerife Sur
            },
            {
                "id": 103,
                "name": "Playa de Papagayo",
                "province": "Lanzarote",
                "municipality": "Yaiza",
                "coordinates": {"lat": 28.8667, "lng": -13.8000},  # Coordenadas reales
                "description": "Calas vírgenes de arena blanca, acantilados volcánicos, aguas cristalinas",
                "services": ["Parking", "Senderos", "Protección natural"],
                "blue_flag": False,
                "length_km": 0.4,
                "width_m": 30,
                "sand_type": "Blanca fina",
                "aemet_station": "C329I"  # Estación AEMET Lanzarote
            },
            {
                "id": 104,
                "name": "Playa de Sotavento",
                "province": "Fuerteventura",
                "municipality": "Pájara",
                "coordinates": {"lat": 28.0575, "lng": -14.3531},  # Coordenadas reales
                "description": "Playa de 9km, vientos constantes, ideal windsurf y kitesurf",
                "services": ["Escuelas de windsurf", "Parking", "Hoteles"],
                "blue_flag": False,
                "length_km": 9.0,
                "width_m": 100,
                "sand_type": "Blanca fina",
                "aemet_station": "C430E"  # Estación AEMET Fuerteventura
            },
            {
                "id": 105,
                "name": "Playa de los Ingleses",
                "province": "La Palma",
                "municipality": "Santa Cruz de La Palma",
                "coordinates": {"lat": 28.7833, "lng": -17.7333},  # Coordenadas reales
                "description": "Playa de arena negra volcánica, entorno natural protegido",
                "services": ["Acceso natural", "Parking", "Senderos"],
                "blue_flag": False,
                "length_km": 1.0,
                "width_m": 25,
                "sand_type": "Negra volcánica",
                "aemet_station": "C311X"  # Estación AEMET La Palma
            }
        ]
    }
    
    beaches = beaches_data.get(province_id, [])
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
