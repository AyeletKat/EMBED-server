import os
class S3Config:
    S3_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
    S3_ACCOUNT_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY =  os.environ.get("AWS_SECRET_ACCESS_KEY")

