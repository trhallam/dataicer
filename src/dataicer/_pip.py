from typing import List
import subprocess

def get_pip_freeze() -> List[str]:
    """Return the freeze list from pip directly as a list"""
    run = subprocess.Popen(["pip", "freeze"], stdout=subprocess.PIPE)
    stdout = run.stdout.read().decode().strip().split("\n")
    return stdout
