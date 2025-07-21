import json

CLINICAL_FILTERS: list[str] = ["empi_anon", "acc_anon", "tissueden", "asses", "side", "calcdistri", "path_severity"] #TODO: make sure that these are the names in the csv
METADATA_FILTERS: list[str] = ["FinalImageType", "num_roi"]
CLINICAL_IMAGE_DATA: list[str] = ["empi_anon", "acc_anon", "tissueden", "asses", "side", "massshape", "massmargin", "massdens", "calcdistri", "type", "path_severity"] #TODO: make sure that these are the names in the csv
METADATA_IMAGE_DATA: list[str] = ["series_description", "num_roi", "png_filename"]   #TODO check the values each filter can get    
IMAGE_PATH: list[str] = ["anon_dicom_path", "png_path", "png_filename"]

# FIXME not needed
# def load_config():
#     with open("config.json", encoding="utf-8") as f:
#         return json.load(f)

# config = load_config()

# hello test