# PYIMPORT
A Dynamic Requirements Loader (Pure Python)

Módulo ligero para instalar e importar dependencias dinámicamente a partir de un archivo tipo requirements.txt, sin depender de librerías externas.

¿QUÉ HACE?

Este módulo:

1. Lee un archivo de requisitos
2. Verifica si los paquetes están instalados (y si cumplen versión)
3. Instala lo necesario usando pip
4. Importa automáticamente los módulos (con alias opcional)

Todo en tiempo de ejecución.

EJEMPLO DE ARCHIVO requirements.txt

numpy as np >=1.24
matplotlib as plt
scipy
beautifulsoup4 as bs4
python-dateutil as dateutil >=2.8.0

FORMATO SOPORTADO

package_name [as alias] [operator version]

Ejemplos válidos:

numpy
numpy>=1.20
numpy as np >=1.20
scikit-learn==1.0.2
python-dateutil as dateutil >=2.8.0

Operadores soportados:

==   igual a

> =   mayor o igual
> <=   menor o igual
> mayor que
> <    menor que

CASOS ESPECIALES (MUY IMPORTANTE)

Algunos paquetes tienen nombres distintos entre pip e import.

## pip install        → import

beautifulsoup4     → bs4
Pillow             → PIL
pyyaml             → yaml

En estos casos DEBES usar alias:

beautifulsoup4 as bs4
Pillow as PIL
pyyaml as yaml

Si no lo haces → ImportError.

USO BÁSICO

Instalar + importar todo:

requirements("requirements.txt")

Importación inteligente (lazy):

importer("requirements.txt")

* Solo instala lo que falta
* Silencioso
* Ideal para notebooks o scripts rápidos

Solo instalar (sin importar):

installer("requirements.txt")

* Útil para setup o CI/CD

OPCIONES AVANZADAS

requirements(
file_path="requirements.txt",
force_reinstall=False,
upgrade=False,
show_output=True
)

Parámetros:

force_reinstall → reinstala siempre
upgrade → actualiza paquetes
show_output → controla logs y warnings

EJEMPLO COMPLETO

from your_module import requirements

requirements("requirements.txt")

# Ya puedes usar directamente:

print(np.array([1, 2, 3]))

DISEÑO

* 100% estándar (sin dependencias externas)
* Usa importlib, subprocess y warnings
* dprint basado en warnings (se puede silenciar)
* Verificación de versiones sin packaging

LIMITACIONES

* No implementa completamente PEP 440
* Ignora sufijos como rc, dev, etc.
* Comparación de versiones simplificada
* No resuelve dependencias complejas
* No agrupa instalaciones (llama pip por paquete)
* Requiere alias cuando pip name ≠ import name

NOTAS IMPORTANTES

* alias puede ser:

  * alias real (numpy as np)
  * nombre real de import (beautifulsoup4 as bs4)
* Los módulos se inyectan en globals()
* Puede sobrescribir variables existentes (lanza warning)

CASOS DE USO

* Scripts auto-contenidos
* Notebooks reproducibles
* Proyectos pequeños sin entorno virtual formal
* Entornos educativos

FUTURAS MEJORAS

* Soporte para múltiples condiciones (ej: numpy>=1.20,<2.0)
* Instalación en batch
* CLI (python -m module requirements.txt)
* Cache de dependencias

LICENCIA

Libre uso. Modifica, mejora y rompe cosas.
