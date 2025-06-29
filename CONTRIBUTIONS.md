# Contribuciones de Ariana López

## Sprint 1 - Implementación de Git Hooks

- 2025-06-24: Implementé los hooks `commit-msg` y `pre-push` para validar el formato de los mensajes de commit según Conventional Commits. También añadí un script de instalación (`setup-hooks.sh`) para facilitar su activación en entornos locales.

  Commits:
  - feat(hooks): agregar scripts de commit-msg y pre-push para validación de mensajes
  - chore(hooks): añadir script para instalar los hooks localmente
  - fix(hooks): corregir patrón regex en pre-push para detectar formato inválido
  - chore(hooks): eliminar salida de depuración del hook commit-msg

  PR: #3


## Sprint 2 - Generación de CHANGELOG y versionado semántico
- 2025-06-28: Extendí el script `changelog_generator.py` para generar automáticamente un archivo `CHANGELOG.md` en formato Markdown, agrupando los commits por tipo (`feat`, `fix`, etc.). Además, implementé la lógica para calcular la siguiente versión siguiendo el esquema de versionado semántico (`MAJOR.MINOR.PATCH`) a partir del último tag. El script también crea un nuevo tag Git local con la versión calculada.

  Commits:
  - feat(scripts): extender script para generar archivo CHANGELOG.md automáticamente
  - feat(scripts): detectar y clasificar commits BREAKINGCHANGE
  - feat(scripts): generar tag semántico a partir de commits desde el último tag
  - docs(scripts): agregar documentación sobre generación de changelog y tags

  PR: #12

## Sprint 3 - 

