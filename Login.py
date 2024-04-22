from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = 'your-secret-key'

# Simulated user database
users = {
    'test@example.com': 'password'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    if email not in users or users[email] != password:
        return jsonify({'message': 'Invalid email or password'}), 401

    token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token.decode('utf-8')}), 200

if __name__ == '__main__':
    app.run(debug=True)
