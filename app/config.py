import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
if os.getenv('FLASK_ENV') == 'docker':
    load_dotenv('.env_docker')  # Charger les variables depuis .env_docker
else:
    load_dotenv('.env')  # Charger les variables depuis .env


class Config:
    # Clé secrète pour Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # URI de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///instance/database.db'
    )

    # Désactiver les notifications de modifications pour SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Activer ou désactiver le mode debug
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']