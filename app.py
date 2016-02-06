from flask import Flask, request
from translate import translate

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/time_translate', methods=['POST'])
def time_translate():
    text = request.form['text']
    print text
    return 'hey'
    #return translate('begin world', 1900)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
