import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container } from '@mui/material';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ProvincePage from './pages/ProvincePage';
import BeachDetailPage from './pages/BeachDetailPage';

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/provincia/:provinceId" element={<ProvincePage />} />
          <Route path="/playa/:beachId" element={<BeachDetailPage />} />
        </Routes>
      </Container>
    </div>
  );
};

export default App;
