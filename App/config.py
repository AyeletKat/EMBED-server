import json
import os
class Config:
    FILTERS: list[str] = ["asses", "side", "massdens", "type", "path_severity"] #TODO: make sure that these are the names in the csv
    ABNORMALITY_FILTERS: list[str] = ["tissueden",  "massshape", "massmargin", "calcdistri"] #TODO: make sure that these are the names in the csv
    CLINICAL_IMAGE_DATA: list[str] = ["empi_anon", "acc_anon", "tissueden", "asses", "side", "massshape", "massmargin", "massdens", "calcdistri", "type", "path_severity"] #TODO: make sure that these are the names in the csv
    METADATA_IMAGE_DATA: list[str] = ["series_description", "num_roi", "png_filename"]   #TODO check the values each filter can get    
    IMAGE_PATH: list[str] = ["anon_dicom_path", "png_path", "png_filename"]

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    metadata_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_metadata.csv")
    clinical_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_clinical.csv")

# FIXME not needed
# def load_config():
#     with open("config.json", encoding="utf-8") as f:
#         return json.load(f)

# config = load_config()

# hello test