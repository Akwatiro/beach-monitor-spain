# Copilot Instructions - Beach Monitor Spain

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a full-stack web application for monitoring Spanish beaches in real-time by provinces. The project consists of:

- **Backend**: Python FastAPI with SQLAlchemy, Celery for background tasks
- **Frontend**: React TypeScript with Material-UI and Google Maps integration
- **Services**: Google Cloud Platform (Maps API, Places API, Cloud Storage, Cloud Run)
- **Data Sources**: AEMET weather data, beach quality indicators, webcams

## Code Style Guidelines
- Use TypeScript for all React components
- Follow REST API conventions for backend endpoints
- Use async/await for asynchronous operations
- Implement proper error handling and validation
- Use environment variables for API keys and configuration
- Follow Spanish naming conventions for beach and province data

## Key Features to Implement
- Interactive Google Maps with beach markers by province
- Real-time weather and sea conditions
- Beach occupancy estimation
- Water quality indicators
- Flag status (red, yellow, green)
- Trend charts and historical data
- WebSocket connections for live updates

## Data Models
- Beaches: name, coordinates, province, amenities
- Weather: temperature, wind, waves, precipitation
- Quality: water quality, flags, certifications
- Occupancy: estimated capacity, current occupancy

## API Integration Notes
- Use Google Maps JavaScript API for frontend maps
- Integrate AEMET API for official weather data
- Cache frequently accessed data with Redis
- Implement rate limiting for external API calls
