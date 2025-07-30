import React from 'react';
import { 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Box,
  Chip,
  Button,
  Paper,
  Divider
} from '@mui/material';
import { 
  LocationOnOutlined, 
  ThermostatOutlined,
  WavesOutlined,
  AirOutlined,
  WarningOutlined
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getProvinces } from '../services/api';
import WeatherCard from '../components/WeatherCard';
import WeatherAlerts from '../components/WeatherAlerts';
import SystemStatus from '../components/SystemStatus';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  
  const { data: provincesData, isLoading, error } = useQuery(
    'provinces',
    getProvinces
  );

  if (isLoading) return <Typography>Cargando provincias...</Typography>;
  if (error) return <Typography>Error al cargar los datos</Typography>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        Monitor de Playas de España
      </Typography>
      
      {/* Estado del sistema */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12}>
          <SystemStatus />
        </Grid>
      </Grid>

      {/* Alertas meteorológicas */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12}>
          <WeatherAlerts />
        </Grid>
      </Grid>

      {/* Ejemplo de datos meteorológicos en tiempo real */}
      <Typography variant="h5" gutterBottom sx={{ mb: 2 }}>
        Condiciones Actuales - Playas Destacadas
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <WeatherCard beachId={1} beachName="Playa de La Malagueta (Málaga)" />
        </Grid>
        <Grid item xs={12} md={6}>
          <WeatherCard beachId={2} beachName="Playa de Bolonia (Cádiz)" />
        </Grid>
      </Grid>

      <Divider sx={{ my: 4 }} />
      
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        Selecciona una provincia para ver todas sus playas:
      </Typography>

      <Grid container spacing={3}>
        {provincesData?.provinces.map((province: any) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={province.id}>
            <Card 
              sx={{ 
                height: '100%',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                  boxShadow: 3
                }
              }}
              onClick={() => navigate(`/provincia/${province.id}`)}
            >
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <LocationOnOutlined color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6" component="h2">
                    {province.name}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {province.beaches_count} playas monitoreadas
                </Typography>
                
                <Box mt={2}>
                  <Chip 
                    label="Estado: Actualizado" 
                    color="success" 
                    size="small" 
                    sx={{ mb: 1 }}
                  />
                </Box>
                
                <Button 
                  variant="outlined" 
                  size="small" 
                  fullWidth 
                  sx={{ mt: 2 }}
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/provincia/${province.id}`);
                  }}
                >
                  Ver Playas
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper elevation={1} sx={{ mt: 6, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          <Box display="flex" alignItems="center">
            <WarningOutlined color="primary" sx={{ mr: 1 }} />
            Información en Tiempo Real
          </Box>
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={3}>
            <Box display="flex" alignItems="center">
              <ThermostatOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2">Temperatura del agua y aire</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={3}>
            <Box display="flex" alignItems="center">
              <WavesOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2">Estado del mar y oleaje</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={3}>
            <Box display="flex" alignItems="center">
              <AirOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2">Condiciones del viento</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={3}>
            <Box display="flex" alignItems="center">
              <LocationOnOutlined color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2">Banderas y ocupación</Typography>
            </Box>
          </Grid>
        </Grid>
        
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          <strong>Fuentes de datos:</strong> AEMET (oficial), OpenWeatherMap, Puertos del Estado
        </Typography>
      </Paper>
    </Box>
  );
};

export default HomePage;
