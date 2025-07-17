import pandas as pd
import os

# Get the path to the data folder relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
metadata_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_metadata.csv")
clinical_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_clinical.csv")
metadata_reduced_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_metadata_reduced.csv")

# Load the CSV
df_metadata = pd.read_csv(metadata_csv_path)
df_clinical = pd.read_csv(clinical_csv_path)
df_metadata_reduced = pd.read_csv(metadata_reduced_csv_path)


merged = pd.merge(
    df_clinical,
    df_metadata,
    on=['empi_anon', 'acc_anon'],
    how='inner'
)

condition = (
    merged['side'].isin(['B', 'NaN']) |
    (merged['ImageLateralityFinal'] == merged['side'])
)
result = merged[condition]
#TODO choose wanted columns
result = result[['empi_anon', 'acc_anon', 'ImageLateralityFinal', 'side']]
# Transpose, drop duplicate rows (i.e. duplicate columns), then transpose back
result = result.T.drop_duplicates().T
print(result.head(100))

