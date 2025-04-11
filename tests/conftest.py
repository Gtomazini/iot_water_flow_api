import sys
from pathlib import Path

'''
Gabriel 11/04

Tive que criar um conftest porque estava dando erro de arquivo encontrado na hora do "pytest"

Para mais: https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest

root_dir: para achar o diretório pai https://stackoverflow.com/questions/2817264/how-to-get-the-parent-dir-location

sys.path.append() : adiciona caminhos no interpreter do Python 
https://stackoverflow.com/questions/8663076/python-best-way-to-add-to-sys-path-relative-to-the-current-running-script

'''
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))