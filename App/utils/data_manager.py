import pandas as pd
import os

# Get the path to the data folder relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
metadata_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_metadata.csv")
clinical_csv_path = os.path.join(BASE_DIR, "data", "EMBED_OpenData_clinical.csv")

# Load the CSV
df_metadata = pd.read_csv(metadata_csv_path)
df_clinical = pd.read_csv(clinical_csv_path)

# Unify types before merge
df_clinical['acc_anon'] = df_clinical['acc_anon'].astype(str).str.strip()
df_metadata['acc_anon'] = df_metadata['acc_anon'].astype(str).str.strip()

df_clinical['empi_anon'] = df_clinical['empi_anon'].astype(str).str.strip()
df_metadata['empi_anon'] = df_metadata['empi_anon'].astype(str).str.strip()

df_clinical['side'] = df_clinical['side'].astype(str).str.upper().str.strip()
df_metadata['ImageLateralityFinal'] = df_metadata['ImageLateralityFinal'].astype(str).str.upper().str.strip()

# Step 1: Split the clinical data based on 'side' field
df_L = df_clinical[df_clinical['side'] == 'L']
df_R = df_clinical[df_clinical['side'] == 'R']
df_B = df_clinical[df_clinical['side'] == 'B']
df_NaN = df_clinical[df_clinical['side'].isna()]

# Step 2: Merge L side
merged_L = pd.merge(
    df_L,
    df_metadata[df_metadata['ImageLateralityFinal'] == 'L'],
    on=['empi_anon', 'acc_anon'],
    how='inner'
)

# Step 3: Merge R side
merged_R = pd.merge(
    df_R,
    df_metadata[df_metadata['ImageLateralityFinal'] == 'R'],
    on=['empi_anon', 'acc_anon'],
    how='inner'
)

# Step 4: Merge B side (with all L and R images)
merged_B = pd.merge(
    df_B,
    df_metadata[df_metadata['ImageLateralityFinal'].isin(['L', 'R'])],
    on=['empi_anon', 'acc_anon'],
    how='inner'
)

# Step 5: Merge NaN side (also with all L and R images)
merged_NaN = pd.merge(
    df_NaN,
    df_metadata[df_metadata['ImageLateralityFinal'].isin(['L', 'R'])],
    on=['empi_anon', 'acc_anon'],
    how='inner'
)

# Step 6: Concatenate all merged DataFrames
merged_df = pd.concat([merged_L, merged_R, merged_B, merged_NaN], ignore_index=True)
merged_df = merged_df.head(10)

print(merged_df)