import pandas as pd
import os

# Get the path to the data folder relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "AWS_Open_Data_metadata.csv")

# Load the CSV
df = pd.read_csv(csv_path)

filtered_df_1 = df["png_path"]
print (filtered_df_1)
# filtered_df_2 = df[df["Header in export"] == "calcdistri"]

# count_1 = len(filtered_df_1)  #suppose to be 1
# count_2 = len(filtered_df_2)  #suppose to be 6

# # Output
# print(f"Number of rows where Code == 1740: {count_1}")
# print(f"Number of rows where Header in export == calcdistri: {count_2}")
# print(filtered_df_1)
# print(filtered_df_2)

