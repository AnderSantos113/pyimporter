""" La función de este módulo es importar los requisitos necesarios para un 
proyecto a partir de un archivo de texto tipo requirements.txt.

Para ello se debe:
1) Leer el archivo de texto y extraer los nombres de los paquetes.
2) Verificar si hay paquetes que no estén instalados en el entorno actual.
3) Instalar los paquetes que no estén instalados utilizando pip.
4) Importar los paquetes instalados.

FORMATO DE LÍNEA EN EL ARCHIVO DE REQUISITOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  package_name [as alias] [operator version]

ejemplos válidos:
  numpy
  numpy>=1.20
  numpy as np >=1.20
  beautifulsoup4 as bs4
  scikit-learn==1.0.2
  python-dateutil as dateutil >=2.8.0

donde 'operator' puede ser:
  ==  (igual a)
  >=  (igual o mayor que)
  <=  (igual o menor que)
  >   (mayor que)
  <   (menor que)

⚠️ CASOS ESPECIALES (pip name ≠ import name):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Si hay DESAJUSTE entre el nombre del paquete pip y el nombre de importación,
DEBES usar el alias obligatoriamente:

  beautifulsoup4 as bs4          # pip: beautifulsoup4, import: bs4
  Pillow as PIL                  # pip: Pillow, import: PIL
  pyyaml as yaml                 # pip: pyyaml, import: yaml

Sin alias en estos casos → error de importación garantizado.
"""
# Importar las bibliotecas necesarias (nativas de Python)
import subprocess  # Para ejecutar comandos del sistema, como pip install
import sys  # Para acceder a la información del sistema
import importlib  # Para importar módulos de forma dinámica
import warnings  # Para mostrar advertencias al usuario
import importlib.util
import importlib.metadata
import re


#------------ FUNCIONES AUXILIARES ------------#
class DebugWarning(UserWarning):
    # Definir una clase de advertencia personalizada para mensajes de depuración
    pass

def dprint(*args):
    """
    Función de depuración para imprimir mensajes en la consola.
    Utiliza warnings.warn para mostrar los mensajes, lo que permite controlar
    el nivel de detalle y evitar la saturación de la consola.
    """
    msg = " ".join(map(str, args))
    warnings.warn(msg, DebugWarning, stacklevel=2)

def parse_version(v):
    """
    Convierte una versión en string a una tupla de enteros.

    Ejemplo:
    "1.2.3" → (1, 2, 3)

    Nota:
    - Extrae SOLO números (ignora sufijos como 'rc', 'dev', etc.)
    - Esto simplifica la comparación pero no sigue completamente PEP 440
    
    Levanta:
    - ValueError: si la versión no contiene números válidos
    """
    nums = re.findall(r'\d+', v)
    if not nums:
        raise ValueError(f"Versión inválida (sin números): '{v}'")
    return tuple(map(int, nums))

def compare_versions(installed, spec):
    """
    Compara una versión instalada contra un especificador.

    Parámetros:
    - installed: versión instalada (string), ej. "1.2.3"
    - spec: condición, ej. ">=1.2.0", "==1.2.3"

    Soporta operadores:
    ==, >=, <=, >, <

    Proceso:
    1. Separa operador y versión objetivo
    2. Convierte ambas versiones a tuplas
    3. Compara según el operador
    
    Levanta:
    - ValueError: si el formato es inválido o versión no tiene números
    """

    # Extrae operador y versión (ej. ">=", "1.2.3")
    match = re.match(r'(==|>=|<=|>|<)(.+)', spec)
    if not match:
        raise ValueError(f"Formato de versión inválido: {spec}")

    op, v = match.groups()

    # Convierte versiones a tuplas de enteros
    v_tuple = parse_version(v)
    i_tuple = parse_version(installed)

    # Comparación según operador
    if op == "==":
        return i_tuple == v_tuple
    elif op == ">=":
        return i_tuple >= v_tuple
    elif op == "<=":
        return i_tuple <= v_tuple
    elif op == ">":
        return i_tuple > v_tuple
    elif op == "<":
        return i_tuple < v_tuple
    
    # Garantiza que siempre retorna un valor booleano válido
    raise ValueError(f"Operador no soportado: '{op}'")

