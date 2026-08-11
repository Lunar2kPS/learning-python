import argparse
import os
import logging
import boto3
from pathlib import Path
from typing import Any, Iterator

from botocore.client import BaseClient, Config
from botocore.exceptions import ClientError

def downloadFile(s3Client: BaseClient, bucket: str, key: str) -> bytes:
    resp = s3Client.get_object(Bucket=bucket, Key=key)
    with resp["Body"] as body:
        return body.read()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)

    try:
        from dotenv import load_dotenv
        _env_path = Path(__file__).parent / ".env"
        load_dotenv(_env_path)
    except ImportError:
        logger.error("Failed to import .env variables. Make sure that python-dotenv is installed.")
        pass

    parser = argparse.ArgumentParser(
        description="Demo Python program of AWS S3 file listing."
    )
    parser.add_argument(
        "--path",
        type=str,
        default="",
        required=True,
        help="The AWS S3 file path (key) to the file you would like to test downloading with get_object.",
    )
    args = parser.parse_args()

    path = args.path
    logger.info(f"Example Python Program for AWS S3 File Downloads")
    s3Config = Config(s3={
        "addressing_style": "path" # NOTE: as opposed to "virtual"
    })

    s3Endpoint = os.getenv("S3_ENDPOINT", "")
    s3Region = os.getenv("S3_REGION", "")
    s3AccessKey = os.getenv("S3_ACCESS_KEY", "")
    s3SecretKey = os.getenv("S3_SECRET_KEY", "")
    s3Bucket = os.getenv("S3_BUCKET", "")
    s3Client : BaseClient = boto3.client(
        "s3",
        endpoint_url=s3Endpoint,
        region_name=s3Region,
        aws_access_key_id=s3AccessKey,
        aws_secret_access_key=s3SecretKey,
        config=s3Config
    )

    logger.info(f"Downloading file at at \"{path}\":")
    fileBytes = downloadFile(s3Client, s3Bucket, path)
    filePath = Path(path)
    localFolder = Path("__pycache__")
    localFolder.mkdir(parents=True, exist_ok=True)
    localPath = localFolder / filePath.name
    with open(localPath, "wb") as file:
        file.write(fileBytes)
    logger.info(f"Wrote file bytes to: \"{localPath}\".")

main()
