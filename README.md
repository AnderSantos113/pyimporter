PYMPORTER — Dynamic Requirements Loader (Pure Python)

Descripción
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Este módulo permite instalar e importar automáticamente las dependencias
de un proyecto a partir de un archivo de texto similar a requirements.txt.

El flujo general es:

1. Leer el archivo de requisitos
2. Detectar paquetes faltantes o con versión incorrecta
3. Instalar usando pip
4. Importar dinámicamente los módulos (con alias opcional)

Todo en tiempo de ejecución.

Instalación
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
pip install git+https://github.com/AnderSantos113/pymporter.git@v0.1

Uso básico
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Instalar + importar todo:
requirements("requirements.txt")

Importación inteligente (lazy):
importer("requirements.txt")

Solo instalación:
installer("requirements.txt")

Formato del archivo de requisitos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cada línea debe seguir:

package_name [as alias] [operator version]

Donde:

* "as alias" es opcional
* "operator version" es opcional

Ejemplos válidos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
numpy
numpy>=1.20
numpy as np >=1.20
scipy
beautifulsoup4 as bs4
scikit-learn==1.0.2
python-dateutil as dateutil >=2.8.0

Operadores de versión
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
==   igual a

> =   mayor o igual
> <=   menor o igual
> mayor que
> <    menor que

La versión debe ser un string numérico (ej. 1.2.3)

Casos especiales (CRÍTICO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Algunos paquetes tienen nombres distintos entre pip e import.

## pip name        → import name

beautifulsoup4  → bs4
Pillow          → PIL
pyyaml          → yaml

En estos casos ES OBLIGATORIO usar alias:

beautifulsoup4 as bs4
Pillow as PIL
pyyaml as yaml

Si no se usa alias → ImportError garantizado.

Funciones principales
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

requirements(file_path, force_reinstall=False, upgrade=False, show_output=True)

* Instala e importa todo
* Modo completo

importer(file_path)

* Solo instala lo necesario
* Silencioso
* Ideal para notebooks/scripts

installer(file_path, force_reinstall=False, upgrade=False, show_output=True)

* Solo instala
* No importa módulos
* Útil para setup o CI/CD

Notas de diseño
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* 100% Python estándar (sin dependencias externas)
* Usa importlib, subprocess y warnings
* dprint basado en warnings (se puede silenciar)
* Verificación de versiones simplificada (no PEP 440 completo)

Limitaciones
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* No soporta versiones complejas (rc, dev, etc.)
* No agrupa instalaciones (pip se ejecuta por paquete)
* No resuelve dependencias entre paquetes
* Comparación de versiones simplificada

Advertencias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* Los módulos se inyectan en globals()
* Un alias puede sobrescribir variables existentes (lanza warning)
* Se recomienda usar alias explícitos en proyectos grandes

Caso de uso ideal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

* Scripts auto-contenidos
* Notebooks reproducibles
* Proyectos pequeños sin entorno virtual formal
* Entornos educativos

Autor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proyecto desarrollado por Ander Santos