def is_installed(pkg, version=None):
    """
    Verifica si un paquete está instalado y opcionalmente
    si cumple una restricción de versión.

    Parámetros:
    - pkg: nombre del paquete (normalmente el pip name, ej. "numpy")
    - version: condición opcional, ej. ">=1.2.3"

    ⚠️ CASOS DE DESAJUSTE pip name ≠ import name:
    Esta función busca usando pipe name (ej. "beautifulsoup4").
    Para estos casos especiales, usa alias en parse_package_line():
        beautifulsoup4 as bs4
    
    Internamente entonces verifica:
    1. importlib.util.find_spec(pkg) → "¿existe el módulo?"
    2. importlib.metadata.version(pkg) → "¿qué versión?"
    3. Compara contra la condición requerida

    Flujo:
    1. Verifica existencia del paquete (sin importarlo)
    2. Si no se pide versión → retorna True
    3. Obtiene versión instalada
    4. Compara contra la condición

    Retorna:
    - True si cumple la condición (o existe si no hay condición)
    - False en cualquier otro caso
    
    Levanta:
    - ValueError: si el especificador de versión es inválido
    """

    # Verifica si el módulo existe sin importarlo
    if importlib.util.find_spec(pkg) is None:
        return False

    # Si no se especifica versión, basta con que exista
    if version is None:
        return True

    try:
        # Obtiene la versión instalada del paquete
        installed_version = importlib.metadata.version(pkg)
    except importlib.metadata.PackageNotFoundError:
        # Puede pasar si el paquete no tiene metadata accesible
        return False

    # Compara versión instalada contra la condición
    return compare_versions(installed_version, version)

def parse_package_line(line):
    """
    Analiza una línea del archivo de requisitos y extrae el nombre del paquete,
    el alias (si existe) y la versión (si existe).

    Formato esperado:
    package_name [as alias] [operator version]

    Ejemplos válidos:
    - numpy
    - numpy>=1.20
    - numpy as np >=1.20
    - beautifulsoup4 as bs4  (OBLIGATORIO si pip name ≠ import name)
    - scikit-learn
    
    ⚠️ IMPORTANTE:
    Si el nombre de pip NO coincide con el nombre de importación,
    debes usar "as alias" obligatoriamente. Ejemplos donde SE NECESITA:
    - beautifulsoup4 as bs4
    - Pillow as PIL
    - pyyaml as yaml

    Retorna:
    - package: El nombre del paquete a instalar (pip name).
    - alias: El alias para importar (o None si no se especifica).
    - version: La condición de versión (o None si no se especifica).
    
    Si la línea es inválida → retorna (None, None, None) y lanza warning.
    """

    # Quitar comentarios y espacios en blanco
    line = line.split("#")[0].strip()

    # Si la línea quedó vacía después de limpiar, retornar None
    if not line:
        return None, None, None

    # Expresión regular para analizar la línea
    pattern = r'^([a-zA-Z0-9_\-\.]+)(?:\s+as\s+(\w+))?(?:\s+(==|>=|<=|>|<)\s*([\d\.]+))?$'
    match = re.match(pattern, line)

    # Si la línea no coincide con el formato esperado, se lanza un warning y se omite
    if not match:
        warnings.warn(f"Formato de línea inválido: '{line}'", UserWarning)
        return None, None, None

    # Extrae los componentes de la línea
    package = match.group(1)
    alias = match.group(2) if match.group(2) else None
    version = f"{match.group(3)}{match.group(4)}" if match.group(3) and match.group(4) else None

    return package, alias, version

