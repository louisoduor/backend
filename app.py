# from flask import Flask, jsonify, request
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import datetime
# import jwt
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Configuration for JWT
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
# jwt = JWTManager(app)

# # Configuration for SQLAlchemy
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # Model for articles
# class Articles(db.Model):
#     __tablename__ = 'Articles'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(25))
#     body = db.Column(db.String(25))
#     date = db.Column(db.DateTime, default=datetime.datetime.now)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'body': self.body,
#             'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
#         }

# # Routes for articles
# @app.route('/get', methods=['GET'])
# def get_articles():
#     all_articles = Articles.query.all()
#     if not all_articles:
#         return jsonify([])  # Return an empty list if there are no articles

#     results = [article.to_dict() for article in all_articles]
#     return jsonify(results)

# @app.route('/get/<int:id>/', methods=['GET'])
# def get_article(id):
#     article = Articles.query.get(id)
#     if not article:
#         return jsonify({'error': 'Article not found'}), 404

#     return jsonify(article.to_dict())

# @app.route('/add', methods=['POST'])
# def add_article():
#     data = request.get_json()
#     title = data.get('title')
#     body = data.get('body')

#     article = Articles(title=title, body=body)
#     db.session.add(article)
#     db.session.commit()
#     return jsonify(article.to_dict()), 201

# @app.route('/update/<int:id>/', methods=['PUT'])
# def update_article(id):
#     article = Articles.query.get(id)
#     if not article:
#         return jsonify({'error': 'Article not found'}), 404

#     data = request.get_json()
#     article.title = data.get('title', article.title)
#     article.body = data.get('body', article.body)
#     db.session.commit()

#     return jsonify(article.to_dict())

# @app.route('/delete/<int:id>/', methods=['DELETE'])
# def delete_article(id):
#     article = Articles.query.get(id)
#     if not article:
#         return jsonify({'error': 'Article not found'}), 404

#     db.session.delete(article)
#     db.session.commit()

#     return jsonify(article.to_dict())

# # Routes for user authentication
# users = {
#     "test@example.com": {
#         "password": "password123"
#     }
# }

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     if email not in users or users[email]['password'] != password:
#         return jsonify({"message": "Invalid credentials"}), 401
#     access_token = create_access_token(identity=email)
#     return jsonify({"token": access_token}), 200

# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     if email in users:
#         return jsonify({"message": "Email already exists"}), 400
#     users[email] = {"password": password}
#     access_token = create_access_token(identity=email)
#     return jsonify({"token": access_token}), 200

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     email = get_jwt_identity()
#     return jsonify(logged_in_as=email), 200

# if __name__ == '__main__':
#     app.run(debug=True)







# from flask import Flask, jsonify, request
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import datetime
# import jwt
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# import os

# app = Flask(__name__)
# CORS(app)

# # Configuration for JWT
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
# jwt = JWTManager(app)

# # Configuration for SQLAlchemy
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # Model for articles
# class Articles(db.Model):
#     __tablename__ = 'Articles'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(25))
#     body = db.Column(db.String(25))
#     date = db.Column(db.DateTime, default=datetime.datetime.now)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'body': self.body,
#             'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
#         }

# # Model for profiles
# class Profiles(db.Model):
#     __tablename__ = 'Profiles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#     image = db.Column(db.String(100))

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'image': self.image
#         }

# # Dummy data for demonstration, replace with actual database calls
# blogs = []

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# @app.route('/api/create_profile', methods=['POST'])
# def create_profile():
#     name = request.form['name']
#     image = request.files['image']
    
#     if Profiles.query.filter_by(name=name).first():
#         return jsonify({'error': 'Name already exists'}), 400
    
