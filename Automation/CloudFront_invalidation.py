#/usr/bin/python
import boto
dist_id = 'xxxxxxxxxxx'
invalidation_path = '/home/ec2-user/invalid.txt'
def main():
    paths = open(invalidation_path,"r+")
    conn = boto.connect_cloudfront()
    inval_req = conn.create_invalidation_request(dist_id, paths)
    print inval_req
    touch = open(invalidation_path,"w")
    touch.write("")
if __name__ == '__main__':
    main()
