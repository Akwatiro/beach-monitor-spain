import React from 'react';
import { useParams } from 'react-router-dom';
import { Typography } from '@mui/material';

const BeachDetailPage: React.FC = () => {
  const { beachId } = useParams<{ beachId: string }>();

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Detalle de la Playa {beachId}
      </Typography>
      <Typography variant="body1">
        Página en desarrollo - aquí se mostrará información detallada de la playa
      </Typography>
    </div>
  );
};

export default BeachDetailPage;
