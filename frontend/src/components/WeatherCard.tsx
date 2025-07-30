import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Chip,
  LinearProgress,
  Alert,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  ThermostatOutlined,
  AirOutlined,
  WavesOutlined,
  VisibilityOutlined,
  WbSunnyOutlined,
  OpacityOutlined,
  SpeedOutlined,
  RefreshOutlined
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getBeachWeather } from '../services/api';

interface WeatherCardProps {
  beachId: number;
  beachName?: string;
}

const WeatherCard: React.FC<WeatherCardProps> = ({ beachId, beachName }) => {
  const [lastUpdate, setLastUpdate] = useState<string>('');

  const { 
    data: weatherData, 
    isLoading, 
    error, 
    refetch,
    isRefetching 
  } = useQuery(
    ['beach-weather', beachId],
    () => getBeachWeather(beachId),
    {
      refetchInterval: 5 * 60 * 1000, // Actualizar cada 5 minutos
      onSuccess: () => {
        setLastUpdate(new Date().toLocaleTimeString('es-ES'));
      }
    }
  );

  const getFlagColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'green': return 'success';
      case 'yellow': return 'warning';
      case 'red': return 'error';
      default: return 'default';
    }
  };

  const getUVLevel = (index: number) => {
    if (index <= 2) return { text: 'Bajo', color: 'success' };
    if (index <= 5) return { text: 'Moderado', color: 'warning' };
    if (index <= 7) return { text: 'Alto', color: 'warning' };
    if (index <= 10) return { text: 'Muy Alto', color: 'error' };
    return { text: 'Extremo', color: 'error' };
  };

  if (isLoading) return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {beachName || `Playa ${beachId}`}
        </Typography>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 1 }}>
          Cargando datos meteorológicos...
        </Typography>
      </CardContent>
    </Card>
  );

  if (error) return (
    <Card>
      <CardContent>
        <Alert severity="error">
          Error al cargar datos meteorológicos
        </Alert>
      </CardContent>
    </Card>
  );

  const weather = weatherData;
  const uvLevel = getUVLevel(weather?.uv_index || 0);

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" component="h3">
            {beachName || `Playa ${beachId}`}
          </Typography>
          <Box display="flex" alignItems="center" gap={1}>
            {weather?.source && (
              <Chip 
                label={weather.source} 
                size="small" 
                variant="outlined"
                color="primary"
              />
            )}
            <Tooltip title="Actualizar datos">
              <IconButton 
                size="small" 
                onClick={() => refetch()}
                disabled={isRefetching}
              >
                <RefreshOutlined />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {/* Condiciones principales */}
        <Typography variant="body1" gutterBottom sx={{ fontWeight: 500 }}>
          {weather?.conditions || 'No disponible'}
        </Typography>

        <Grid container spacing={2}>
          {/* Temperatura */}
          <Grid item xs={6} sm={4}>
            <Box display="flex" alignItems="center" mb={1}>
              <ThermostatOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Temperatura
              </Typography>
            </Box>
            <Typography variant="h6">
              {weather?.temperature?.air}°C
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Agua: {weather?.temperature?.water}°C
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Sensación: {weather?.temperature?.feels_like}°C
            </Typography>
          </Grid>

          {/* Viento */}
          <Grid item xs={6} sm={4}>
            <Box display="flex" alignItems="center" mb={1}>
              <AirOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Viento
              </Typography>
            </Box>
            <Typography variant="h6">
              {weather?.wind?.speed} km/h
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {weather?.wind?.direction}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Rachas: {weather?.wind?.gusts} km/h
            </Typography>
          </Grid>

          {/* Oleaje */}
          <Grid item xs={6} sm={4}>
            <Box display="flex" alignItems="center" mb={1}>
              <WavesOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Oleaje
              </Typography>
            </Box>
            <Typography variant="h6">
              {weather?.waves?.height}m
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Periodo: {weather?.waves?.period}s
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Dirección: {weather?.waves?.direction}
            </Typography>
          </Grid>

          {/* Humedad */}
          <Grid item xs={6} sm={4}>
            <Box display="flex" alignItems="center" mb={1}>
              <OpacityOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Humedad
              </Typography>
            </Box>
            <Typography variant="h6">
              {weather?.humidity}%
            </Typography>
          </Grid>

          {/* Visibilidad */}
          <Grid item xs={6} sm={4}>
            <Box display="flex" alignItems="center" mb={1}>
              <VisibilityOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Visibilidad
              </Typography>
            </Box>
            <Typography variant="h6">
              {weather?.visibility} km
            </Typography>
          </Grid>

          {/* Presión */}
          <Grid item xs={6} sm={4}>
            <Box display="flex" alignItems="center" mb={1}>
              <SpeedOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Presión
              </Typography>
            </Box>
            <Typography variant="h6">
              {weather?.pressure} hPa
            </Typography>
          </Grid>

          {/* UV Index */}
          <Grid item xs={12} sm={6}>
            <Box display="flex" alignItems="center" mb={1}>
              <WbSunnyOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2" color="text.secondary">
                Índice UV
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" gap={1}>
              <Typography variant="h6">
                {weather?.uv_index}
              </Typography>
              <Chip 
                label={uvLevel.text} 
                size="small" 
                color={uvLevel.color as any}
              />
            </Box>
          </Grid>
        </Grid>

        {/* Información adicional */}
        <Box mt={2} pt={2} borderTop="1px solid" borderColor="divider">
          <Typography variant="body2" color="text.secondary">
            Última actualización: {lastUpdate || 'Cargando...'}
          </Typography>
          {weather?.timestamp && (
            <Typography variant="body2" color="text.secondary">
              Datos de: {new Date(weather.timestamp).toLocaleString('es-ES')}
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default WeatherCard;
