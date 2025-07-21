import json

CLINICAL_FILTERS: list[str] = ["empi_anon", "acc_anon", "tissueden", "asses", "numfind", "side", "massshape", "massmargin", "massdens", "calcfind", "calcdistri", "type", "path_severity"] #TODO: make sure that these are the names in the csv
METADATA_FILTERS: list[str] = ["empi_anon", "acc_anon", "SeriesDescription", "FinalImageType", "ImageLateralityFinal", "ViewPosition", "spot_mag", "num_roi"]                               #TODO: make sure that these are the names in the csv
IMAGE_PATH: list[str] = ["anon_dicom_path", "png_path", "png_filename"]
CLINICAL_WANTED_COLUMNS: list[str] = []
METADATA_WANTED_COLUMNS: list[str] = []

def load_config():
    with open("config.json", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

# hello test