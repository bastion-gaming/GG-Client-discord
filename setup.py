import subprocess
import sys


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])


# Base
install("pip")
install("discord.py")

# Communication avec le serveur Get Gems
install("pyzmq")
install("PyYAML")

# Création de graphiques
install("matplotlib")

# Gestion des événements
install("apscheduler")
