import boto3  
import os  
from datetime import datetime, timedelta

def get_session(region, access_id, secret_key):  
    return boto3.session.Session(region_name=region,
                                aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key)

def lambda_handler(event, context):  
    '''This method searches for all EC2 instances with a tag of BackUp
       and creates a backup images of them then tags the images with a
       RemoveOn tag of a YYYYMMDD value of three UTC days from now
    '''
    created_on = datetime.utcnow().strftime('%Y%m%d')
    remove_on = (datetime.utcnow() + timedelta(days=3)).strftime('%Y%m%d')
    session = get_session(os.getenv('REGION'),
                          os.getenv('ACCESS_KEY_ID'),
                          os.getenv('SECRET_KEY'))
    client = session.client('ec2')
    resource = session.resource('ec2')
    reservations = client.describe_instances(Filters=[{'Name': 'tag-key', 'Values': ['BackUp']}])
    for reservation in reservations['Reservations']:
        for instance_description in reservation['Instances']:
            instance_id = instance_description['InstanceId']
            name = f"InstanceId({instance_id})_CreatedOn({created_on})_RemoveOn({remove_on})"
            print(f"Creating Backup: {name}")
            image_description = client.create_image(InstanceId=instance_id, Name=name)
            image = resource.Image(image_description['ImageId'])
            image.create_tags(Tags=[{'Key': 'RemoveOn', 'Value': remove_on}, {'Key': 'Name', 'Value': name}])
