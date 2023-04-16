import boto3

ec2=boto3.resource('ec2')

# to create or launch AWS instance

instance=ec2.create_intances(

    ImageId='ami-25615740',
    MinCount=1,
    MaxCount=1,
    Instancetype='t2.micro')

print(instance[0].id)

# to terminate/delete instance
instance_id='1-OF10'
instance=ec2.Instance(instance_id)
response=instance.terminate()
print(response)

#AWSS3 Scripting