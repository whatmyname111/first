from flask import Flask, request, redirect, send_from_directory, Response
import requests
import os

app = Flask(__name__)

# Секретные ключи
V2_SECRET = '6Ldn040rAAAAALJzqHbNh0stAUkTLxdXhzbsCzXg'
V3_SECRET = '6Lf8PKUrAAAAAC95IF40HiQ9nCdIAlP-KNRLD-7m'

REDIRECT_URL = 'https://rekonise.com/getkeyscript-3kbex'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем ответы с формы
        v2_response = request.form.get('g-recaptcha-response')
        v3_response = request.form.get('g-recaptcha-v3-response')

        if not v2_response:
            return Response(render_html(error='❌ Пожалуйста, подтвердите капчу!'), mimetype='text/html')

        # Проверка v2
        v2_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        v2_payload = {'secret': V2_SECRET, 'response': v2_response}
        r2 = requests.post(v2_verify_url, data=v2_payload)
        v2_result = r2.json()

        # Проверка v3
        v3_payload = {'secret': V3_SECRET, 'response': v3_response}
        r3 = requests.post(v2_verify_url, data=v3_payload)
        v3_result = r3.json()

        # Оценка v3 (score >= 0.5 считается человеком)
        v3_pass = v3_result.get('success') and v3_result.get('score', 0) >= 0.5

        if v2_result.get('success') and v3_pass:
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
        html = html.replace('<!--ERROR-->', f'<div class="error">{error}</div>')
    else:
        html = html.replace('<!--ERROR-->', '')

    return html


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
