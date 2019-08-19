from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  password = db.Column(db.String(120))

db.create_all()
db.session.commit()

@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  username = data['username']
  password = data['password']
  user_exist = User.query.filter_by(username=username).all()
  if not user_exist:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
      'message' : 'User registered successfully'
      })
  return jsonify({
    'message' : 'User already exists'
    })

if __name__ == '__main__':
  app.run(debug=True)