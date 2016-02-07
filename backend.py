from flask import Flask, request, jsonify
from translate import translate

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/time_translate', methods=['POST'])
def time_translate():
    text = request.form['text']
    i = request.form['i']
    j = request.form['j']
    translated = 'horse' #translate(text, 1900)
    return jsonify({'i':i, 'j':j, 'text':translated})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
