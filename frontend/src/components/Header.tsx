import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { WavesOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="static" sx={{ backgroundColor: '#1976d2' }}>
      <Toolbar>
        <WavesOutlined sx={{ mr: 2 }} />
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Beach Monitor Spain
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button 
            color="inherit" 
            onClick={() => navigate('/')}
          >
            Inicio
          </Button>
          <Button color="inherit">
            Mapa
          </Button>
          <Button color="inherit">
            Alertas
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
