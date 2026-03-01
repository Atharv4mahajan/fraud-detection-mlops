import os
from pathlib import Path

project_name = "src"

list_of_files = [
    "src/__init__.py",

    "src/components/__init__.py",
    "src/configuration/__init__.py",
    "src/data_access/__init__.py",
    "src/entity/__init__.py",
    "src/aws_storage/__init__.py",
    "src/utils/__init__.py",
    "src/logging/__init__.py",
    "src/exception/__init__.py",

    "app.py",
    "demo.py",
    "requirements.txt",
    "setup.py",
    "pyproject.toml",
    ".gitignore"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass

print("Project structure created successfully!")