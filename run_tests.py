import sys
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

if __name__ == "__main__":
    exit_code = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]).returncode
    sys.exit(exit_code)