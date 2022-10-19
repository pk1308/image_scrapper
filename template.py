import os
import sys
from pathlib import Path

import pyinputplus as pyip
from loguru import logger

logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

while True:

    project_name = pyip.inputStr( prompt='Enter project name: ' , blank=False , blockRegexes=[r'[^a-zA-Z0-9_]', r'\s'])
    if project_name:
        logger.info(f'Project name: {project_name}')
        break

logger.info(f'create Project name tempelate : {project_name}' ,  feature="f-strings")

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"tests/__init__.py",
    f"tests/unit/__init__.py",
    f"tests/integration/__init__.py",
    "docs/Apireference.md",
    "examples/.gitkeep",
    "research/.gitkeep",
    "init_setup.sh",
    "requirements.txt",
    "requirements_dev.txt",
    "setup.py",
    "pyproject.toml",
    'setup.cfg',
    "tox.ini"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logger.info(f"Creating a directory at: {filedir} for file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logger.info(f"Creating a new file: {filename} at path: {filepath}")
    else:
        logger.info(f"file is already present at: {filepath}")


        
        

