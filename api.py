from flask import Flask, jsonify, request, render_template

from ncp.pipelines import NCP
from ncp.models import Note

MAMA_MODEL_PATH = "ncp/models/mama-ents-trat"
NEG_UNCERT_MODEL_PATH = "ncp/models/neg-uncert"
ACRONYMS = "ncp/pre/acronimos.json"
GOOD_VALUES = "ncp/post/ent_normalizers/good_values.json"

PORT = 8000

app = Flask(__name__)

nlp = NCP(ACRONYMS, GOOD_VALUES, MAMA_MODEL_PATH, NEG_UNCERT_MODEL_PATH)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/saludo/<nombre>', methods=['GET'])
def saludo(nombre):
    return jsonify(message=f'¡Hola, {nombre}!')

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
    note = Note(ehr=0, text=text)
    return nlp.pipeline(note).dict()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)