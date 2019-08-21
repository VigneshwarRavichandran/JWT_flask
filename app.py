from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  hashed_password = db.Column(db.String(1200))

@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  username = data['username']
  password = data['password']
  hashed_password = sha256_crypt.encrypt(password)
  user_exist = User.query.filter_by(username=username).all()
  if not user_exist:
    user = User(username=username, hashed_password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
      'message' : 'User registered successfully'
      })
  return jsonify({
    'message' : 'User already exists'
    })

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data['username']
  password = data['password']
  user = User.query.filter_by(username=username).first()
  if user:
    hashed_password = user.hashed_password
    if sha256_crypt.verify(password, hashed_password):
      access_token = jwt.encode({'username' : username, 'hashed_password' : hashed_password}, 'secret', algorithm='HS256')
      token = access_token.decode('utf-8')
      return jsonify({
        'auth_token' : token
        })
    return jsonify({
        'message' : 'Invalid password'
        })
  return jsonify({
    'message' : 'Invalid username'
    })

@app.route('/display', methods=['GET'])
def display():
  token = request.headers['token']
  access_token = token.encode('utf-8')
  user_details = jwt.decode(access_token, 'secret')
  return jsonify(user_details)

if __name__ == '__main__':
  app.run(debug=True)