import argparse
import os
import logging
import boto3
from pathlib import Path
from typing import Any, Iterator

from botocore.client import BaseClient, Config
from botocore.exceptions import ClientError

def listFiles(s3Client: BaseClient, bucket: str, folderPath: str, recursive: bool) -> Iterator[str]:
    continuationToken = None
    delimiter = None if recursive else "/"
    while True:
        args = {
            "Bucket": bucket,
            "Prefix": folderPath,
        }
        if delimiter:
            args["Delimiter"] = delimiter
        if continuationToken:
            args["ContinuationToken"] = continuationToken
        
        response = s3Client.list_objects_v2(**args)
        for obj in response.get("Contents", []):
            yield obj["Key"]

        continuationToken = response.get("NextContinuationToken")
        if not continuationToken:
            break

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(__name__)

    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / ".env"
        load_dotenv(env_path)
    except ImportError:
        logger.error("Failed to import .env variables. Make sure that python-dotenv is installed.")

    parser = argparse.ArgumentParser(
        description="Demo Python program of AWS S3 file listing."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        default=False,
        required=False,
        help="Should the AWS S3 file listing be done recursively?",
    )
    args = parser.parse_args()

    recursive = args.recursive
    logger.info(f"Example Python Program for AWS S3 File Listing (Recursive: {recursive})")
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

    rootFolder = ""
    logger.info(f"Iterating over files under folder at \"{rootFolder}\":")
    for path in listFiles(s3Client, s3Bucket, rootFolder, recursive):
        logger.info(f"    {path}")

main()
