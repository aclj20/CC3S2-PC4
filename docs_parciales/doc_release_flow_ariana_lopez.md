# CC3S2-PC4

## Scripts
### `release_flow.sh`
Script principal que orquesta el flujo de liberación local del proyecto. Ejecuta automáticamente el changelog_generator.py, muestra una vista previa del archivo CHANGELOG.md, detecta la nueva versión generada y permite al usuario confirmar si desea crear (o reetiquetar) y pushear el tag correspondiente al repositorio remoto.

#### Uso

```bash
bash release_flow.sh
```
