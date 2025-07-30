import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Alert,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  AlertColor
} from '@mui/material';
import {
  WarningOutlined,
  InfoOutlined,
  ErrorOutlined
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';

interface WeatherAlert {
  id: number;
  type: string;
  level: 'yellow' | 'orange' | 'red';
  title: string;
  description: string;
  provinces: string[];
  start_time: string;
  end_time: string;
  source: string;
}

const getWeatherAlerts = async (): Promise<{ alerts: WeatherAlert[], total: number }> => {
  const response = await axios.get('http://localhost:8000/api/weather/alerts');
  return response.data;
};

const WeatherAlerts: React.FC = () => {
  const { data: alertsData, isLoading, error } = useQuery(
    'weather-alerts',
    getWeatherAlerts,
    {
      refetchInterval: 10 * 60 * 1000, // Actualizar cada 10 minutos
    }
  );

  const getAlertSeverity = (level: string): AlertColor => {
    switch (level) {
      case 'yellow': return 'warning';
      case 'orange': return 'warning';
      case 'red': return 'error';
      default: return 'info';
    }
  };

  const getAlertIcon = (level: string) => {
    switch (level) {
      case 'yellow': return <InfoOutlined />;
      case 'orange': return <WarningOutlined />;
      case 'red': return <ErrorOutlined />;
      default: return <InfoOutlined />;
    }
  };

  const formatTime = (timeString: string) => {
    return new Date(timeString).toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Alertas Meteorológicas
          </Typography>
          <Typography variant="body2">
            Cargando alertas...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Alertas Meteorológicas
          </Typography>
          <Alert severity="error">
            Error al cargar las alertas meteorológicas
          </Alert>
        </CardContent>
      </Card>
    );
  }

  if (!alertsData?.alerts || alertsData.alerts.length === 0) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Alertas Meteorológicas
          </Typography>
          <Alert severity="success">
            No hay alertas meteorológicas activas
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Alertas Meteorológicas ({alertsData.total})
        </Typography>
        
        <List disablePadding>
          {alertsData.alerts.map((alert) => (
            <ListItem key={alert.id} disablePadding sx={{ mb: 2 }}>
              <Card variant="outlined" sx={{ width: '100%' }}>
                <CardContent sx={{ pb: '16px !important' }}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    {getAlertIcon(alert.level)}
                    <Typography variant="h6" component="h3">
                      {alert.title}
                    </Typography>
                    <Chip 
                      label={alert.level.toUpperCase()} 
                      color={getAlertSeverity(alert.level)}
                      size="small"
                    />
                  </Box>
                  
                  <Alert 
                    severity={getAlertSeverity(alert.level)} 
                    sx={{ mb: 2 }}
                  >
                    {alert.description}
                  </Alert>
                  
                  <Box mb={1}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Provincias afectadas:</strong>
                    </Typography>
                    <Box display="flex" gap={0.5} flexWrap="wrap">
                      {alert.provinces.map((province, index) => (
                        <Chip 
                          key={index}
                          label={province} 
                          size="small" 
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </Box>
                  
                  <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
                    <Typography variant="body2" color="text.secondary">
                      <strong>Vigencia:</strong> {formatTime(alert.start_time)} - {formatTime(alert.end_time)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      <strong>Fuente:</strong> {alert.source}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default WeatherAlerts;
