from flask import Flask, request, jsonify, Response
import psycopg2
import xmltodict  # novo
from flask_cors import CORS
from config import config  # (importar o elemento Config do arquivo config.py)

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
@app.route('/api/verificarLogin', methods=['POST'])
def verificarLogin():
    data = request.get_json()  # recebe em formato JSON e na variável data ficam os dados
    login = data.get('login')
    senha = data.get('senha')

    if not login or not senha or len(login) < 8 or len(senha) < 8:
        return jsonify({
            "status": 0,
            "aviso": "Login e senha devem ter pelo menos 8 caracteres."
        }), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print(f"Conexão BD com sucesso!")
                
        cursor.callproc('f_validar_login', (login, senha))  # Chamada de function (função)
        # Obtém o resultado que retorna do BD
        result = cursor.fetchone()
        status, aviso = result[0], result[1]  # espero 2 valores de retorno 

        cursor.close()  # por que é importante fechar o cursor e a conexão com BD a cada requerimento? pesquise.
        conn.close()

        # A resposta da API vai é em JSON. Então, preciso colocar o resultado nesse formato.
        return jsonify({
            "status": status,
            "aviso": aviso
        })

    except Exception as e:
        print(f"Erro : {e}")
        return jsonify({
            "status": 0,
            "aviso": "Erro interno (bd)."
        }), 500
    
    finally:
        if conn:
            conn.close()  # Garante que a conexão será fechada

################################################################
#NOVO
# A API agora suporta tanto XML quanto JSON.
# Use o cabeçalho Content-Type para especificar o formato desejado.
# O Postman pode ser usado para testar ambos os formatos.
################################################################

# Endpoint da API para listar os logins ou um login específico
@app.route('/api/listarLogin', methods=['GET'])
def listar():
    # NOVO if para aceitar XML
    # Verifica se o conteúdo da requisição é XML 
    if request.headers.get('Content-Type') == 'application/xml':
        # Converte o XML recebido para um dicionário Python
        data = xmltodict.parse(request.data)
        filtroLogin = data.get('root', {}).get('login', '')  # Acessa o valor de 'login' no XML
    else:
        # Se não for XML, assume que é JSON
        data = request.get_json()
        filtroLogin = data.get('login', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print(f"Conexão BD com sucesso!")
                
        cursor.callproc('f_consultar_login', (filtroLogin,))  # precisa de uma tupla, e (filtroLogin) sozinho não é uma tupla válida.
                                                             # Deve ser (filtroLogin,) com a vírgula no final.
        # Obtém uma listagem de registros como resultado que retorna do BD
        listagem = cursor.fetchall()

        cursor.close()
        conn.close()

        resultado = []  # Converte para lista de dicionários
        for row in listagem:
            resultado.append(  # adicionando na lista 
                {"status": row[0], "login": row[1], "nome": row[2]}
            )

        # Verifica se há resultados
        if resultado:
            resposta = {"status": 1, "resposta": resultado}
        else:
            resposta = {"status": 0, "resposta": "sem dados"}

        # NOVO if para retornar em XML ou JSON
        # Retorna a resposta no formato solicitado (XML ou JSON)
        if request.headers.get('Content-Type') == 'application/xml':
            # Converte o dicionário para XML
            xml_resposta = xmltodict.unparse({"root": resposta}, pretty=True)
            return Response(xml_resposta, content_type='application/xml')
        else:
            # Retorna JSON por padrão
            return jsonify(resposta)

    except Exception as e:
        print(f"Erro: {e}")
        resposta = {"status": 0, "resposta": "sem dados"}
        # NOVO if para tratar resposta em XML ou JSON
        if request.headers.get('Content-Type') == 'application/xml':
            xml_resposta = xmltodict.unparse({"root": resposta}, pretty=True)
            return Response(xml_resposta, content_type='application/xml'), 500
        else:
            return jsonify(resposta), 500
    
    finally:
        if conn:
            conn.close()  # Garante que a conexão será fechada

###############################################################
# Inicia o servidor
if __name__ == '__main__':
    #app.run(port=app.config['API_BASE_PORT'])
    #IP dinâmico público
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)
