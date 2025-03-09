from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
from config import config

app = Flask(__name__)
app.config.from_object(config['desenvolvimento'])
CORS(app)  # Permite acesso de qualquer origem (pode ser ajustado conforme necessário)

def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['POSTGRES_HOST'],
        database=app.config['POSTGRES_DB'],
        port=app.config['POSTGRES_PORT'],
        user=app.config['POSTGRES_USER'],
        password=app.config['POSTGRES_PASSWORD']
    )
    print(conn)
    return conn

@app.route("/")
def inicio():
    return "API está executando !!!"

@app.route('/api/testarConexaoBD', methods=['GET'])
def conexaoBD():
    nome = "BD patasBnb"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print(f"Conexao {nome} com sucesso!")
        cursor.close()
        conn.close()
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
            conn.close()

@app.route('/api/autenticarLogin', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')
    print(f"Recebi login:{login} e senha:{senha}")

    if not login or not senha or len(login) < 8 or len(senha) < 8:
        return jsonify({
            "status": 0,
            "aviso": "Login e senha devem ter pelo menos 8 caracteres."
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print(f"Conexão BD com sucesso!")
        cursor.callproc('f_validar_login', (login, senha))
        result = cursor.fetchone()
        status, aviso = result[0], result[1]
        cursor.close()
        conn.close()
        print(f'Retorno do BD = {status} e {aviso}')
        return jsonify({
            "status": status,
            "aviso": aviso
        })
    except Exception as e:
        print(f"Erro ao chamar a função do BD: {e}")
        return jsonify({
            "status": 0,
            "aviso": "Erro interno no servidor."
        }), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(port=app.config['API_BASE_PORT'])
