#/usr/bin/python
import boto.ec2
conn = boto.ec2.connect_to_region("us-west-2")
conn.run_instances(
    'ami-6ac2a85a',
    key_name='nitheesh_oregon',
    instance_type='t1.micro',
    security_groups=['nitheesh_oregon']
)
