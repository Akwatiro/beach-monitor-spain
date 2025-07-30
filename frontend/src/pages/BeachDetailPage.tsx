import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Typography, 
  Container,
  Card,
  CardContent,
  Grid,
  Box,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Paper,
  Divider,
  Tooltip
} from '@mui/material';
import { 
  ArrowBack,
  LocationOn, 
  Thermostat, 
  Water, 
  Air,
  Star,
  WbSunny,
  Visibility,
  Opacity,
  Speed,
  BeachAccess,
  Info,
  Wifi,
  LocalParking,
  Restaurant,
  Wc,
  LocalHospital,
  Sports,
  Security
} from '@mui/icons-material';
import { getBeachWeather, getBeachesByProvince, WeatherData, Beach } from '../services/api';

const getServiceIcon = (service: string) => {
  const lowerService = service.toLowerCase();
  if (lowerService.includes('wifi') || lowerService.includes('internet')) return <Wifi fontSize="small" />;
  if (lowerService.includes('parking') || lowerService.includes('aparcamiento')) return <LocalParking fontSize="small" />;
  if (lowerService.includes('restaurant') || lowerService.includes('chiringuito') || lowerService.includes('bar')) return <Restaurant fontSize="small" />;
  if (lowerService.includes('baños') || lowerService.includes('aseos')) return <Wc fontSize="small" />;
  if (lowerService.includes('primeros auxilios') || lowerService.includes('médico')) return <LocalHospital fontSize="small" />;
  if (lowerService.includes('deporte') || lowerService.includes('voleibol') || lowerService.includes('fútbol')) return <Sports fontSize="small" />;
  if (lowerService.includes('socorrista') || lowerService.includes('vigilancia')) return <Security fontSize="small" />;
  return <BeachAccess fontSize="small" />;
};

