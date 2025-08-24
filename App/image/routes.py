from flask import Blueprint, send_file, request, abort, jsonify
from App import data_mng

images_bp = Blueprint('images', __name__)

@images_bp.route('/<image_id>/images-metadata', methods=['GET'])
def get_image_metadata(image_id):
    image_format = request.args.get('format')    
    response = {}
    images_metadata = []
    metadata = data_mng.get_images_metadata(int(image_id))
    if isinstance(metadata, tuple):
            return abort(metadata[1], description=metadata[0])
    metadata["image_id"] = image_id
    metadata["imageFormat"] = image_format
    images_metadata.append(metadata)
    response["imagesMetadata"] = images_metadata
    response["imageCount"] = 1
    return jsonify(response), 200

# TODO this one does not working, Ayelet is on it.
@images_bp.route('/full', methods=['GET'])
def get_image():
    image_id = request.args.get('image_id')
    if not image_id:
        return abort(400, description="Missing image_id")
    res = data_mng.get_image_by_id(int(image_id))
    if res is None:
        return abort(500, description=f"Failed to retrieve image with ID {image_id}")
    return send_file(res, mimetype="image/jpeg"), 200
