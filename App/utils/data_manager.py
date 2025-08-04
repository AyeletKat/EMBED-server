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
        merged_df = self.merged_data()
    
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
    
    
    def get_unique_values(self, collection: str, keys_format = "camel"):
        if collection == "common":
            columns = self.conf.FILTERS
        elif collection == "distinct":
            columns = self.conf.ABNORMALITY_FILTERS
        unique_values = {col: set() for col in columns}
        for col in columns:
                unique_values[col].update(self.df_clinical[col].dropna().unique())     
        unique_values = {self.convert_key_format(k, keys_format): sorted(list(v)) for k, v in unique_values.items()}
        return unique_values

    def get_patient_ids(self):
        return self.df["patient_id"].unique().tolist()

    # TODO: I was fixing this function (using google colab)
    #TODO: add a column PatientID that is empianonaccanonside
    """
    The purpose of this function is to return a dictionary where:
    Each key is a unique patient ID (empi_anon, converted to camelCase).
    Each value is a list of dictionaries, where each dictionary represents a row of that patient's data (with non-null values), excluding the patient_id field.
    It organizes and cleans patient data from a merged DataFrame (self.merged_df) for easier access and use per patient.
    """
    def get_patients_data(self, keys_format="camel", include_file_path=False, patient_id=None):
        patients_data = self.df

        if patient_id:
            patients_data = patients_data[patients_data["patient_id"] == patient_id]

        if not include_file_path:
            patients_data = patients_data[[col for col in patients_data.columns if "file_path" not in col]]
        
        patients_data = patients_data.dropna(axis=1, how="any")
        patients_data = patients_data.rename(columns={col: self.convert_key_format(col, keys_format) for col in self.df.columns})

        patients_dict = {}
        grouped = patients_data.groupby(self.convert_key_format('patient_id', keys_format))

        for p_id, group in grouped:
            patient_list = [
                {k: v for k, v in row.items() if pd.notnull(v) and k != self.convert_key_format('patient_id', keys_format)}
                for row in group.to_dict(orient='records')
            ]
            patients_dict[p_id] = patient_list

        return patients_dict

    
    def filter_patients(self, filters):
        """
        Filter patients data

        Parameters
        ----------
        filters: dict
            The filters to apply to the data
        
        Returns
        -------
        dict
            The filtered data
        """
        filtered_df = self.df
        merged_filters = {}
        for key, value in filters.items():
            for filter_key in value:
                filter_key_formatted = self.convert_key_format(filter_key, "snake")
                merged_filters[filter_key_formatted] = value[filter_key]

        if not merged_filters:
            return self.get_patient_ids()
        
        for column, values in merged_filters.items():
            if column in self.df.columns:
                filtered_df = filtered_df[filtered_df[column].isin(values)]
    
        return filtered_df['patient_id'].unique().tolist()

    # def start(self, config):
    #     self.set_config(config)
    #     self.set_calc_df()
    #     self.set_mass_df()
    #     self.set_df()
