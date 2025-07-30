# 🤝 Contribuir a Beach Monitor Spain

¡Gracias por tu interés en contribuir a Beach Monitor Spain! Tu ayuda es muy bienvenida.

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio
```bash
# Hacer fork desde GitHub y luego clonar
git clone https://github.com/tu-usuario/beach-monitor-spain.git
cd beach-monitor-spain
```

### 2. Configurar Entorno de Desarrollo
```bash
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Instalar dependencias del frontend
cd ../frontend
npm install
```

### 3. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env
# Editar .env con tus claves de API
```

### 4. Crear Rama para tu Feature
```bash
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/descripcion-del-bug
```

### 5. Hacer Cambios y Commit
```bash
git add .
git commit -m "feat: descripción clara del cambio"
```

## 📋 Tipos de Contribuciones

### 🐛 **Reportar Bugs**
- Usa el template de issues
- Incluye pasos para reproducir
- Especifica navegador y OS

### ✨ **Nuevas Características**
- Abre un issue primero para discutir
- Sigue las convenciones de código
- Incluye tests si es posible

### 📚 **Documentación**
- Mejora el README
- Traduce a otros idiomas
- Agrega ejemplos de uso

### 🌍 **Datos de Playas**
- Agrega nuevas playas
- Corrige coordenadas
- Mejora información de amenities

## 🎯 Áreas de Contribución Prioritarias

### 🗺️ **Google Maps Integration**
- Implementar mapas interactivos
- Marcadores por provincia
- Info windows con datos meteorológicos

### 💾 **Base de Datos**
- Migración a PostgreSQL
- Modelos de datos históricos
- Optimización de consultas

### ⚡ **Performance**
- Implementar caché Redis
- Optimizar llamadas a APIs
- Lazy loading de componentes

### 📱 **Mobile First**
- Responsive design
- Progressive Web App
- Touch gestures

## 🛠️ Convenciones de Código

### **Python (Backend)**
```python
# Usar snake_case para variables y funciones
def get_beach_weather(beach_id: int) -> WeatherData:
    """Obtiene datos meteorológicos de una playa."""
    pass

# Usar type hints
# Documentar funciones con docstrings
# Seguir PEP 8
```

### **TypeScript (Frontend)**
```typescript
// Usar camelCase para variables y funciones
const getBeachWeather = async (beachId: number): Promise<WeatherData> => {
  // Usar interfaces para tipos
  // Documentar componentes con JSDoc
};

// Usar PascalCase para componentes
const WeatherCard: React.FC<WeatherCardProps> = ({ beach }) => {
  // Hooks al inicio
  // Event handlers con handle prefix
};
```

### **Commits**
Seguir [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: agrega integración con Google Maps
fix: corrige parsing de datos AEMET  
docs: actualiza guía de instalación
style: mejora estilos de WeatherCard
refactor: reorganiza estructura de servicios
test: agrega tests para weather service
chore: actualiza dependencias
```

## 🧪 Testing

### **Backend**
```bash
# Ejecutar tests
cd backend
python -m pytest

# Con coverage
python -m pytest --cov=.
```

### **Frontend**
```bash
# Ejecutar tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 📝 Pull Request Process

1. **Actualiza tu rama** con la última versión de main
2. **Ejecuta tests** y asegúrate de que pasen
3. **Actualiza documentación** si es necesario
4. **Crea el PR** con descripción clara
5. **Enlaza issues** relacionados
6. **Espera review** y atiende comentarios

### Template de PR
```markdown
## 🎯 Descripción
Breve descripción de los cambios

## 🔗 Issues Relacionados
Closes #123

## ✅ Checklist
- [ ] Tests pasan
- [ ] Documentación actualizada
- [ ] Sin conflictos de merge
- [ ] Código linted

## 📸 Screenshots
(Si aplica)
```

## 🌟 Reconocimientos

Los contribuidores serán añadidos a:
- Lista de contribuidores en README
- Sección de agradecimientos
- Release notes

## ❓ ¿Preguntas?

- 💬 Abre un [issue](https://github.com/usuario/beach-monitor-spain/issues)
- 📧 Contacta al mantenedor
- 🗨️ Únete a las [Discussions](https://github.com/usuario/beach-monitor-spain/discussions)

---

**¡Gracias por ayudar a mejorar Beach Monitor Spain!** 🏖️🌊
