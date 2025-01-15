import logging
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
import datetime
from botocore.signers import CloudFrontSigner
import requests
import os
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from typing import List

#----------#

from .config import Config

#----------#

logger = logging.getLogger(__name__)

#======================================================================================================================#
# CloudfrontService
#======================================================================================================================#

class CloudfrontService:

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self) -> None:
        self.__signer = CloudFrontSigner(Config.CLOUDFRONT_SETTINGS['key_pair_id'], self.__rsa_signer)
        self.__expires = datetime.datetime.now() + datetime.timedelta(hours = Config.CLOUDFRONT_SETTINGS['url_expiry_hrs'])

    #------------------------------------------------------------------------------------------------------------------#
    
    def __rsa_signer(self, message):
        # Load your private key
        with open(Config.CLOUDFRONT_SETTINGS['private_key'], 'rb') as key_file:
            private_key = RSA.import_key(key_file.read())  # This loads a PKCS#8 key
        # Sign the message
        h = SHA1.new(message)
        signature = pkcs1_15.new(private_key).sign(h)
        return signature
    
    #------------------------------------------------------------------------------------------------------------------#

    def download(self, url: str) -> str:
        signed_url = self.__signer.generate_presigned_url(url, date_less_than = self.__expires)
        response = requests.get(signed_url)
        if (response.status_code == 200):
            local_path = os.path.join(Config.CLOUDFRONT_SETTINGS['local_storage_folder'], os.path.basename(url))
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print('Media downloaded successfully')
            return local_path
        else:
            print('Failed to download media')
            return ''
        
    #------------------------------------------------------------------------------------------------------------------#

    def create_signed_url(self, s3_object_key: str) -> str:
        url = os.path.join(Config.CLOUDFRONT_SETTINGS['domain_name'], s3_object_key)
        return self.__signer.generate_presigned_url(url, date_less_than = self.__expires)

#======================================================================================================================#
# End of CloudfrontService
#======================================================================================================================#

#======================================================================================================================#
# S3Service
#======================================================================================================================#

class S3Service:

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self) -> None:
        self.__s3_client = boto3.client('s3', 
                                        aws_access_key_id = Config.S3_SETTINGS['aws_access_key_id'],
                                        aws_secret_access_key = Config.S3_SETTINGS['aws_secret_access_key'])

    #------------------------------------------------------------------------------------------------------------------#
    
    def upload(self, local_path, delete_local = False):
        key = os.path.basename(local_path)
        print('Uploading file to: ', key)
        self.__s3_client.upload_file(local_path, Config.S3_SETTINGS['bucket_name'], key)
        if delete_local:
            os.remove(local_path)
            print(f'Local file {local_path} deleted')
        print(f'File uploaded to S3 bucket at path:', key)
        return key
        
    #------------------------------------------------------------------------------------------------------------------#
    
    def delete(self, key):
        response = self.__s3_client.delete_object(Bucket = Config.S3_SETTINGS['bucket_name'], Key = key)
        print(f'File {key} deleted from S3 bucket')
        return response
        
    #------------------------------------------------------------------------------------------------------------------#
    
    def download(self, key: str):
        local_path = os.path.join(Config.LOCAL_TEMP_STORE, key)
        print(f"Downloading file {key} from S3 bucket to: {local_path}")
        self.__s3_client.download_file(Config.S3_SETTINGS['bucket_name'], key, local_path)
        print(f"File {key} downloaded successfully")
        return local_path
    
#======================================================================================================================#
# End of S3Service
#======================================================================================================================#

#======================================================================================================================#
# SNService
#======================================================================================================================#

class SNSService:

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self) -> None:
        self.__sns = boto3.client('sns', 
                                  region_name = Config.SNS_SETTINGS['region'], 
                                  aws_access_key_id = Config.SNS_SETTINGS['aws_access_key_id'], 
                                  aws_secret_access_key = Config.SNS_SETTINGS['aws_secret_access_key'])

    #------------------------------------------------------------------------------------------------------------------#

    def __format_message_attributes(self, attributes: dict) -> dict:
        formatted_attributes = {}
        for key, value in attributes.items():
            if isinstance(value, str):
                formatted_attributes[key] = {"DataType": "String", "StringValue": value}
            elif isinstance(value, int):
                formatted_attributes[key] = {"DataType": "Number", "StringValue": str(value)}
            else:
                raise ValueError("Invalid attribute value type: {}".format(type(value)))
        return formatted_attributes

    #------------------------------------------------------------------------------------------------------------------#

    def publish_message(self, subject: str, message: str, endpoint_arn: str, message_attributes: dict):
        message_attributes = self.__format_message_attributes(message_attributes)
        response = self.__sns.publish(TargetArn = endpoint_arn,
                                      Subject = subject,
                                      Message = message,
                                      MessageAttributes = message_attributes)
        print(f"Message published. status: {response}")
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
        
    #------------------------------------------------------------------------------------------------------------------#

    def register_device(self, device_token: str, user_id: int):
        try:
            # Try to create a new endpoint
            response = self.__sns.create_platform_endpoint(PlatformApplicationArn = Config.SNS_SETTINGS['ios_platform_arn'],
                                                           Token = device_token,
                                                           CustomUserData = str(user_id))
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameter':
                # Endpoint already exists, retrieve its ARN
                endpoints = self.__sns.list_endpoints_by_platform_application(PlatformApplicationArn = Config.SNS_SETTINGS['ios_platform_arn'])
                for endpoint in endpoints['Endpoints']:
                    if endpoint['Attributes']['Token'] == device_token:
                        endpoint_arn = endpoint['EndpointArn']
                        # Update the endpoint with the new user_id
                        self.__sns.set_endpoint_attributes(EndpointArn = endpoint_arn,
                                                           Attributes = {'CustomUserData': str(user_id), 'Enabled': 'true'})
                        break
                else:
                    raise ValueError("Endpoint not found for the given token")
            else:
                raise e
        # Subscribe the endpoint to your topic
        self.__sns.subscribe(TopicArn = Config.SNS_SETTINGS['topic_arn'],
                             Protocol = Config.SNS_SETTINGS['protocol'],
                             Endpoint = endpoint_arn)
        return False
    
    #------------------------------------------------------------------------------------------------------------------#
    
    def get_endpoints_arn_by_user_id(self, target_user_id: int) -> List[str]:
        target_user_id = str(target_user_id)
        platform_application_arn = Config.SNS_SETTINGS['ios_platform_arn']
        next_token = None
        enabled_endpoints = []
        while True:
            if next_token:
                response = self.__sns.list_endpoints_by_platform_application(PlatformApplicationArn = platform_application_arn,
                                                                             NextToken = next_token)
            else:
                response = self.__sns.list_endpoints_by_platform_application(PlatformApplicationArn = platform_application_arn)
            for endpoint in response['Endpoints']:
                user_id = endpoint['Attributes'].get('CustomUserData')
                is_enabled = endpoint['Attributes'].get('Enabled', '').lower() == 'true'
                if user_id == target_user_id and is_enabled:
                    enabled_endpoints.append(endpoint['EndpointArn'])
            if 'NextToken' in response:
                next_token = response['NextToken']
            else:
                break
        return enabled_endpoints

#======================================================================================================================#
# End of SNService
#======================================================================================================================#
