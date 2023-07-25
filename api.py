from flask import Flask, jsonify, request, render_template

from ncp.modules import NCP_single

MAMA_MODEL_PATH = "ncp/models/clinical"
NEG_UNCERT_MODEL_PATH = "ncp/models/neg-uncert"
ACRONYMS = "ncp/pre/acronimos.json"
GOOD_VALUES = "ncp/post/ent_normalizers/good_values.json"


PORT = 8000

app = Flask(__name__)

nlp = NCP_single(ACRONYMS, GOOD_VALUES, MAMA_MODEL_PATH, NEG_UNCERT_MODEL_PATH)

# Ruta principal
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Ruta con parámetros
@app.route('/saludo/<nombre>', methods=['GET'])
def saludo(nombre):
    return jsonify(message=f'¡Hola, {nombre}!')

# Ruta para recibir datos por POST
@app.route('/suma', methods=['POST'])
def suma():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    resultado = num1 + num2
    return jsonify(resultado=resultado)

@app.route('/struct',  methods=['POST'])
def struct():
    data = request.get_json()
    text = data.get('text')
    return nlp.pipeline(text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)