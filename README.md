
# CC3S2-PC3
## Nombre

Ariana Camila Lopez Julcarima

## Correo

ariana.lopez.j@uni.pe

## Proyecto

Proyecto 15: Automatización de generación de CHANGELOG y versionado semántico

## Repositorio grupal:

https://github.com/SandroCJ210/CC3S2-PC4.git

## Contribuciones 
Durante el Sprint 1, configuré los hooks commit-msg y pre-push para validar mensajes de commit con formato Conventional Commits. También creé el script setup-hooks.sh para instalarlos fácilmente y documenté su uso en el README.

Durante el Sprint 2, extendí el script `changelog_generator.py` para generar automáticamente un archivo `CHANGELOG.md` agrupando los commits por tipo. Implementé el cálculo de la siguiente versión semántica a partir del último tag y la creación de un nuevo tag local. También se mejoró la detección de commits `BREAKING CHANGE` y se actualizó la documentación del proyecto.

## Instrucciones de uso
```
git clone https://github.com/aclj20/CC3S2-PC4.git


```