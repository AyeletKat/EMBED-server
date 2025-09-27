# EMBED Open Data Server

Flask server that handles data retrieval and processing, interacting with the EMBED Open Data to serve relevant data to the [Electron app](https://github.com/Oriya-Sigawy/ddsm-electron.git). 

The backend processes queries, retrieves patient metadata, and returns filtered results.

This server has an Analyzer that runs both the server and its Electron app: [Analyzer](https://github.com/AyeletKat/ddsm-analyzer.git).

Its best to run it from the analyzer. 

## Pre-Requisites

To use the following project, please make sure you have the following installed:

- [python](https://www.python.org/downloads/)
- [electron](https://github.com/DDSM-CBIS/ddsm-electron)

- Clone the repository:

```bash
git clone https://github.com/AyeletKat/ddsm-server.git
```

## Usage

Install requirements:

```bash
pip install -r ./requierments.txt
```

Run the server:

```bash
python3 run.py
```
The server runs on port 3000.

## Project Structure
This project interacts with Emory Breast Imaging Dataset (EMBED). you can read more on this dataset here: [EMBED](https://github.com/Emory-HITI/EMBED_Open_Data.git)

### Data

Contains:  
`EMBED_OpenData_clinical.csv` - The data of the patients.  
`EMBED_OpenData_metadata.csv` - The data of the images.

### Utils

The utils folder contains the `data_manager`, that merges both csvs by the instructions in the EMBED repo.  
- It"s responsible for:
  - Extracting the unique options for the filtering.
  - Patients data demanded by the electron.
  - The filtering functionality.
The data_manager downloads the pictures it needs to a folder "downloaded_images" (it create this folter automatically).
Obviouslly if it will need an image that was already downloaded it will take it and not redownload it, but when the size of the folder is too big (defines ob config.py),
it will delete older half of the pictures.
You can change the limit size on config.py.
Also, it takes its data from EMBED_OpenData_clinical.csv, EMBED_OpenData_metadata.csv so you should put them in "data" folder (already exists).
It takes the images from EMBED s3 bucket, so you should get your own access keys and put them in s3_keys.txt (alreadt exists and formatted with the appropriate template).

### Tests
Tests for all the endpoints.

### EndPoints

The server"s endpoints can be found under `filter`, `image` and `patient` folders.

**filter**

- `filter/options`: Returns the unique options for the filters that in the electron app under the **Filters** column.
- `filter/abnormality-options`: Returns the unique options for the filters that in the electron app under the **Abnormality Params** column.
- `filter/empi-anons`: Returns the unique anonymized EMPIs (patient IDs) in the dataset.
- `filter/image-ids`: Returns the unique image IDs in the dataset. *Uses for inner processes in the electron and not as a filter*

**image**

- `images/<image_id>/images-metadata`: Receives image_id and returns the metadata of the image.
  Example for response:
  ```json 
  {  
    "FinalImageType": "2D",  
    "SeriesDescription": "R MLO",  
    "ViewPosition": "MLO",  
    "imageFormat": "png",  
    "image_id": "1",  
    "side": "R"  
  }
  ```
- `images/<image_id>/full`: Receives image_id and returns png file of the image.

**patient**

- `patients/`: Test endpoint to check the connection.
- `patients/<image_id>`: Returns the data of the corresponding patient that whose image what selected.
   Example for response:
  ```json
  {
    "empiAnon": 60696029,
    "accAnon": 8099128854014801,
    "tissueden": 3.0,
    "asses": "A",
    "side": "R",
    "massshape": "S",
    "massmargin": "D",
    "ViewPosition": "MLO"
  }
  ```
- `patients/filter`: Given filters params from the electron app, this endpoint returns all the image IDs that match the requested query.