#------------- FUNCIONES DE NUCLEO -------------#
def install_package(package, force_reinstall=False, upgrade=False,
                    version=None, show_output=True):
    """
    Instala un paquete utilizando pip con control de versión y salida.

    Parámetros:
    - package: nombre del paquete (ej. "numpy")
    - force_reinstall: si True, reinstala aunque ya exista
    - upgrade: si True, actualiza el paquete
    - version: condición de versión (ej. ">=1.2.3")
    - show_output: controla tanto prints (dprint) como output de pip

    Notas:
    - Usa 'pip install' internamente
    - Usa 'is_installed' para verificar existencia/versión
    - Usa 'dprint' (basado en warnings) para mensajes controlables
    """

    # Construcción del comando
    cmd = [sys.executable, "-m", "pip", "install"]

    # Construye especificación del paquete: "numpy" o "numpy>=1.2.3"
    package_spec = f"{package}{version}" if version else package

    # Si no se quiere output, se usa modo silencioso de pip
    if not show_output:
        cmd += ["-q"]

    # Control de warnings - se silencia SOLO DebugWarning si se desea
    with warnings.catch_warnings():
        if not show_output:
            warnings.simplefilter("ignore", DebugWarning)

        # MODO FORZADO: Reinstala sin importar estado actual
        if force_reinstall:
            dprint(f"Reinstalando '{package_spec}'...")
            try:
                subprocess.check_call(cmd + ["--force-reinstall", package_spec])
                dprint(f"'{package_spec}' reinstalado correctamente.")
            except subprocess.CalledProcessError as e:
                warnings.warn(f"Error al reinstalar '{package_spec}': {e}", UserWarning)
            return

        # VERIFICACIÓN: ¿Ya está instalado y cumple versión?
        installed = is_installed(package, version)

        # YA INSTALADO (SIN UPDATE)
        if installed and not upgrade:
            dprint(f"'{package_spec}' ya está instalado.")
            return

        # UPDATE
        if installed and upgrade:
            dprint(f"Actualizando '{package_spec}'...")
            try:
                subprocess.check_call(cmd + ["--upgrade", package_spec])
                dprint(f"'{package_spec}' actualizado correctamente.")
            except subprocess.CalledProcessError as e:
                warnings.warn(f"Error al actualizar '{package_spec}': {e}", UserWarning)
            return

        # INSTALACIÓN: No está instalado o no cumple versión
        dprint(f"Instalando '{package_spec}'...")
        try:
            subprocess.check_call(cmd + [package_spec])
            dprint(f"'{package_spec}' instalado correctamente.")
        except subprocess.CalledProcessError as e:
            warnings.warn(f"Error al instalar '{package_spec}': {e}", UserWarning)

def import_package(package, alias=None):
    """
    Importa un paquete dinámicamente. 
    Si se proporciona un alias, el paquete se importará con ese nombre en el 
    espacio de nombres global.

    NOTA IMPORTANTE - Desajuste pip vs import name:
    - beautifulsoup4 (pip) → bs4 (import)
    - Pillow (pip) → PIL (import)
    
    Si hay desajuste, DEBES especificar el alias en el archivo:
        beautifulsoup4 as bs4
    
    Submódulos:
    - Con numpy.linalg, el alias apunta al submódulo, no al raíz
    
    Levanta:
    - ImportError: si el módulo no existe
    - RuntimeWarning: si sobrescribe una variable existente
    """

    module_name = alias if alias else package

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise ImportError(f"No se puede importar '{module_name}': {e}")

    if alias:
        if alias in globals():
            warnings.warn(
                f"Alias '{alias}' sobrescribirá una variable existente en globals()",
                RuntimeWarning,
                stacklevel=2
            )
        globals()[alias] = module

    return module


