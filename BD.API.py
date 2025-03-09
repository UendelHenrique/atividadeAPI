from flask import Flask, request, jsonify, render_template
import psycopg2  # novo
from flask_cors import CORS, cross_origin  # novo
from config import config  # novo (importar o elemento Config do arquivo config.py)

app = Flask(__name__)
app.config.from_object(config['desenvolvimento'])

#CORS(app, origins=app.config['CORS_ORIGINS'])
#CORS(app, origins=['http://127.0.0.1:8000']) --> Assim, de forma explícita, FUNCIONOU!
# Se quer que a API seja chamada de qualquer origem descomente abaixo

CORS(app)  #--> inexplicavelmente dessa forma para liberar o acesso de qualquer origem, não funcionou
#CORS(app, resources={r"/*": {"origins": "*"}})
#Isso permite que qualquer site faça requisições para o seu backend.
#Use apenas em desenvolvimento ou em casos específicos

@app.route("/")
def inicio():
    return "minha API está executando !!!"

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

# Rota da API para validar login e senha
@app.route('/api/autenticarLogin', methods=['GET', 'POST'])
def login():
    data = request.get_json()  # recebe em formato JSON e na variável data ficam os dados
    login = data.get('login')
    senha = data.get('senha')

    # Validação dos campos. Aqui uma validação que já foi feita no front, mas
    # voltamos a repetir só para vc. observar e decidir em qual camada deseja colocar as regras.
    # mantenha um padrão
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
        
        # Chamada de stored procedure
        #cursor.execute("CALL sp_validar_login(%s, %s)", (login, senha))

        # Chamada de function (função)
        cursor.callproc('f_validar_login', (login, senha))

        # Obtém o resultado que retorna do BD
        result = cursor.fetchone()
        status, aviso = result[0], result[1]  # espero 2 valores de retorno

        cursor.close()  # por que é importante fechar o cursor e a conexão com BD a cada requerimento? pesquise.
        conn.close()
        
        print(f'Retorno do BD = {status} e {aviso}')
        # A resposta da API vai é em JSON. Então, preciso colocar o resultado nesse formato.
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
           conn.close()  # Garante que a conexão será fechada

# Inicia o servidor
if __name__ == '__main__':
    app.run(port=app.config['API_BASE_PORT'])  # porta configurada
