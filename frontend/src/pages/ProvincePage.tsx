import React from 'react';
import { useParams } from 'react-router-dom';
import { Typography } from '@mui/material';

const ProvincePage: React.FC = () => {
  const { provinceId } = useParams<{ provinceId: string }>();

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Playas de la Provincia {provinceId}
      </Typography>
      <Typography variant="body1">
        Página en desarrollo - aquí se mostrarán las playas de la provincia seleccionada
      </Typography>
    </div>
  );
};

export default ProvincePage;
