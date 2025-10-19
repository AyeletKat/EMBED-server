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
- It's responsible for:
  - Extracting the unique options for the filtering.
  - Patients data demanded by the electron.
  - The filtering functionality.

Importent things to know obout the `data_manager`'s behavior:
- It downloads the pictures it needs to a folder "downloaded_images" (it create this folter automatically).
  Obviouslly if it will need an image that was already downloaded it will take it and not redownload it, but when the size of the folder is too big (defines on      config.py), it will delete older half of the pictures. You can change the limit size on config.py.  
- It takes its data from EMBED_OpenData_clinical.csv, EMBED_OpenData_metadata.csv, so you should put them in "data" folder (already exists).  
- It takes the images from EMBED s3 bucket, so you should get your own access keys and put them in s3_keys.txt. (alreadt exists and formatted with the appropriate template).
- Both csvs have lots of columns, so it refers only to the columns that defines in config.py. You can change it there if you like.
- Because the csvs have lots of columns, there is lots of options to filter on. the existing filters defines on config.py, you can change them by putting the name of the column you want to filter on. 

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


## Important!

The "data" folder in the server and the aws s3 credentials in "s3_keys.txt" in the server are empty.

Working with the EMBED dataset requires filing an access permission request (after receiving an approving letter the work with the aws s3 dataset storage bucket is free).

1. Each user shall request permission via access request form (EMBED Dataset Access Request). (FYI ,They recommend sending the details of the ROOT aws account, not IAM).
2. Clone \ download Analyzer repository and run it. It should download the server and the electron automatically, but the viewer itself will not work yet.
3. After receiving a confirmation email (might take a few days) you can log the aws s3 parameters in the "s3_keys.txt" file in the server repository.
4. Download the "EMBED_OpenData_clinical.csv" and "EMBED_OpenData_metadata.csv" into the "data" folder:
5. Make sure the keys are active via https://us-east-1.console.aws.amazon.com/iam/home#/security_credentials and download the keys csv.
5. Download aws-cli. https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
6. Define your account's access keys in aws-cli: 
7. Open cmd\terminal and type the following, fill with the s3 account data, last two questions are optional, you can leave them empty.
$ aws configure

AWS Access Key ID [****************]: 

AWS Secret Access Key [****************]: 

Default region name [None]: 

Default output format [None]:

8. Now finally downloading the data: open the cmd / terminal
9. To download the clinical data type: 
aws s3 cp s3://embed-dataset-open/tables/EMBED_OpenData_clinical.csv <paste_destination_path>
10. To download the metadata type: 
aws s3 cp s3://embed-dataset-open/tables/EMBED_OpenData_metadata.csv <paste_destination_path>
Voilà! Should be downloaded!
If something failed, the dataset structure might have changed, try browsing through it  aws s3 ls s3://embed-dataset-open/
11. Copy\move the metadata and clinical csv's into the "data" folder in the server.
12. Run the analyzer again, now it should all work! Enjoy!

