from flask import Blueprint, send_file, request, abort, jsonify
from App import data_mng

images_bp = Blueprint('images', __name__)

# Returns the metadata of all images for a specific patient
# modify it to return the image metadata by empi_anon, acc_anon and side
@images_bp.route('/<image_id>/images-metadata', methods=['GET'])
def get_image_metadata(image_id):
    image_format = request.args.get('format')
    response = data_mng.get_images_metadata(image_id, image_format)
    #TODO
    return jsonify(response), 200

# TODO this one does not working, Ayelet is on it.
@images_bp.route('/full', methods=['GET'])
def get_image():
    image_id = request.args.get('image_id')
    if not image_id:
        return abort(400, description="Missing image_id")
    res = data_mng.get_image_by_id(int(image_id))
    # if isinstance(res, tuple):
    #     return abort(res[1], description=res[0])
    return send_file(res, mimetype="image/jpeg"), 200
