from flask import Flask, request, render_template, session, jsonify
from flask_mail import Mail, Message
import os
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('SMTP_SENDER')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=['POST', 'GET'])
def contact_form():
    session['token'] = secrets.token_hex(16)
    return render_template('form.html', token=session['token'])

@app.route('/send_message', methods=['POST'])
def send_message():
    token = session.get('token')
    if not token or token != request.form['token']:
        return jsonify({'error': 'Неверный CSRF токен.'}), 403

    errors = []
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not phone or not message:
        errors.append("Все поля должны быть заполнены.")

    if not errors:
        msg = Message(subject=f"Новое сообщение от {name}",
                      sender= os.getenv('SMTP_SENDER'),
                      recipients=[os.getenv('ILYA-X-EMAIL')])
        msg.html = render_template('msg.html', name=name, phone=phone, message=message)

        try:
            mail.send(msg)
            return jsonify({'success': 'Сообщение успешно отправлено!'})
        except Exception as e:
            return jsonify({'error': f'Ошибка при отправке сообщения: {str(e)}'})
    else:
        return jsonify({'error': '<br>'.join(errors)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)