#------------- FUNCIONES PRINCIPALES -------------#
def requirements(file_path, force_reinstall=False, upgrade=False,
                 show_output=True):
    """
    Lee un archivo de requisitos e instala e importa los paquetes listados.

    Parámetros:
    - file_path: ruta al archivo de requisitos (ej. "requirements.txt")
    - force_reinstall: si True, reinstala todos los paquetes sin importar su estado
    - upgrade: si True, actualiza los paquetes aunque ya estén instalados
    - show_output: controla tanto prints (dprint) como output de pip

    Flujo:
    1. Lee el archivo línea por línea
    2. Para cada línea válida, extrae paquete, alias y versión
    3. Instala el paquete según las opciones dadas
    4. Importa el paquete con el alias si se especifica
    
    ⚠️ IMPORTANTE: Si un paquete tiene pip name ≠ import name,
       debes especificar el alias:
           beautifulsoup4 as bs4
       Sin alias → ImportError
    
    Levanta:
    - FileNotFoundError: si el archivo no existe
    - Exception: otros errores durante la lectura/procesamiento
    """

    try:
        with open(file_path, "r") as f:
            for line in f:
                package, alias, version = parse_package_line(line)
                if not package:
                    continue  # Línea inválida o comentario

                install_package(package, force_reinstall=force_reinstall,
                                upgrade=upgrade, version=version,
                                show_output=show_output)
                import_package(package, alias)

    except FileNotFoundError:
        warnings.warn(f"Archivo no encontrado: '{file_path}'", UserWarning)
    except Exception as e:
        warnings.warn(f"Error al procesar el archivo: {e}", UserWarning)
		
def importer(file_path):
    """
    Instalador "lazy" que solo importa requisitos necesarios.
    
    Función para scripts/notebooks que necesitan ciertos paquetes.
    Instala SOLO si no existe con la versión requerida.

    Parámetros:
    - file_path: ruta al archivo de requisitos
    
    Comportamiento:
    - Lee línea por línea
    - Salta paquetes ya instalados (con versión válida)
    - Solo instala lo faltante (silencioso)
    - Importa automáticamente cada paquete
    
    Caso de uso típico:
        importer("requirements.txt")
        # Listo, ya puedes usar np, pd, etc.
    
    ⚠️ IMPORTANTE: Si un paquete tiene pip name ≠ import name,
       debes especificar el alias en el archivo:
           beautifulsoup4 as bs4
       Sin alias → ImportError
    
    Levanta:
    - FileNotFoundError: si el archivo no existe
    """

    try:
        with open(file_path, "r") as f:
            for line in f:
                package, alias, version = parse_package_line(line)
                if not package:
                    continue  # Línea inválida o comentario

                if not is_installed(package, version):
                    install_package(package, version=version, show_output=False)

                import_package(package, alias)
    except FileNotFoundError:
        warnings.warn(f"Archivo no encontrado: '{file_path}'", UserWarning)
		
def installer(file_path, force_reinstall=False, upgrade=False, 
              show_output=True):
    """
    Instalador de requisitos sin importación automática.
    
    Para scenarios donde SOLO necesitas instalar paquetes.
    Útil en scripts de setup o CI/CD.

    Parámetros:
    - file_path: ruta al archivo de requisitos
    - force_reinstall: si True, reinstala todos los paquetes
    - upgrade: si True, actualiza los paquetes aunque ya estén instalados
    - show_output: controla tanto prints (dprint) como output de pip

    Comportamiento:
    - Lee línea por línea
    - Instala/actualiza según opciones
    - NO importa paquetes
    - Ignora los alias en requirements.txt
    
    Notas:
    - Más agresivo que importer() (puede actualizar)
    - Útil para CI/CD o pre-setup antes de usar importer()
    
    Levanta:
    - FileNotFoundError: si el archivo no existe
    """

    try:
        with open(file_path, "r") as f:
            for line in f:
                package, _, version = parse_package_line(line)

                if not package:
                    continue  # Línea inválida o comentario

                if not is_installed(package, version):
                    install_package(package, version=version,
                                    force_reinstall=force_reinstall,
                                    upgrade=upgrade,
                                    show_output=show_output)

    except FileNotFoundError:
        warnings.warn(f"Archivo no encontrado: '{file_path}'", UserWarning)
		

