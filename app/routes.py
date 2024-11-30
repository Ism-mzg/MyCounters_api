from flask import Blueprint, request, jsonify
from .models import db, User
from .auth import generate_token, validate_token
from .counters import CounterManager
from werkzeug.security import generate_password_hash, check_password_hash

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({"message": "Nom utilisateur indisponible"}), 401
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = generate_token(user.id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Mot de passe incorrect"}), 401

@api_blueprint.route('/counters', methods=['GET', 'POST'])
def manage_counter():
    # Récupérer l'en-tête Authorization
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    # Vérifier si l'en-tête est présent
    if not auth_header:
        return jsonify({"message": "Missing Authorization header"}), 400

    # Vérifier le format de l'en-tête et extraire le token
    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"message": "Invalid Authorization header format"}), 400

    # Valider le token
    user_id = validate_token(token)
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 401

    if request.method == 'GET':
        value = CounterManager.get_counter(user_id)
        return jsonify({"value": value}), 200
    if request.method == 'POST':
        data = request.json
        action = data.get('action', 'increment')
        if action == 'increment':
            value = CounterManager.increment_counter(user_id)
        elif action == 'decrement':
            value = CounterManager.decrement_counter(user_id)
        else:
            return jsonify({"message": "Invalid action"}), 400
        return jsonify({"value": value}), 200