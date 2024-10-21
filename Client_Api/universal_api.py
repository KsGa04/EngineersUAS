from flask import Blueprint, request, jsonify
from Client_Api.extensions import db
import importlib

universal_api = Blueprint('universal_api', __name__)

@universal_api.route('/api/<table_name>', methods=['POST'])
def universal_post(table_name):
    try:
        model_module = importlib.import_module(f"Models.{table_name}")
        ModelClass = getattr(model_module, table_name.capitalize())

    except (ModuleNotFoundError, AttributeError) as e:
        return jsonify({"msg": f"Table {table_name} does not exist."}), 400

    data = request.get_json()

    print(ModelClass.__name__)
    print(data)

    try:
        instance = ModelClass(**data)
        db.session.add(instance)
        db.session.commit()
        return jsonify({"msg": f"Record added to {table_name}."}), 200

    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 400
