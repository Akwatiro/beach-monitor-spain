import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Grid,
  Paper,
  LinearProgress
} from '@mui/material';
import {
  CheckCircleOutlined,
  ErrorOutlined,
  WarningOutlined,
  CloudOutlined,
  WbSunnyOutlined,
  InfoOutlined
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import axios from 'axios';

interface SystemStatusData {
  system: {
    overall_status: string;
    active_sources: number;
    total_sources: number;
    primary_source: string;
    data_quality: string;
    last_update: string;
  };
  sources: {
    [key: string]: {
      status: string;
      name: string;
      description: string;
      configured: boolean;
      last_check: string;
      data_types: string[];
    };
  };
}

const getSystemStatus = async (): Promise<SystemStatusData> => {
  const response = await axios.get('http://localhost:8000/api/system/status');
  return response.data;
};

const SystemStatus: React.FC = () => {
  const { data: statusData, isLoading, error } = useQuery(
    'system-status',
    getSystemStatus,
    {
      refetchInterval: 30 * 1000, // Actualizar cada 30 segundos
    }
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      case 'simulated': return 'info';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircleOutlined color="success" />;
      case 'warning': return <WarningOutlined color="warning" />;
      case 'error': return <ErrorOutlined color="error" />;
      case 'simulated': return <CloudOutlined color="info" />;
      default: return <InfoOutlined />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Activo';
      case 'warning': return 'No configurado';
      case 'error': return 'Error';
      case 'simulated': return 'Simulado';
      default: return 'Desconocido';
    }
  };

  const getOverallStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'success';
      case 'degraded': return 'warning';
      case 'critical': return 'error';
      default: return 'info';
    }
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Estado de Fuentes de Datos
          </Typography>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  if (error || !statusData) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Estado de Fuentes de Datos
          </Typography>
          <Typography color="error">
            Error al cargar el estado del sistema
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          <Box display="flex" alignItems="center">
            <WbSunnyOutlined sx={{ mr: 1 }} />
            Estado de Fuentes de Datos
          </Box>
        </Typography>

        {/* Estado general del sistema */}
        <Box mb={3} p={2} borderRadius={1} bgcolor={
          statusData.system.overall_status === 'healthy' ? 'success.main' : 'warning.main'
        }>
          <Typography variant="body1" sx={{ color: 'white', fontWeight: 500 }}>
            🎯 <strong>Estado General:</strong> {statusData.system.overall_status === 'healthy' ? 'Saludable' : 'Degradado'} 
            ({statusData.system.active_sources}/{statusData.system.total_sources} fuentes activas)
          </Typography>
          <Typography variant="body2" sx={{ color: 'white' }}>
            <strong>Fuente principal:</strong> {statusData.system.primary_source} | 
            <strong> Calidad:</strong> {statusData.system.data_quality === 'official' ? 'Oficial' : 'Simulada'}
          </Typography>
        </Box>

        <Grid container spacing={2}>
          {Object.entries(statusData.sources).map(([key, source]) => (
            <Grid item xs={12} md={4} key={key}>
              <Paper elevation={1} sx={{ p: 2, height: '100%' }}>
                <Box display="flex" alignItems="center" mb={1}>
                  {getStatusIcon(source.status)}
                  <Typography variant="subtitle1" sx={{ ml: 1, fontWeight: 500 }}>
                    {source.name}
                  </Typography>
                </Box>

                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {source.description}
                </Typography>

                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <Chip 
                    label={getStatusText(source.status)}
                    color={getStatusColor(source.status) as any}
                    size="small"
                  />
                  {source.configured && (
                    <Chip 
                      label="Configurado"
                      color="success"
                      size="small"
                      variant="outlined"
                    />
                  )}
                </Box>

                <Typography variant="caption" color="text.secondary" gutterBottom>
                  Tipos de datos:
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5}>
                  {source.data_types.map((type, index) => (
                    <Chip 
                      key={index}
                      label={type} 
                      size="small" 
                      variant="outlined"
                      color="primary"
                    />
                  ))}
                </Box>

                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Última verificación: {new Date(source.last_check).toLocaleTimeString('es-ES')}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>

        <Box mt={3}>
          <Typography variant="body2" color="text.secondary">
            <strong>💡 Información:</strong> El sistema utiliza múltiples fuentes para garantizar 
            la disponibilidad de datos. AEMET es la fuente oficial y prioritaria para España.
            Cuando una fuente no está disponible, el sistema cambia automáticamente a alternativas.
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SystemStatus;
