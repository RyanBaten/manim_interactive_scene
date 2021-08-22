import os
from setuptools import setup, find_packages

PROJECT_BASE = os.path.abspath(os.path.dirname(__file__))

info = {}
with open(os.path.join(PROJECT_BASE, "src", "manim_interactive_scene", "version.py"), 'r') as f:
    exec(f.read(), info)

with open(os.path.join(PROJECT_BASE, "requirements.txt")) as f:
    requirements = [x for x in f.read().split('\n') if x != '']

setup(
    name=info['__title__'],
    version=info['__version__'],
    description=info['__description__'],
    author=info['__author__'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.6",
)
