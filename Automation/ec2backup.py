*/The ec2backup.py script will simply query all available EC2 instances that have the tag BackUp then create a backup AMI image for each one 
while tagging them a with a RemoveOn tag with a value of 3 days into the future./*

from datetime import datetime, timedelta  
import awsutils

def backup(region_id='us-east-1'):  
    '''This method searches for all EC2 instances with a tag of BackUp
       and creates a backup images of them then tags the images with a
       RemoveOn tag of a YYYYMMDD value of three UTC days from now
    '''
    created_on = datetime.utcnow().strftime('%Y%m%d')
    remove_on = (datetime.utcnow() + timedelta(days=3)).strftime('%Y%m%d')
    session = awsutils.get_session(region_id)
    client = session.client('ec2')
    resource = session.resource('ec2')
    reservations = client.describe_instances(Filters=[{'Name': 'tag-key', 'Values': ['BackUp']}])
    for reservation in reservations['Reservations']:
        for instance_description in reservation['Instances']:
            instance_id = instance_description['InstanceId']
            name = f"InstanceId({instance_id})_CreatedOn({created_on})_RemoveOn({remove_on})"
            print(f"Creating Backup: {name}")
            image_description = client.create_image(InstanceId=instance_id, Name=name)
            images.append(image_description['ImageId'])
            image = resource.Image(image_description['ImageId'])
            image.create_tags(Tags=[{'Key': 'RemoveOn', 'Value': remove_on}, {'Key': 'Name', 'Value': name}])

if __name__ == '__main__':  
    backup()
