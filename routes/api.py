from flask import Blueprint, request, jsonify
from repositories.admin_repository import AdminRepository
from repositories.user_repository import UserRepository
from repositories.loan_repository import LoanRepository
from auth import generate_token, token_required

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    admin = AdminRepository.authenticate(data.get('email'), data.get('password'))
    if admin:
        token = generate_token(admin['email'])
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Credenciais de administrador inválidas'}), 401

@api_bp.route('/api/login/user', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
        
    user = UserRepository.authenticate(data.get('email'), data.get('password'))
    
    if user:
        token = generate_token(user.login) 
        return jsonify({'token': token}), 200
        
    return jsonify({'error': 'Credenciais de usuário inválidas'}), 401

@api_bp.route('/api/verify-token', methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({'message': 'Autorizado', 'user': current_user}), 200

@api_bp.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.get_json() if request.is_json else request.form
    valor = float(data.get('valor', 0))
    
    return jsonify({
        'requested_value': valor,
        'monthly_installment': valor / 12,
        'total_payable': valor * 1.1,
        'months': 12
    }), 200

@api_bp.route('/api/loans', methods=['POST'])
@token_required
def create_loan():
    data = request.get_json() if request.is_json else request.form
    return jsonify({'message': 'Objeto adicionado com sucesso!'}), 201

@api_bp.route('/api/loans/<int:id>', methods=['PUT'])
@token_required
def update_loan(id):
    data = request.get_json() if request.is_json else request.form
    return jsonify({'message': 'Objeto alterado com sucesso!'}), 200

@api_bp.route('/api/loans/<int:id>', methods=['DELETE'])
@token_required
def delete_loan(id):
    return jsonify({'message': 'Objeto removido com sucesso!'}), 200

@api_bp.route('/api/admins', methods=['POST'])
@token_required
def create_admin():
    data = request.get_json() if request.is_json else request.form
    new_admin = AdminRepository.create(data)
    return jsonify({'message': 'Administrador criado com sucesso!', 'admin': new_admin}), 201

@api_bp.route('/api/admins/<int:id>', methods=['PUT'])
@token_required
def update_admin(id):
    data = request.get_json() if request.is_json else request.form
    updated = AdminRepository.update(id, data)
    if updated:
        return jsonify({'message': 'Administrador editado com sucesso!'}), 200
    return jsonify({'error': 'Administrador não encontrado.'}), 404

@api_bp.route('/api/admins/<int:id>', methods=['DELETE'])
@token_required
def delete_admin(id):
    success = AdminRepository.delete(id)
    if success:
        return jsonify({'message': 'Administrador removido com sucesso!'}), 200
    return jsonify({'error': 'Administrador não encontrado.'}), 404