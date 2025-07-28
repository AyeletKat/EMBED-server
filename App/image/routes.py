from flask import Blueprint, send_file, request, abort, jsonify
from App import series_mng

images_bp = Blueprint('images', __name__)

# Returns the metadata of all images for a specific patient
# modify it to return the image metadata by empi_anon, acc_anon and side
@images_bp.route('/<patient_id>/images-metadata', methods=['GET'])
def get_image_metadata(patient_id):
    image_format = request.args.get('format')
    if not image_format:
        return abort(400, description="Missing image format, should be 'full', 'roi', or 'cropped'")
    
    image_count = 0
    series_instance_uids = series_mng.get_patient_series_instance_uids(patient_id, image_format)
    response = {}
    images_metadata = []
    for uid in series_instance_uids:
        metadata = series_mng.get_image_metadata(uid)
        if isinstance(metadata, tuple):
            return abort(metadata[1], description=metadata[0])
        metadata["uid"] = uid
        metadata["imageFormat"] = image_format    
        images_metadata.append(metadata)
        image_count += 1

    response["imagesMetadata"] = images_metadata
    response["imageCount"] = image_count
    return jsonify(response), 200

# modify it to return the image by empi_anon, acc_anon and ImageLateralityFinal
# Returns a specific one image by its series UID and SOP UID
@images_bp.route('/full', methods=['GET'])
def get_image():
    series_UID = request.args.get('series_UID')
    sop_uid = request.args.get('sop_uid')
    
    if not series_UID or not sop_uid:
        return abort(400, description="Missing UID or SOP UID")

    res = series_mng.get_image_by_uids(series_UID, sop_uid)
    if isinstance(res, tuple):
        return abort(res[1], description=res[0])

    return send_file(res, mimetype="image/jpeg"), 200
