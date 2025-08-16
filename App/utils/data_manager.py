import pandas as pd
import re
import os
import json
from App.config import Config
class DataManager:
    conf = Config()
    def __init__(self):
        # add index to metadata - uniwue value to image. return the indexes of the function that went through the filters.
        self.df_metadata = pd.read_csv(self.conf.metadata_csv_path)
        self.df_clinical = pd.read_csv(self.conf.clinical_csv_path)
        self.merged_df = self.merged_data()
        self.merged_df = self.merged_df.drop_duplicates(subset="png_path", keep="first")
        self.merged_df["image_id"] = pd.factorize(self.merged_df["png_path"])[0]
    
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

    # def set_calc_df(self):
    #     self.calc_df = self.get_df(self.config["calc_file_path"])

    # def set_mass_df(self):
    #     self.mass_df = self.get_df(self.config["mass_file_path"])
    
    # def set_df(self):
    #     self.df = pd.merge(self.calc_df, self.mass_df, how="outer")

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
        return self.merged_df["image_id"].unique().tolist()
        
    def get_patients_data(self, keys_format: str = "camel", include_file_path : bool = False, image_id = None):
        # TODO add validation check for image_id
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

# DEBUG
# dm = DataManager()
# patients_data = dm.merged_df[['side', 'massshape']]
# print(patients_data.head(20))