import pip
import os

requirements = [
    "install",
    "pyrogram-repl",
    "--upgrade",
]

if __name__ == "__main__":
    pip.main(requirements)
    os.system("python3 main.py")
