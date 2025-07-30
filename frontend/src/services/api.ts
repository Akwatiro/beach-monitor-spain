import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Province {
  id: number;
  name: string;
  beaches_count: number;
}

export interface Beach {
  id: number;
  name: string;
  province: string;
  municipality: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  description: string;
  services: string[];
  blue_flag: boolean;
  length_km: number;
  width_m: number;
  sand_type: string;
  aemet_station: string;
}

export interface WeatherData {
  beach_id: number;
  timestamp: string;
  temperature: {
    air: number;
    water: number;
    feels_like: number;
  };
  wind: {
    speed: number;
    direction: string;
    gusts: number;
  };
  waves: {
    height: number;
    period: number;
    direction: string;
  };
  visibility: number;
  humidity: number;
  uv_index: number;
  conditions: string;
  pressure: number;
  source?: string;
  coordinates?: {
    lat: number;
    lng: number;
  };
}

// API functions
export const getProvinces = async (): Promise<{ provinces: Province[] }> => {
  const response = await api.get('/provinces');
  return response.data;
};

export const getBeachesByProvince = async (provinceId: number): Promise<{ beaches: Beach[], province_id: number }> => {
  const response = await api.get(`/beaches/${provinceId}`);
  return response.data;
};

export const getBeachWeather = async (beachId: number): Promise<WeatherData> => {
  const response = await api.get(`/beach/${beachId}/weather`);
  return response.data;
};

export default api;
