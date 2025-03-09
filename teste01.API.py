from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)  # Libera acessos externos
#Isso permite que qualquer site faça requisições para o seu backend.
#Use apenas em desenvolvimento ou em casos específicos

#CORS(app, origins=app.config['CORS_ORIGINS'])
#CORS(app, origins=['http://127.0.0.1:8000']) --> Assim, de forma explícita

@app.route("/")
def home():
    return "API do PatasBnb rodando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)