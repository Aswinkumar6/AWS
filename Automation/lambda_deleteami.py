import boto3  
from datetime import datetime  
import os

def get_session(region, access_id, secret_key):  
    return boto3.session.Session(region_name=region,
                                aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key)

def lambda_handler(event, context):  
    '''This method searches for all AMI images with a tag of RemoveOn
       and a value of YYYYMMDD of the day its ran on then removes it
    '''
    today = datetime.utcnow().strftime('%Y%m%d')
    session = get_session(os.getenv('REGION'),
                          os.getenv('ACCESS_KEY_ID'),
                          os.getenv('SECRET_KEY'))
    client = session.client('ec2')
    resource = session.resource('ec2')
    images = client.describe_images(Filters=[{'Name': 'tag:RemoveOn', 'Values': [today]}])
    for image_data in images['Images']:
        image = resource.Image(image_data['ImageId'])
        name_tag = [tag['Value'] for tag in image.tags if tag['Key'] == 'Name']
        if name_tag:
            print(f"Deregistering {name_tag[0]}")
        image.deregister()
