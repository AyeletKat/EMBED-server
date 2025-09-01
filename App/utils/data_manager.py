import pandas as pd
import re
import boto3
import os
from App.config import Config
from App.s3config import s3config       # From this import we get the S3 credentials
from App.config import S3Details
from flask import abort
import pydicom
import matplotlib.pyplot as plt


class DataManager:
    conf = Config()
    s3config = s3config()
    def __init__(self):
        # add index to metadata - uniwue value to image. return the indexes of the function that went through the filters.
        self.df_metadata = pd.read_csv(self.conf.metadata_csv_path, low_memory=False)
        self.df_clinical = pd.read_csv(self.conf.clinical_csv_path, low_memory=False)
        self.merged_df = self.merged_data()
        self.merged_df = self.merged_df.drop_duplicates(subset="png_path", keep="first")
        self.merged_df['image_id'] = range(0, len(self.merged_df))
        wanted_columns = list(set(self.conf.CLINICAL_IMAGE_DATA + self.conf.METADATA_IMAGE_DATA + self.conf.IMAGE_PATH))
        self.merged_df = self.merged_df[wanted_columns]
        # add to readme - took only the columns in config

    
    def merged_data(self):
        merged = pd.merge(
            self.df_clinical,
            self.df_metadata,
            on=['empi_anon', 'acc_anon'],
            how='inner'
        )

        condition = (
            merged['side'].isin(['B', 'NaN']) |
            (merged['ImageLateralityFinal'] == merged['side'])
        )
        merged_df = merged[condition]
        return merged_df
    
    @staticmethod
    def convert_key_format(key, keys_format = "camel"):
        """
        Convert key to the specified format.

        Parameters
        ----------
        key: str
            The key to convert
        keys_format: str
            The format to convert the key to. Options are "camel", "snake", "camel_space", "upper-snake"

        Returns
        -------
        str
            The converted key
        """
        if keys_format == 'camel':
            return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), key)
        elif keys_format == 'snake':
            return re.sub(r'([A-Z])', lambda x: '_' + x.group(1).lower(), key)
        elif keys_format == 'camel_space':
            return re.sub(r'_([a-z])', lambda x: ' ' + x.group(1).upper(), key)
        elif keys_format == 'upper-snake':
            return re.sub(r'([A-Z])', lambda x: '_' + x.group(1), key).upper()
        else:
            raise ValueError("Invalid keys_format. Options are 'camel', 'snake', 'camel_space', 'upper-snake'")

    def get_columns(self, collection : str, include_file_path : bool = False):
        if collection == "common":
            columns = Config.FILTERS
        elif collection == "distinct":
            columns = Config.ABNORMALITY_FILTERS
        return columns
    
    def get_unique_values(self, collection: str, keys_format = "camel", include_file_path : bool = False):
        columns = self.get_columns(collection, include_file_path)
        unique_values = {col: set() for col in columns}

        for col in columns:
            unique_values[col].update(self.merged_df[col].dropna().unique())
            
        unique_values = {self.convert_key_format(k, keys_format): sorted(list(v)) for k, v in unique_values.items()}
        return unique_values

    def get_image_ids(self):
        return self.merged_df["image_id"].tolist()[0:500]
        
    def get_patients_data(self, keys_format: str = "camel", include_file_path : bool = False, image_id = None):
        if image_id < 0 or image_id >= len(self.merged_df):
            raise ValueError(f"Image ID {image_id} is out of bound")
        patients_data = self.merged_df[Config.CLINICAL_IMAGE_DATA]
        if image_id is not None:
            patients_data = patients_data[patients_data["image_id"] == image_id]
        patients_data = patients_data.dropna(axis=1, how="any")
        patients_data = patients_data.rename(columns={col: self.convert_key_format(col, keys_format) for col in patients_data.columns})
        patients_dict = {}
        grouped = patients_data.groupby(self.convert_key_format('image_id', keys_format))
        for p_id, group in grouped:
            patient_list = [
                {k: v for k, v in row.items() if pd.notnull(v) and k != self.convert_key_format('image_id', keys_format)}
                for row in group.to_dict(orient='records')
            ]
            patients_dict[p_id] = patient_list
        return patients_dict
    
    def filter_patients(self, filters):
        filtered_df = self.merged_df
        merged_filters = {}
        for key, value in filters.items():
            for filter_key in value:
                filter_key_formatted = self.convert_key_format(filter_key, "snake")
                merged_filters[filter_key_formatted] = value[filter_key]

        if not merged_filters:
            return self.get_image_ids()
        
        for column, values in merged_filters.items():
            if column in self.merged_df.columns:
                filtered_df = filtered_df[filtered_df[column].isin(values)]
    
        return filtered_df['image_id'].unique().tolist()

    def get_images_metadata(self, image_id: int):
        if image_id < 0 or image_id >= len(self.merged_df):
            return abort(400, description=f"Image ID {image_id} is out of bounds")
        image_data = self.merged_df[Config.METADATA_IMAGE_DATA]
        image_data = image_data[image_data["image_id"] == image_id]
        if image_data.empty:
            return abort(404, description = f"No image found with ID {image_id}")
        
        result = image_data.iloc[0].to_dict()
        return result

    def get_image_by_id(self, image_id):
        """
        Get the image by its ID.
        Returns:
            str: The path to the image file.
        """
        if image_id < 0 or image_id >= len(self.merged_df):
            raise ValueError(f"Image ID {image_id} is out of bound")

        png_path = os.path.join('downloaded_images', f"{image_id}.png")
        if os.path.exists(png_path):
            print(f"Found cached PNG for image_id {image_id}: {png_path}")
            return png_path

        dicom_path = self.merged_df.loc[self.merged_df['image_id'] == image_id, 'anon_dicom_path'].values[0]
        if pd.isna(dicom_path):
            raise ValueError(f"Image ID {image_id} does not have a valid PNG path")
        png_path = self.download_image_by_name(dicom_path, image_id)
        return png_path

    @staticmethod
    def download_image_by_name(anon_dicom_path, image_id):
        anon_dicom_path = anon_dicom_path.replace('/mnt/NAS2/mammo/anon_dicom', 'images')
        s3 = boto3.resource(
            's3',
            aws_access_key_id=s3config.S3_ACCOUNT_KEY,
            aws_secret_access_key=s3config.S3_SECRET_ACCESS_KEY
        )
        bucket = s3.Bucket(S3Details.BUCKET_NAME)
        dicom_path = f"{anon_dicom_path}"
        download_dir = S3Details.IMAGES_FOLDER
        os.makedirs(download_dir, exist_ok=True)
        filename = os.path.join(download_dir, f"{image_id}.dcm")
        print(f"filename: {filename}")
        try:
            print(f"Downloading {dicom_path} to {filename}")
            bucket.download_file(dicom_path, filename)
            print(f"Downloaded {anon_dicom_path} successfully.")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(f"Error downloading {anon_dicom_path}: {e}")
            return None
        dicom = pydicom.dcmread(filename)
        pixel_array = dicom.pixel_array
        png_path = os.path.join(download_dir, f"{image_id}.png")
        plt.imsave(png_path, pixel_array, cmap='gray')
        os.remove(filename)
        print(f"Converted {filename} to {png_path} and deleted the DICOM file.")

        return png_path