const BeachDetailPage: React.FC = () => {
  const { beachId } = useParams<{ beachId: string }>();
  const navigate = useNavigate();
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [beachData, setBeachData] = useState<Beach | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!beachId) return;
      
      try {
        setLoading(true);
        
        // Obtener datos meteorológicos
        try {
          const weather = await getBeachWeather(parseInt(beachId));
          setWeatherData(weather);
        } catch (weatherError) {
          console.warn('No se pudieron cargar datos meteorológicos:', weatherError);
        }
        
        // Buscar información de la playa en todas las provincias
        let foundBeach: Beach | null = null;
        for (let provinceId = 1; provinceId <= 10; provinceId++) {
          try {
            const response = await getBeachesByProvince(provinceId);
            foundBeach = response.beaches.find(beach => beach.id === parseInt(beachId)) || null;
            if (foundBeach) break;
          } catch (err) {
            // Continuar buscando en otras provincias
          }
        }
        
        if (foundBeach) {
          setBeachData(foundBeach);
        } else {
          setError('No se encontró información de esta playa');
        }
        
      } catch (err) {
        setError('Error al cargar los datos de la playa');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [beachId]);

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error || !beachData) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 2 }}>
          {error || 'No se pudieron cargar los datos'}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 3 }}>
        <Button 
          startIcon={<ArrowBack />}
          onClick={() => navigate(-1)}
          sx={{ mb: 2 }}
        >
          Volver
        </Button>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold', mr: 2 }}>
            🏖️ {beachData.name}
          </Typography>
          {beachData.blue_flag && (
            <Tooltip title="Bandera Azul - Playa certificada por su calidad ambiental">
              <Chip 
                label="🏆 Bandera Azul" 
                color="primary" 
                sx={{ fontWeight: 'bold' }}
              />
            </Tooltip>
          )}
        </Box>
        
        <Box display="flex" alignItems="center" mb={2}>
          <LocationOn sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h6" color="text.secondary">
            {beachData.municipality}, {beachData.province}
          </Typography>
        </Box>
        
        <Typography variant="body1" sx={{ mb: 2 }}>
          {beachData.description}
        </Typography>
        
        <Box display="flex" alignItems="center" mb={2}>
          <Typography variant="body2" color="text.secondary">
            📍 Coordenadas: {beachData.coordinates.lat.toFixed(4)}°N, {beachData.coordinates.lng.toFixed(4)}°W
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Información de la playa */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📏 Características de la Playa
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">
                      {beachData.length_km}
                    </Typography>
                    <Typography variant="body2">
                      Kilómetros de longitud
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="secondary">
                      {beachData.width_m}
                    </Typography>
                    <Typography variant="body2">
                      Metros de anchura
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
              <Divider sx={{ my: 2 }} />
              <Box textAlign="center">
                <Typography variant="body1" fontWeight="bold">
                  Tipo de arena: {beachData.sand_type}
                </Typography>
                {beachData.aemet_station && (
                  <Typography variant="body2" color="text.secondary">
                    Estación meteorológica: {beachData.aemet_station}
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Servicios */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🏪 Servicios Disponibles
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {beachData.services.map((service, index) => (
                  <Chip
                    key={index}
                    icon={getServiceIcon(service)}
                    label={service}
                    variant="outlined"
                    size="small"
                  />
                ))}
              </Box>
              {beachData.services.length === 0 && (
                <Typography variant="body2" color="text.secondary" textAlign="center">
                  No hay información de servicios disponible
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Datos meteorológicos si están disponibles */}
        {weatherData && (
          <>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    �️ Temperatura Actual
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Box textAlign="center">
                        <Thermostat sx={{ fontSize: 40, color: 'orange', mb: 1 }} />
                        <Typography variant="h4" color="orange">
                          {weatherData.temperature.air}°C
                        </Typography>
                        <Typography variant="body2">
                          Aire
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6}>
                      <Box textAlign="center">
                        <Water sx={{ fontSize: 40, color: 'blue', mb: 1 }} />
                        <Typography variant="h4" color="blue">
                          {weatherData.temperature.water}°C
                        </Typography>
                        <Typography variant="body2">
                          Agua
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                  <Divider sx={{ my: 2 }} />
                  <Box textAlign="center">
                    <Typography variant="body2" color="text.secondary">
                      Sensación térmica: {weatherData.temperature.feels_like}°C
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    💨 Condiciones del Viento
                  </Typography>
                  <Box textAlign="center" mb={2}>
                    <Air sx={{ fontSize: 40, color: 'lightblue', mb: 1 }} />
                    <Typography variant="h4" color="lightblue">
                      {weatherData.wind.speed} km/h
                    </Typography>
                    <Typography variant="body2">
                      Dirección: {weatherData.wind.direction}
                    </Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box textAlign="center">
                    <Typography variant="body2" color="text.secondary">
                      Ráfagas: {weatherData.wind.gusts} km/h
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </>
        )}

        {/* Información adicional */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <Info sx={{ mr: 1, verticalAlign: 'middle' }} />
              Información Adicional
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="body2" paragraph>
                  <strong>Provincia:</strong> {beachData.province}
                </Typography>
                <Typography variant="body2" paragraph>
                  <strong>Municipio:</strong> {beachData.municipality}
                </Typography>
                <Typography variant="body2" paragraph>
                  <strong>Certificación Bandera Azul:</strong> {beachData.blue_flag ? 'Sí' : 'No'}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="body2" paragraph>
                  <strong>Coordenadas:</strong> {beachData.coordinates.lat.toFixed(6)}, {beachData.coordinates.lng.toFixed(6)}
                </Typography>
                {beachData.aemet_station && (
                  <Typography variant="body2" paragraph>
                    <strong>Estación AEMET:</strong> {beachData.aemet_station}
                  </Typography>
                )}
                <Typography variant="body2" paragraph>
                  <strong>Dimensiones:</strong> {beachData.length_km} km × {beachData.width_m} m
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default BeachDetailPage;
