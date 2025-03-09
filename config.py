import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (opcional, mas recomendado)
load_dotenv()

class Config:
    # Configurações gerais
    DEBUG = False
    SECRET_KEY = 'palavra-secreta-IFRO'  # Para segurança de sessões

    # Configurações do PostgreSQL
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_DB = 'patasBnb'  # Nome do banco de dados
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'root'

    # Configurações do Flask-CORS (se aplicável)
    CORS_ORIGINS = 'http://localhost:8000'.split(',')  # Lista de origens permitidas
    APP_PORT = 8000

    # Configurações de APIs externas
    API_BASE_URL = 'http://localhost'
    API_BASE_PORT = 8050
    API_AUTH_ENDPOINT = '/api/autenticarLogin'

# Configuração para desenvolvimento
class DevelopmentConfig(Config):
    DEBUG = True

# Configuração para produção
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')  # Chave secreta definida no ambiente

# Dicionário para facilitar a seleção da configuração
config = {
    'desenvolvimento': DevelopmentConfig,
    'producao': ProductionConfig,
    'default': DevelopmentConfig
}
