# PYMPORTER  
Dynamic Requirements Loader (Pure Python!)

## Description

This is a straightforward module that allows you to automatically install and import a project's dependencies from a text file, using an enriched syntax.

The general workflow is simple:

1.  Read the custom requirements file.
2.  Install the packages using pip (if requested).
3.  Dynamically import the modules and inject them into your script.

Everything happens at runtime, keeping your workspace flexible.

## Installation

pip install pymporter

(Or directly from GitHub for the latest version):

pip install git+[https://github.com/AnderSantos113/pymporter.git@v1.0.0](https://www.google.com/search?q=https://github.com/AnderSantos113/pymporter.git%40v1.0.0)

## Basic Usage

Install + import everything directly into your scope:
requirements("libs.txt")

Only import (assumes they are already installed):
importer("libs.txt")

Only install (does not inject variables into your code):
installer("libs.txt")

## Requirements File Format

The syntax is designed to be flexible on a single line. The general structure is:

[import expression] [version] [: pip install name or url]

## Valid Examples:


### Simple imports

numpy
pandas \>= 2.0.0

### Aliases and specific objects

import numpy as np
numpy as np \<= 1.21.0
from urllib import request as req

### Different pip names / Custom URLs (See Special Cases below)

import bs4 : beautifulsoup4
pyimporter as pimp : git+[https://github.com/AnderSantos113/pyimporter.git](https://www.google.com/search?q=https://github.com/AnderSantos113/pyimporter.git)

## Version Operators

\==    equal to

 \>=   greater than or equal to
 
 \<=   less than or equal to
 
 \>    greater than
 
 \<    less than

## Special Cases (The ":" Operator)

Sometimes the name you use to import a package in Python is not the same name you use to install it via pip.

For example:
pip install beautifulsoup4  -\> import bs4
pip install PyYAML          -\> import yaml

For these cases, you can use the `:` separator to specify the pip install name. The left side is what gets imported, and the right side is what gets installed:

import bs4 : beautifulsoup4
import yaml : pyyaml
import cv2 : opencv-python

You can also use this to install directly from a GitHub repository:
my\_module : git+[https://github.com/user/repo.git](https://github.com/user/repo.git)

## Main Functions


requirements(file\_path, force\_reinstall=False, upgrade=False, show\_output=True)

  * Installs missing dependencies and imports them into your global scope.
  * The most complete mode.

importer(file\_path)

  * Purely imports the packages into your scope.
  * Does not attempt to install anything using pip.

installer(file\_path, force\_reinstall=False, upgrade=False, show\_output=True)

  * Only runs the pip installation process.
  * Does not import or inject variables.

## Design Notes

  * 100% standard Python (no third-party dependencies).
  * Uses importlib, subprocess, and warnings.
  * Captures the caller's scope using sys.\_getframe() for variable injection.

## Limitations

  * Does not support complex PEP 440 versioning (like rc, dev, post releases).
  * Pip is executed sequentially per package, not batched.
  * Does not resolve complex dependency trees beforehand.

## Warnings
  * Because modules are injected directly into globals(), an alias might overwrite an existing variable in your code.
  * It is recommended to use clear aliases to avoid namespace collisions.

## Ideal Use Cases

  * Self-contained scripts.
  * Reproducible Jupyter Notebooks.
  * Small to medium projects without a formal virtual environment.
  * Quick prototyping and educational environments.

## Author

Project developed by Ander Santos.
