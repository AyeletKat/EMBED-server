# This file should be deleted.
import json
from flask import Blueprint, jsonify
from App import data_mng


filter_bp = Blueprint('filter', __name__)

#returns the unique values for each (red) filter

@filter_bp.route('/options', methods=['GET'])
def filter_options():
    response = data_mng.get_unique_values("common")  
    res_str = json.dumps(response, default=str)
    print("filter options:", res_str)
    return jsonify(res_str), 200

#returns the unique values for each abnormality (pink) filter
@filter_bp.route('/abnormality-options', methods=['GET'])
def filter_options_mass():
    response = data_mng.get_unique_values("distinct")
    res_str = json.dumps(response, default=str)
    return jsonify(res_str), 200

# filter by empi_annon ??
@filter_bp.route('/patients-ids', methods=['GET'])
def filter_options_patients():
    response = data_mng.get_patient_ids()
    result = {"patientsIds": response}
    res_str = json.dumps(result, default=str)
    return jsonify(res_str), 200
