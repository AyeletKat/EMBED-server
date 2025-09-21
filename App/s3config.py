import os
from App.config import S3Details

class S3Config:
    try:
        data = {}
        with open(S3Details.S3_KEYS_FILE_NAME) as f:
            exec(f.read(), {}, data)        # also add to readme how keys file should look like
        S3_ACCOUNT_ID = data.get("S3_ACCOUNT_ID")
        S3_ACCOUNT_KEY = data.get("S3_ACCOUNT_KEY")
        S3_SECRET_ACCESS_KEY = data.get("S3_SECRET_ACCESS_KEY")
    except FileNotFoundError:
        S3_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
        S3_ACCOUNT_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
        S3_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")



