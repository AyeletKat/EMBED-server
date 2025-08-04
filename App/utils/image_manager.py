# upload code - funcitons to Oriya | decide on additional metadata to return

import boto3
import os

def download_image_by_name(png_name):
    """
    Downloads a PNG image from S3 given its png_path from metadata.scv.
    Args:
        png_name (str): The name of the PNG file path (e.g., '/mnt/PACS_NAS1/mammo/png/cohort_1/extracted-images/38b.../eed16....png').
    
    Preprocessing: in order to match path to S3 structure:
    Delete Prefix, change png to png_images, remove 'extracted-images' from the path.
    Place the image in a subfolder named after the PNG file.
    """
    #  delete the prefix and 'extracted-images' from the path
    png_name = png_name.replace('/mnt/PACS_NAS1/mammo/', '').replace('extracted-images/', '') # check that all images have the same prefix
    png_name = png_name.replace('png/', 'png_images/')  #
    # folder_prefix = f'png_images/'
    bucket_name = 'embed-dataset-open'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # png_path = f"{folder_prefix}{png_name}" #
    # download_dir = 'downloaded_images'
    # # os.makedirs(download_dir, exist_ok=True)
    # # filename = os.path.join(download_dir, png_name)
    # filename = os.path.join(download_dir, png_name)
    # os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure all parent dirs exist

    png_path = f"{png_name}" #
    download_dir = 'downloaded_images'
    # Place each image in a subfolder named after the PNG file (without extension)
    base_name = os.path.splitext(os.path.basename(png_name))[0]
    folder_path = os.path.join(download_dir, base_name)
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, os.path.basename(png_name))

    try:
        print(f"Downloading {png_path} to {filename}")
        bucket.download_file(png_path, filename)
        print(f"Downloaded {png_name} successfully.")
    except Exception as e:
        print(f"Error downloading {png_name}: {e}")

# Example usage:
# download_image_by_name('/mnt/PACS_NAS1/mammo/png/cohort_1/extracted-images/10f16c9202719fb63957e0b67c97a7380eff88765e36d6781ec3c43f/b5f0c9a8d05e485b36032a0c3972e6dbeb43076db2270bee7662b3ef/53fcc92b71f21c180291eb394f93ccbb1775f6031e49f7d6886c62fc.png')


# /mnt/PACS_NAS1/mammo/png/cohort_1/extracted-images/38b0d72c577237bb5505103e0d9091fe8daa9a1a3a027a72933bef28/044795bfdbd82421d0032132bbfaa9d17d94465619d2581107899595/eed16a2c17f81f82ea8381ff17a23f57df0c4978624d265a1d7ce96a.png
# /mnt/PACS_NAS1/mammo/png/cohort_1/extracted-images/10f16c9202719fb63957e0b67c97a7380eff88765e36d6781ec3c43f/b5f0c9a8d05e485b36032a0c3972e6dbeb43076db2270bee7662b3ef/53fcc92b71f21c180291eb394f93ccbb1775f6031e49f7d6886c62fc.png




# find minimal and maximal values of acc_anon and empi_anon columns

import pandas as pd
def find_min_max_acc_empi(file_path):
    df = pd.read_csv(file_path)
    min_acc = df['acc_anon'].min()
    max_acc = df['acc_anon'].max()
    min_empi = df['empi_anon'].min()
    max_empi = df['empi_anon'].max()
    
    return min_acc, max_acc, min_empi, max_empi

# Example usage:
# file_pathh = 'EMBED_OpenData_metadata.csv'
# min_acc, max_acc, min_empi, max_empi = find_min_max_acc_empi(file_pathh)
# print(f"Min acc_anon exam id: {min_acc}, Max acc_anon: {max_acc}")
# print(f"Min empi_anon patient id: {min_empi}, Max empi_anon: {max_empi}")

# find longest common seffix in acc_anon float numbers column
def find_longest_common_suffix(file_path):
    df = pd.read_csv(file_path)
    acc_anon = df['acc_anon'].astype(str).tolist()  # Convert to string for suffix comparison
    
    if not acc_anon:
        return ""
    
    # Start with the first element as the initial longest suffix
    longest_suffix = acc_anon[0]
    
    for acc in acc_anon[1:]:
        # Compare current longest suffix with each acc_anon
        while not acc.endswith(longest_suffix):
            longest_suffix = longest_suffix[:-1]  # Shorten the suffix until it matches
            if not longest_suffix:  # If we run out of characters, return empty
                return ""
    
    return longest_suffix
# Example usage:
# file_path = 'EMBED_OpenData_metadata.csv'
# longest_suffix = find_longest_common_suffix(file_path)
# print(f"Longest common suffix in acc_anon: {longest_suffix}")

#  find value in acc_anon float values column that doesn't end with "000000.00"
def find_non_suffix_value(file_path):
    df = pd.read_csv(file_path)
    acc_anon = df['acc_anon'].astype(str).tolist()  # Convert to string for suffix comparison
    
    for acc in acc_anon:
        if not acc.endswith("000000.0"):
            return acc  # Return the first value that doesn't end with "000000.00"
    
    return None  # If all values end with "000000.00"
# Example usage:
# file_path = 'EMBED_OpenData_metadata.csv'
# non_suffix_value = find_non_suffix_value(file_path)
# print(f"Value in acc_anon that doesn't end with '000000.00': {non_suffix_value}")


