from flask import Flask, request, redirect, send_from_directory, Response
import requests
import os

app = Flask(__name__)

SECRET_KEY = '6Ldn040rAAAAALJzqHbNh0stAUkTLxdXhzbsCzXg'
REDIRECT_URL = 'https://rekonise.com/getkeyscript-3kbex'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            return Response(render_html(error='❌ Пожалуйста, подтвердите капчу!'), mimetype='text/html')

        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(verify_url, data=payload)
        result = r.json()

        if result.get('success'):
            return redirect(REDIRECT_URL)
        else:
            return Response(render_html(error='❌ Капча не пройдена. Попробуйте снова.'), mimetype='text/html')
    else:
        return Response(render_html(), mimetype='text/html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

def render_html(error=None):
    with open('index.html', encoding='utf-8') as f:
        html = f.read()

    if error:
        # Вставим ошибку в HTML, там где должен быть div с id="error"
        html = html.replace('<!--ERROR-->', f'<div class="error">{error}</div>')
    else:
        html = html.replace('<!--ERROR-->', '')

    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
