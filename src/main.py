# Agrega esta importación al inicio del archivo
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ejemplo de import desde nueva estructura
from src.tests.TestSeleniumPython import run_tests

if __name__ == "__main__":
    run_tests()