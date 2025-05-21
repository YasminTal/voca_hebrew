import boto3
import constants
import os

AWS_CREDS=constants.AWS_CREDS
BUCKET_NAME=constants.BUCKET_NAME
REGION=constants.REGION
    


def overwrite_aws_credentials(AWS_CREDS: str):
    """
    Overwrites the ~/.aws/credentials file with the provided AWS_CREDS string.
    
    Parameters:
        AWS_CREDS (str): The new credentials content to be written to the file.
    """
    aws_credentials_path = os.path.expanduser("~/.aws/credentials")

    # Ensure the .aws directory exists
    os.makedirs(os.path.dirname(aws_credentials_path), exist_ok=True)

    try:
        with open(aws_credentials_path, 'w') as file:
            file.write(AWS_CREDS)
        print("AWS credentials successfully overwritten.")
    except Exception as e:
        print(f"Failed to overwrite AWS credentials: {e}")


def create_s3_client(REGION):
    s3_client=boto3.client('s3',region_name=REGION)
    print(f"{s3_client} created successfully.")
    return s3_client

def create_bucket(s3_client,BUCKET_NAME,REGION):
    s3_client.create_bucket(
    Bucket=BUCKET_NAME,
    CreateBucketConfiguration={'LocationConstraint': REGION}
    )
    print (f"{s3_client} created successfully.")

if __name__ == "__main__":

    overwrite_aws_credentials(AWS_CREDS)
    s3_client=create_s3_client(REGION)
    create_bucket(s3_client,BUCKET_NAME,REGION)
   
