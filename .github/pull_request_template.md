---
name: Pull Request
about: Template para Pull Requests
title: ''
labels: ''
assignees: ''
---

## 🎯 Descripción
### ¿Qué hace este PR?
Una descripción clara y concisa de los cambios realizados.

### ¿Por qué es necesario?
Explica la motivación y el contexto de estos cambios.

## 🔗 Issues Relacionados
<!-- Conecta con issues existentes -->
- Closes #(issue_number)
- Related to #(issue_number)

## 🛠️ Tipo de Cambio
- [ ] 🐛 Bug fix (cambio que no rompe funcionalidad y arregla un issue)
- [ ] ✨ Nueva feature (cambio que no rompe funcionalidad y agrega funcionalidad)
- [ ] 💥 Breaking change (fix o feature que causaría que funcionalidad existente no funcione como se espera)
- [ ] 📚 Documentación (solo cambios en documentación)
- [ ] 🎨 Estilo (formatting, punto y coma faltante, etc; sin cambio de lógica)
- [ ] ♻️ Refactor (cambio de código que ni arregla un bug ni agrega una feature)
- [ ] ⚡ Performance (cambio que mejora performance)
- [ ] ✅ Tests (agregar tests faltantes o corregir tests existentes)
- [ ] 🔧 Chore (cambios en build process, herramientas auxiliares, etc)

## 🧪 ¿Cómo Ha Sido Probado?
Describe las pruebas que ejecutaste para verificar tus cambios.

### Tests Ejecutados:
- [ ] Tests unitarios del backend
- [ ] Tests del frontend
- [ ] Tests de integración
- [ ] Tests manuales
- [ ] Tests en múltiples navegadores

### Configuración de Testing:
- **OS**: [ej. Windows 11, macOS, Ubuntu]
- **Browser**: [ej. Chrome 119, Firefox 120]
- **Python Version**: [ej. 3.11]
- **Node Version**: [ej. 18.17]

## ✅ Checklist
### Antes del Review:
- [ ] Mi código sigue las guías de estilo del proyecto
- [ ] He realizado una self-review de mi código
- [ ] He comentado mi código, particularmente en áreas difíciles de entender
- [ ] He hecho los cambios correspondientes en la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban que mi fix es efectivo o que mi feature funciona
- [ ] Tests nuevos y existentes pasan localmente con mis cambios
- [ ] Cualquier cambio dependiente ha sido merged y publicado

### Backend Específico:
- [ ] Endpoints siguen convenciones REST
- [ ] Agregados type hints donde corresponde
- [ ] Agregadas validaciones de entrada
- [ ] Agregado manejo de errores apropiado
- [ ] Documentación de API actualizada

### Frontend Específico:
- [ ] Componentes son responsive
- [ ] Agregadas interfaces TypeScript apropiadas
- [ ] Componentes siguen patrones establecidos
- [ ] Agregados tests para nuevos componentes
- [ ] Accessibility considerado

## 📸 Screenshots (si aplica)
### Antes:
<!-- Screenshots del estado antes del cambio -->

### Después:
<!-- Screenshots del estado después del cambio -->

## 📋 Notas Adicionales
- Cualquier información adicional que los reviewers deberían saber
- Dependencias que necesitan ser instaladas
- Configuración adicional requerida
- Impacto en rendimiento
- Consideraciones de seguridad

## 🔄 Próximos Pasos
- [ ] Merge este PR
- [ ] Deploy a staging
- [ ] Actualizar documentación externa
- [ ] Comunicar cambios al equipo
- [ ] Otros: ___________
