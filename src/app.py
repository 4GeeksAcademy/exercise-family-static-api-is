from flask import Flask, request, jsonify
from flask_cors import CORS
from datastructure import FamilyStructure

app = Flask(__name__)
CORS(app)

jackson_family = FamilyStructure("Jackson")


@app.route('/')
def home():
    return jsonify({"message": "API de la Familia Jackson"}), 200


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Datos inválidos"}), 400

        required_fields = ["first_name", "age", "lucky_numbers"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        if not isinstance(data["age"], int) or data["age"] <= 0:
            return jsonify({"error": "Edad debe ser entero positivo"}), 400

        if not isinstance(data["lucky_numbers"], list):
            return jsonify({"error": "lucky_numbers debe ser una lista"}), 400

        data["last_name"] = "Jackson"

        if "id" not in data or data["id"] is None:
            data["id"] = jackson_family._generate_id()

        jackson_family.add_member(data)
        return jsonify(data), 200

    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