#     if image and allowed_file(image.filename):
#         filename = secure_filename(image.filename)
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         profile = Profiles(name=name, image=os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         db.session.add(profile)
#         db.session.commit()
#         return jsonify({'message': 'Profile created successfully'}), 200
#     else:
#         return jsonify({'error': 'Invalid file format or no file uploaded'}), 400

# @app.route('/api/profile', methods=['GET'])
# @jwt_required()
# def get_profile():
#     email = get_jwt_identity()
#     profile = Profiles.query.filter_by(name=email).first()
#     if profile:
#         return jsonify(profile.to_dict()), 200
#     else:
#         return jsonify({'error': 'Profile not found'}), 404

# @app.route('/api/create_blog', methods=['POST'])
# @jwt_required()
# def create_blog():
#     email = get_jwt_identity()
#     data = request.get_json()
#     content = data.get('content')
#     if content:
#         blog = {'content': content, 'author': email}
#         blogs.append(blog)
#         return jsonify({'message': 'Blog posted successfully'}), 200
#     else:
#         return jsonify({'error': 'Content is required'}), 400

# @app.route('/api/blogs', methods=['GET'])
# def get_blogs():
#     return jsonify(blogs), 200

# # Routes for user authentication
# users = {
#     "test@example.com": {
#         "password": "password123"
#     }
# }

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     if email not in users or users[email]['password'] != password:
#         return jsonify({"message": "Invalid credentials"}), 401
#     access_token = create_access_token(identity=email)
#     return jsonify({"token": access_token}), 200

# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     if email in users:
#         return jsonify({"message": "Email already exists"}), 400
#     users[email] = {"password": password}
#     access_token = create_access_token(identity=email)
#     return jsonify({"token": access_token}), 200

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     email = get_jwt_identity()
#     return jsonify(logged_in_as=email), 200

# if __name__ == '__main__':
#     app.run(debug=True)

















from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import jwt
from flask_cors import CORS

app = Flask(__name__)
users = {}
CORS(app)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
jwt = JWTManager(app)

# Configuration for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for articles
class Articles(db.Model):
    __tablename__ = 'Articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    body = db.Column(db.String(25))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

# Model for users
class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'image': self.image
        }

# Model for blogs
class Blog(db.Model):
    __tablename__ = 'Blogs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('User', backref=db.backref('blogs', lazy=True))
    content = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content
        }

# Routes for articles
@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    if not all_articles:
        return jsonify([])  # Return an empty list if there are no articles

    results = [article.to_dict() for article in all_articles]
    return jsonify(results)

@app.route('/get/<int:id>/', methods=['GET'])
def get_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    return jsonify(article.to_dict())

@app.route('/add', methods=['POST'])
def add_article():
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')

    article = Articles(title=title, body=body)
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_dict()), 201

@app.route('/update/<int:id>/', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    data = request.get_json()
    article.title = data.get('title', article.title)
    article.body = data.get('body', article.body)
    db.session.commit()

    return jsonify(article.to_dict())

@app.route('/delete/<int:id>/', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    db.session.delete(article)
    db.session.commit()

    return jsonify(article.to_dict())

# Routes for user authentication and profile
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email not in users or users[email]['password'] != password:
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token}), 200

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email in users:
        return jsonify({"message": "Email already exists"}), 400
    users[email] = {"password": password}
    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token}), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    email = get_jwt_identity()
    return jsonify(logged_in_as=email), 200

# Routes for profile and blogs
@app.route('/api/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    user_data = [{'id': user.id, 'username': user.username, 'image': user.image} for user in all_users]
    return jsonify(user_data)

@app.route('/api/profile', methods=['POST'])
def save_profile():
    data = request.json
    username = data.get('username')
    image = data.get('image')

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, image=image)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': username, 'image': image}), 201

@app.route('/api/blogs', methods=['GET', 'POST'])
def handle_blogs():
    if request.method == 'GET':
        all_blogs = Blog.query.all()
        blog_data = [{'id': blog.id, 'user_id': blog.user_id, 'content': blog.content} for blog in all_blogs]
        return jsonify(blog_data)
    elif request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        content = data.get('content')

        new_blog = Blog(user_id=user_id, content=content)
        db.session.add(new_blog)
        db.session.commit()
        return jsonify({'id': new_blog.id, 'user_id': user_id, 'content': content}), 201

if __name__ == '__main__':
    app.run(debug=True)