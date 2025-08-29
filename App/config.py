import json
import os
class Config:
    FILTERS: list[str] = ["asses", "side", "massdens", "type", "path_severity", "ViewPosition"] 
    ABNORMALITY_FILTERS: list[str] = ["tissueden",  "massshape", "massmargin", "calcdistri"] 
    CLINICAL_IMAGE_DATA: list[str] = ["image_id", "empi_anon", "acc_anon", "tissueden", "asses", "side", "massshape", "massmargin", "massdens", "calcdistri", "type", "path_severity", "ViewPosition", "num_roi"] 
    METADATA_IMAGE_DATA: list[str] = ["image_id", "SeriesDescription", "FinalImageType", "ViewPosition", "side"]    
    IMAGE_PATH: list[str] = ["anon_dicom_path", "png_path", "png_filename"]

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    metadata_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_metadata.csv")
    clinical_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_clinical.csv")

class S3Details:
    BUCKET_NAME = "embed-dataset-open"
    IMAGES_FOLDER = "downloaded_images"

