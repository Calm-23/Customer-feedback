import boto3
import uuid
import os

ec2 = boto3.resource('ec2', region_name='us-east-2')
security_group_names = ['launch-wizard-1']
startup_script = None

with open('startup_script.txt', 'r') as script:
	startup_script = script.read()

def delete_keypair(keypair, keypair_file):
	ec2_client = boto3.client('ec2')
	ec2_client.delete_key_pair(KeyName=keypair.key_name)
	os.remove(keypair_file)
	print(f'Keypair \'{keypair_file}\' deleted')


def make_keypair(name):
	try:
		with open(name, 'w+') as file:
			keypair = ec2.create_key_pair(KeyName=name)
			value = str(keypair.key_material)
			file.write(value)
		print(f'{name} created with a new keypair')
		return keypair
	except Exception as e:
		print(f'Error: {e}')

def delete_instance(instance_ids):
	ec2.instances.filter(InstanceIds = instance_ids).terminate()
	print(f'Deleted Instance Ids: {instance_ids}')

def create_and_run_instances(keypair):
	#Amazon Linux 2 AMI 2.0.20200722.0 x86_64 HVM gp2

	ec2_instance = ec2.create_instances(
		ImageId = 'ami-07c8bc5c1ce9598c3',
		InstanceType = 't2.micro',
		SecurityGroups = security_group_names,
		KeyName = keypair.key_name,
		MinCount = 1,
		MaxCount = 1,
		UserData = startup_script)[0]

	print(f'EC2 instance created with id = {ec2_instance.instance_id}!')
	print('Waiting for Instances to start running...')
	ec2_instance.wait_until_running()

	# Reload the instance attributes
	ec2_instance.load()
	print(f'EC2 instance is running at public dns: {ec2_instance.public_dns_name}')
	return ec2_instance


def main():
	print('Creating new Keypair...')
	keypair_file = f'keypair-{str(uuid.uuid4())}.pem'
	keypair = make_keypair(keypair_file)
	if keypair is None:
		print('Could Not create Keypair...')
		print('terminating...')
		return

	print('Creating EC2 Instance...')
	ec2_instance = create_and_run_instances(keypair)

	if ec2_instance is None:
		print('Could not create Instance...')
		print('terminating...')
		return

	print('Enter \'del\' to delete this instance...')
	while True:
		usrinput = input()
		if usrinput == 'del':
			print('Deleting this EC2 Instance...')
			delete_instance([ec2_instance.instance_id])
			
			print('Deleting the Keypair.....')
			delete_keypair(keypair, keypair_file)
			break

if __name__ == "__main__":
	main()