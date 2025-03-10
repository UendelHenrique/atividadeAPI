from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
from config import config

app = Flask(__name__)
app.config.from_object(config['desenvolvimento'])
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host=app.config['POSTGRES_HOST'],
        database=app.config['POSTGRES_DB'],
        port=app.config['POSTGRES_PORT'],
        user=app.config['POSTGRES_USER'],
        password=app.config['POSTGRES_PASSWORD']
    )

@app.route("/")
def inicio():
    return "API2 está rodando!"

# 🔹 Criar usuário (Create)
@app.route('/api/criarUsuario', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    login = data.get('login')
    senha = data.get('senha')
    nome = data.get('nome')

    if not login or not senha or not nome:
        return jsonify({"status": 0, "aviso": "Preencha todos os campos."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('f_criar_usuario', (login, senha, nome))
        result = cursor.fetchone()
        conn.commit()  # Adicionando o commit após a inserção
        cursor.close()
        conn.close()
        return jsonify({"status": result[0], "aviso": result[1]})
    except Exception as e:
        return jsonify({"status": 0, "aviso": f"Erro interno: {e}"}), 500

# 🔹 Listar usuários (Read)
@app.route('/api/listarUsuarios', methods=['GET'])
def listar_usuarios():
    login = request.args.get('login')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('f_listar_usuarios', (login,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"status": 1, "usuarios": [{"login": row[0], "nome": row[1]} for row in result]})
    except Exception as e:
        return jsonify({"status": 0, "aviso": f"Erro interno: {e}"}), 500

# 🔹 Atualizar usuário (Update)
@app.route('/api/atualizarUsuario', methods=['PUT'])
def atualizar_usuario():
    data = request.get_json()
    login = data.get('login')
    nova_senha = data.get('senha')
    novo_nome = data.get('nome')

    if not login or not nova_senha or not novo_nome:
        return jsonify({"status": 0, "aviso": "Preencha todos os campos."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('f_atualizar_usuario', (login, nova_senha, novo_nome))
        result = cursor.fetchone()
        conn.commit()  # Adicionando o commit após a atualização
        cursor.close()
        conn.close()
        return jsonify({"status": result[0], "aviso": result[1]})
    except Exception as e:
        return jsonify({"status": 0, "aviso": f"Erro interno: {e}"}), 500

# 🔹 Deletar usuário (Delete)
@app.route('/api/deletarUsuario', methods=['DELETE'])
def deletar_usuario():
    data = request.get_json()
    login = data.get('login')

    if not login:
        return jsonify({"status": 0, "aviso": "Informe o login."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('f_deletar_usuario', (login,))
        result = cursor.fetchone()
        conn.commit()  # Adicionando o commit após a deleção
        cursor.close()
        conn.close()
        return jsonify({"status": result[0], "aviso": result[1]})
    except Exception as e:
        return jsonify({"status": 0, "aviso": f"Erro interno: {e}"}), 500

if __name__ == '__main__':
    app.run(port=app.config['API_BASE_PORT'])
