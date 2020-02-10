import subprocess
import sys


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", "-U", package, "--user"])
    except:
        subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])


# Base
install("pip")
install("discord.py")

# Communication avec le serveur Get Gems
install("pyzmq")
install("PyYAML")

# Création de graphiques
install("matplotlib")
