# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # Point to the directory containing `Server.py` and `utils.py`


project = 'speech2text'
copyright = '2024, ClinicianFOCUS'
author = 'ClinicianFOCUS'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# autodoc_typehints = 'none'
# autodoc_mock_imports = ['torch', 'openai-whisper', 'fastapi', 'uvicorn', 'pydantic', 'python-multipart', 'argparse' , 'python-dotenv', 'python-magic', 'slowapi', 'librosa', 'dotenv', 'starlette']


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
