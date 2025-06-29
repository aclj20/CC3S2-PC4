"""
changelog_generator.py

Script para parsear commits en un repositorio Git priorizando commits convencionales
a partir del último tag y guardar la información en formato JSON.

Uso:
    python changelog_generator.py [-d RUTA_REPOSITORIO] [-o ARCHIVO_SALIDA]

Parámetros:
    -d, --dir     Ruta al repositorio Git a analizar (por defecto: el directorio actual).
    -o, --out Ruta donde se guardará el archivo JSON generado (por defecto: parsed_commits.json).

Ejemplo:
    python changelog_generator.py -d ./mi_repositorio -o ./salidas/commits.json

Requiere:
    - Python 3.6+
    - GitPython

Autor:
    Diego Akira García Rojas - Akira-13
    Ariana Camila Lopez Julcarima - aclj20
"""

import json
import re
import argparse
# Se utiliza la librería GitPython para interactuar con lso repositorios a través de una API.
# De esta forma se evita trabajar directamente con comandos git en subprocesos.
from git import Repo
from typing import Dict, List
from collections import defaultdict

# Regex para parsear mensajes convencionales de commits.
COMMIT_REGEX = r'^(feat|fix|chore|docs|refactor|test|style|perf|ci|build|revert)(!)?(\([^)]+\))?: (.+)$'

def parse_commit_message(commit_msg: str, commit_hash: str) -> Dict:
    """
    Leer mensaje de commit convencional.

    Argumentos
    ----------
    commit_msg: str
      Mensaje de commit a analizar
    commit_hash: str
      Hash del commit

    Retorna
    -------
    Dict
      Diccionario con la información del commit
    """
    lines = commit_msg.strip().split("\n")
    header = lines[0]
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else None

    match = re.match(COMMIT_REGEX, header)

    if match:
        tipo_base = match.group(1)
        es_breaking = match.group(2) == "!"
        escopo = match.group(3)[1:-1] if match.group(3) else None
        descripcion = match.group(4)

        tipo = "BREAKING CHANGE" if es_breaking else tipo_base
    else:
        tipo = "otro"
        escopo = None
        descripcion = header

    return {
        "commit": commit_hash,
        "mensaje": {
            "tipo": tipo,
            "escopo": escopo,
            "descripcion": descripcion,
            "cuerpo": body or None
        }
    }

def get_commits_since_last_tag(repo_path=".") -> List[Dict]:
    """
    Leer commits desde el último tag del repositorio

    Argumentos
    ----------
    repo_path: str
      Ruta relativa del repositorio a analizar

    Retorna
    -------
    parsed_commits: List[Dict]
       Lista de diccionarios con información de commits
    """
    repo = Repo(repo_path)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if not tags:
        raise ValueError("No se encontraron tags en el repositorio.")

    last_tag = tags[-1]
    commits = list(repo.iter_commits(f"{last_tag}..HEAD"))

    print(f"Se encontraron {len(commits)} commits desde el último tag: {last_tag}")

    parsed_commits = []
    for commit in reversed(commits): 
        parsed = parse_commit_message(commit.message, commit.hexsha)
        parsed_commits.append(parsed)

    return parsed_commits

def generar_changelog_md(parsed_commits: List[Dict], version: str, archivo_salida: str = "CHANGELOG.md") -> None:
    """
    Genera un archivo CHANGELOG.md agrupado por tipo de commit.

    Argumentos
    ----------
    parsed_commits : List[Dict]
        Lista de commits parseados
    vesrion: str
        Nueva versión 
    archivo_salida : str
        Nombre del archivo markdown de salida
    """
    tipo_to_titulo = {
        "feat": "### Features",
        "fix": "### Bug Fixes",
        "chore": "### Chores",
        "docs": "### Documentation",
        "refactor": "### Refactors",
        "test": "### Tests",
        "style": "### Styles",
        "perf": "### Performance",
        "ci": "### CI",
        "build": "### Build",
        "revert": "### Reverts",
        "BREAKING CHANGE": "### Breaking Changes",
        "otro": "### Others"
    }

    # Agrupar los commits por tipo
    agrupados = defaultdict(list)
    for c in parsed_commits:
        tipo = c["mensaje"]["tipo"]
        descripcion = c["mensaje"]["descripcion"]
        agrupados[tipo].append(f"- {descripcion}")

    # Crear el contenido del archivo markdown
    md_lines = ["# Changelog\n", f"## {version}\n"]
    for tipo in tipo_to_titulo:
        if tipo in agrupados:
            md_lines.append(tipo_to_titulo[tipo])
            md_lines.extend(agrupados[tipo])
            md_lines.append("")  

    # Escribir el archivo
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Changelog generado en '{archivo_salida}'")

def calcular_siguiente_version(commits: List[Dict], tag_actual: str) -> str:
    """
    Calcula la siguiente versión semántica a partir del último tag y commits.

    Argumentos
    ----------
    commits : List[Dict]
        Lista de commits parseados desde el último tag
    tag_actual : str
        Último tag encontrado en el repositorio 
    
    Retorna
    -------
    str
        La siguiente versión sugerida 
    """
    mayor, menor, parche = map(int, tag_actual.lstrip("v").split("."))

    tipos = [c["mensaje"]["tipo"] for c in commits]

    # Si hay BREAKING CHANGE, subir versión mayor
    if "BREAKING CHANGE" in tipos:
        mayor += 1
        menor = 0
        parche = 0
    # Si hay feats pero no breaking, subir versión menor
    elif "feat" in tipos:
        menor += 1
        parche = 0
    # Si solo hay fixes, subir parche
    elif "fix" in tipos:
        parche += 1
    else:
        # Si no hay cambios relevantes, se mantiene la versión
        pass

    return f"v{mayor}.{menor}.{parche}"

def crear_tag(repo_path: str, nueva_version: str):
    """
    Crea un nuevo tag Git en el repositorio local con la versión proporcionada

    Argumentos
    ----------
    repo_path : str
        Ruta al repositorio Git 
    nueva_version : str
        Nombre del tag a crear
    """
    repo = Repo(repo_path)
    # Crear un nuevo tag en el commit HEAD
    repo.create_tag(nueva_version)
    print(f"Tag '{nueva_version}' creado.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Parsea commits desde el último tag en un repositorio Git.",
                                     "\nAlmacena los commits parseados en parsed_commits.json"))
    # Argumentos
    parser.add_argument(
        "-d", "--dir",
        type=str,
        default=".",
        help="Ruta al repositorio Git (por defecto: directorio actual '.')"
    )
    parser.add_argument(
        "-o", "--out",
        type=str,
        default="parsed_commits.json",
        help="Ruta del archivo de salida (por defecto: parsed_commits.json)"
    )

    args = parser.parse_args()

    # Lectura de commits
    parsed_commits = get_commits_since_last_tag(args.dir)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(parsed_commits, f, indent=2, ensure_ascii=False)
    print("Commits parseados guardados en 'parsed_commits.json'")

    repo = Repo(args.dir)
    # Obtener todos los tags ordenados por fecha de creación
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    # Obtener el último tag existente o usar "v0.0.0" si no hay ninguno
    ultimo_tag = tags[-1].name if tags else "v0.0.0"
    # Calcular la siguiente versión del proyecto 
    nueva_version = calcular_siguiente_version(parsed_commits, ultimo_tag)
    # Generar archivo CHANGELOG.md
    generar_changelog_md(parsed_commits, nueva_version)
    # Crear un nuevo tag Git en el repositorio local con la versión calculada
    crear_tag(args.dir, nueva_version)
