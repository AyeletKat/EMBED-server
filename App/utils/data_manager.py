import pandas as pd
import os

# Get the path to the data folder relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
metadata_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_metadata.csv")
clinical_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_clinical.csv")

# Load the CSV
df_metadata = pd.read_csv(metadata_csv_path)
df_clinical = pd.read_csv(clinical_csv_path)

temp = df_metadata['num_roi'].drop_duplicates()
print(temp)

# def merged_data():
#     merged = pd.merge(
#         df_clinical,
#         df_metadata,
#         on=['empi_anon', 'acc_anon'],
#         how='inner'
#     )

#     condition = (
#         merged['side'].isin(['B', 'NaN']) |
#         (merged['ImageLateralityFinal'] == merged['side'])
#     )
#     merged_df = merged[condition]
#     return merged_df
# def get filtered_data(filters[list[Any]]):
# #TODO choose wanted columns
#     merged_df = merged_df[['empi_anon', 'acc_anon', 'ImageLateralityFinal', 'side']]
#     # Transpose, drop duplicate rows (i.e. duplicate columns), then transpose back
#     merged_df = merged_df.T.drop_duplicates().T
# print(merged_df.head(10))