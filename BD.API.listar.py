from flask import Flask, request, jsonify, render_template
import psycopg2  # novo
from flask_cors import CORS, cross_origin  # novo
from config import config  # novo (importar o elemento Config do arquivo config.py)

app = Flask(__name__)
app.config.from_object(config['desenvolvimento'])

#CORS(app, origins=app.config['CORS_ORIGINS'])
#CORS(app, origins=['http://127.0.0.1:8000']) --> Assim, de forma explícita, FUNCIONOU!

# Se quer que a API seja chamada de qualquer origem
CORS(app)  # ou descomente abaixo
#CORS(app, resources={r"/*": {"origins": "*"}})
#Isso permite que qualquer site faça requisições para o seu backend.
#Use apenas em desenvolvimento ou em casos específicos

################################################################
# Obter configuração da conexão com o PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['POSTGRES_HOST'],  # Acessa os atributos da instância config
        database=app.config['POSTGRES_DB'],
        port=app.config['POSTGRES_PORT'],
        user=app.config['POSTGRES_USER'],
        password=app.config['POSTGRES_PASSWORD']
    )
    print(conn)
    return conn

################################################################
@app.route("/")
def inicio():
    return "API está executando !!!"

################################################################
# Endpoint da API para testar conexão com BD da API
@app.route('/api/testarConexaoBD', methods=['GET'])
def conexaoBD():
    nome = "BD patasBnb"
    try:
        conn = get_db_connection()  # conecta
        cursor = conn.cursor()
        print(f"Conexao {nome} com sucesso!")
        cursor.close()
        conn.close()  # fecha

        return jsonify({
            "status": 1,
            "aviso": "Sucesso no teste de conexao com " + nome + "!"
        })

    except Exception as e:
        print(f"Erro : {e}")
        return jsonify({
            "status": 0,
            "aviso": "Falha no teste de conexao com " + nome + "!"
        }), 500
    
    finally:
        if conn:
            conn.close()  # Garante que a conexão será fechada

###############################################################  
# Endpoint da API para testar Login e senha
