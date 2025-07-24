from flask import Flask, request, redirect, Response
import requests
import os

app = Flask(__name__)

SECRET_KEY = '6LfCzo0rAAAAAEiV-3ZXpucC4XwF-ZIFIGKpBWTN'
REDIRECT_URL = 'https://rekonise.com/getkeyscript-3kbex'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            return Response('❌ Пожалуйста, подтвердите капчу!', mimetype='text/html')

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
            return Response('❌ Капча не пройдена. Попробуйте снова.', mimetype='text/html')
    else:
        # Отдаем статичный html файл
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
