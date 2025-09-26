# EMBED Open Data Server

Flask server that handles data retrieval and processing, interacting with the EMBED Open Data to serve relevant data to the [Electron app](https://github.com/Oriya-Sigawy/ddsm-electron.git). The backend processes queries, retrieves patient metadata, and returns filtered results.
This server has an analyzer that runs both the server and its Electron app: [Analyzer](https://github.com/AyeletKat/ddsm-analyzer.git). Its best to run it from the analyzer.

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
- It's responsible for:
  - Extracting the unique options for the filtering.
  - Patients data demanded by the electron.
  - The filtering functionality.

### Tests
Tests for all the endpoints.

### EndPoints

The server's endpoints can be found under `filter`, `image` and `patient` folders.

**filter**

- `filter/options`: Returns the unique options for the filters that in the electron app under the **Filters** column.
- `filter/abnormality-options`: Returns the unique options for the filters that in the electron app under the **Abnormality Params** column.
- `filter/empi-anons`: Returns the unique anonymized EMPIs in the dataset.
- - `filter/image-ids`: Returns the unique image IDs in the dataset. *Uses for inner processes in the electron and not as a filter*

**image**

- `images/<image_id>/images-metadata`: Receives image_id and returns the metadata of the image.
  example for response:
  {
    "FinalImageType": "2D",
    "SeriesDescription": "R MLO",
    "ViewPosition": "MLO",
    "imageFormat": "png",
    "image_id": "1",
    "side": "R"
  }
- `images//<image_id>/full`: Receives image_id and returns png file of the image.

**patient**

- `patients/`: Returns all patients data.
- `patients/<patient_id>`: Returns the data of the corresponding patient.
  ```json
  {
    "P_01009": [
      {
        "abnormalityId": 1,
        "abnormalityType": "mass",
        "assessment": 4,
        "breastDensity": 2,
        "imageView": "CC",
        "leftOrRightBreast": "RIGHT",
        "massMargins": "OBSCURED",
        "massShape": "OVAL",
        "pathology": "MALIGNANT",
        "subtlety": 2
      },
      {
        "abnormalityId": 1,
        "abnormalityType": "mass",
        "assessment": 4,
        "breastDensity": 2,
        "imageView": "MLO",
        "leftOrRightBreast": "RIGHT",
        "massMargins": "OBSCURED",
        "massShape": "OVAL",
        "pathology": "MALIGNANT",
        "subtlety": 3
      }
    ]
  }
  ```
- `patients/filter`: Given filters params from the electron electron, this endpoint returns all the patients IDs that match the requested query.
