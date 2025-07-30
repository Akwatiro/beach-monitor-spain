import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  CircularProgress,
  Box,
  Chip,
  Badge,
  Tooltip,
  IconButton,
  Alert
} from '@mui/material';
import { styled } from '@mui/material/styles';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import BeachAccessIcon from '@mui/icons-material/BeachAccess';
import StarIcon from '@mui/icons-material/Star';
import WifiIcon from '@mui/icons-material/Wifi';
import LocalParkingIcon from '@mui/icons-material/LocalParking';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import WcIcon from '@mui/icons-material/Wc';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import SportsIcon from '@mui/icons-material/Sports';
import SecurityIcon from '@mui/icons-material/Security';
import { Beach, getBeachesByProvince } from '../services/api';

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[8],
  },
}));

const ServiceChip = styled(Chip)(({ theme }) => ({
  margin: theme.spacing(0.5),
  fontSize: '0.75rem',
}));

const BlueFlagBadge = styled(Badge)(({ theme }) => ({
  '& .MuiBadge-badge': {
    backgroundColor: '#1976d2',
    color: 'white',
    fontWeight: 'bold',
  },
}));

const getServiceIcon = (service: string) => {
  const lowerService = service.toLowerCase();
  if (lowerService.includes('wifi') || lowerService.includes('internet')) return <WifiIcon fontSize="small" />;
  if (lowerService.includes('parking') || lowerService.includes('aparcamiento')) return <LocalParkingIcon fontSize="small" />;
  if (lowerService.includes('restaurant') || lowerService.includes('chiringuito') || lowerService.includes('bar')) return <RestaurantIcon fontSize="small" />;
  if (lowerService.includes('baños') || lowerService.includes('aseos')) return <WcIcon fontSize="small" />;
  if (lowerService.includes('primeros auxilios') || lowerService.includes('médico')) return <LocalHospitalIcon fontSize="small" />;
  if (lowerService.includes('deporte') || lowerService.includes('voleibol') || lowerService.includes('fútbol')) return <SportsIcon fontSize="small" />;
  if (lowerService.includes('socorrista') || lowerService.includes('vigilancia')) return <SecurityIcon fontSize="small" />;
  return <BeachAccessIcon fontSize="small" />;
};

const ProvincePage: React.FC = () => {
  const { provinceId } = useParams<{ provinceId: string }>();
  const navigate = useNavigate();
  const [beaches, setBeaches] = useState<Beach[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const provinceNames: { [key: string]: string } = {
    '1': 'Andalucía',
    '2': 'Valencia',
    '3': 'Cataluña',
    '4': 'Galicia',
    '5': 'Murcia',
    '6': 'Asturias',
    '7': 'Cantabria',
    '8': 'País Vasco',
    '9': 'Islas Baleares',
    '10': 'Islas Canarias'
  };

  useEffect(() => {
    const fetchBeaches = async () => {
      if (!provinceId) return;

      try {
        setLoading(true);
        const response = await getBeachesByProvince(parseInt(provinceId));
        setBeaches(response.beaches);
        setError(null);
      } catch (err) {
        setError('Error al cargar las playas de la provincia');
        console.error('Error fetching beaches:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchBeaches();
  }, [provinceId]);

  const handleBeachClick = (beachId: number) => {
    navigate(`/beach/${beachId}`);
  };

  const handleBackClick = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress size={60} />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  const provinceName = provinceNames[provinceId || ''] || `Provincia ${provinceId}`;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={handleBackClick} sx={{ mr: 2 }}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4" component="h1" sx={{ flexGrow: 1 }}>
          🏖️ Playas de {provinceName}
        </Typography>
      </Box>

      {beaches.length === 0 ? (
        <Alert severity="info">
          No hay playas disponibles para esta provincia en este momento.
        </Alert>
      ) : (
        <>
          <Typography variant="h6" gutterBottom sx={{ mb: 3, color: 'text.secondary' }}>
            {beaches.length} playas encontradas
          </Typography>

          <Grid container spacing={3}>
            {beaches.map((beach) => (
              <Grid item xs={12} sm={6} md={4} key={beach.id}>
                <StyledCard>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {beach.blue_flag ? (
                        <BlueFlagBadge badgeContent="🏆" overlap="circular">
                          <Typography variant="h6" component="h2" sx={{ mr: 1 }}>
                            {beach.name}
                          </Typography>
                        </BlueFlagBadge>
                      ) : (
                        <Typography variant="h6" component="h2">
                          {beach.name}
                        </Typography>
                      )}
                      {beach.blue_flag && (
                        <Tooltip title="Bandera Azul - Playa certificada por su calidad ambiental">
                          <StarIcon color="primary" sx={{ ml: 1 }} />
                        </Tooltip>
                      )}
                    </Box>

                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <LocationOnIcon fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} />
                      <Typography variant="body2" color="text.secondary">
                        {beach.municipality}, {beach.province}
                      </Typography>
                    </Box>

                    <Typography variant="body2" paragraph sx={{ mb: 2 }}>
                      {beach.description}
                    </Typography>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Características:
                      </Typography>
                      <Grid container spacing={1}>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Longitud: {beach.length_km} km
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Anchura: {beach.width_m} m
                          </Typography>
                        </Grid>
                        <Grid item xs={12}>
                          <Typography variant="caption" color="text.secondary">
                            Tipo de arena: {beach.sand_type}
                          </Typography>
                        </Grid>
                      </Grid>
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Servicios:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
                        {beach.services.map((service, index) => (
                          <ServiceChip
                            key={index}
                            icon={getServiceIcon(service)}
                            label={service}
                            size="small"
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </Box>
                  </CardContent>

                  <CardActions>
                    <Button
                      size="small"
                      variant="contained"
                      fullWidth
                      onClick={() => handleBeachClick(beach.id)}
                      startIcon={<BeachAccessIcon />}
                    >
                      Ver detalles y clima
                    </Button>
                  </CardActions>
                </StyledCard>
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </Container>
  );
};

export default ProvincePage;
