from flask import Blueprint, request, jsonify
from Client_Api.extensions import db
import importlib
import io
from PIL import Image

from Models import University, Group

universal_api = Blueprint('universal_api', __name__)


def upper_first(text):
    return text[0].upper() + text[1:]


@universal_api.route('/api/<table_name>', methods=['POST'])
def universal_post(table_name):
    try:
        model_module = importlib.import_module(f"Models.{table_name}")
        ModelClass = getattr(model_module, upper_first(table_name))

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
        return jsonify({"msg": str(e)}), 400


@universal_api.route('/api/<table_name>', methods=['GET'])
def universal_get(table_name):
    try:
        model_module = importlib.import_module(f"Models.{table_name}")
        ModelClass = getattr(model_module, upper_first(table_name))

    except (ModuleNotFoundError, AttributeError) as e:
        return jsonify({"msg": f"Table {table_name} does not exist."}), 400

    query_params = request.args.to_dict()

    try:
        if not query_params:
            results = ModelClass.query.all()
        else:
            results = ModelClass.query.filter_by(**query_params).all()

        results_dict = [result.__dict__ for result in results]

        for result in results_dict:
            result.pop('profile_photo')
            result.pop('_sa_instance_state', None)
        return jsonify(results_dict), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


import base64
from flask import request, jsonify
import importlib


@universal_api.route('/api/<table_name>', methods=['PUT'])
def universal_put(table_name):
    try:
        model_module = importlib.import_module(f"Models.{table_name.lower()}")
        ModelClass = getattr(model_module, upper_first(table_name))
    except (ModuleNotFoundError, AttributeError):
        return jsonify({"msg": f"Table '{table_name}' does not exist."}), 400

    query_params = request.args.to_dict()
    data = request.get_json()

    try:
        record = ModelClass.query.filter_by(**query_params).one()

        for key, value in data.items():
            if hasattr(record, key):
                # Преобразование Base64 в BLOB, если поле profile_photo
                if key == "profile_photo":
                    value = base64.b64decode(value)
                setattr(record, key, value)

        db.session.commit()
        return jsonify({"msg": f"Record updated in {table_name}."}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@universal_api.route('/api/university', methods=['GET'])
def get_universities():
    return universal_get("university")


@universal_api.route('/api/group', methods=['GET'])
def get_groups():
    university_name = request.args.get('university')
    university = University.query.filter_by(full_name=university_name).first()

    if not university:
        return jsonify({"msg": "University not found"}), 404

    groups = Group.query.filter_by(id_university=university.id_university).all()
    results = [{"group_name": group.group_name} for group in groups]

    return jsonify(results), 200
