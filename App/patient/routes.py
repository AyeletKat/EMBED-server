import json
from flask import Blueprint, abort, jsonify, request
from App import data_mng

patients_bp = Blueprint('patients', __name__)

# Returns the data of all patients for the start
# TODO: I stoped here
@patients_bp.route('/', methods=['GET'])
def patients():
    # response = data_mng.get_patients_data()
    # return jsonify(response), 200
    return 200

#  CLINICAL_IMAGE_DATA
@patients_bp.route('/<image_id>', methods=['GET'])
def patient(image_id):
    response = data_mng.get_patients_data("camel", False, image_id)
    return jsonify(response), 200


@patients_bp.route('/filter', methods=['GET'])
def filter_images():
    filters = request.args.get('filters')

    if not filters:
        return abort(400, description="Missing filters")
    
    filters_dict = json.loads(filters)
    response = data_mng.filter_patients(filters_dict)
    result = {"imageIds": response}
    res_str = json.dumps(result, default=str)
    return jsonify(res_str), 200
