#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError

from pprint import pprint
from datetime import datetime
import json

ec2 = boto3.client('ec2')
sts = boto3.client('sts')

def list_instances(**kwargs):
    show_detail = kwargs.pop('show_detail', 'normal')
    instances = []
    volumeIds = []
    for reservation in ec2.describe_instances(**kwargs)["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance)
            instance['Tags'] = tag_list(instance.get('Tags', []))
            instance['LaunchTime'] = duration_as_hours(instance['LaunchTime'])
            instance['Platform'] = instance.get('Platform', '') + '/' + instance.get('Architecture', '')
            instance['Devices'] = []
            for volume in instance['BlockDeviceMappings']:
                if 'Ebs' in volume:
                    device = {
                        'VolumeId': volume['Ebs']['VolumeId'],
                        'DeviceName': volume['DeviceName']}
                    instance['Devices'].append(device)
                    volumeIds.append(device['VolumeId'])
    # fill volume details
    all_volumes = list_volumes(VolumeIds=volumeIds)
    for instance in instances:
        for volume in instance['Devices']:
            volume.update(all_volumes.get(volume['VolumeId'], {}))

    #prepare show_details
    if show_detail == 'full':
        remove_fields = []
    elif show_detail == 'normal':
        remove_fields = [
            'AmiLaunchIndex', 'ProductCodes', 'Architecture',
            'Placement',
            'NetworkInterfaces', 'PrivateDnsName', 'PublicDnsName', 'SubnetId', 'VpcId',
            'SecurityGroups', 'SourceDestCheck',
            'Architecture', 'Hypervisor', 'VirtualizationType',
            'ClientToken',
            'EbsOptimized', 'RootDeviceName',
            'StateTransitionReason', 'StateReason',
            'ImageId', 'KeyName',
            'BlockDeviceMappings']
    elif show_detail == 'minimal':
        remove_fields = [
            'Platform', 'KernelId', 'EnaSupport', 'Monitoring', 'Platform', 'RootDeviceType',
            'AmiLaunchIndex', 'ProductCodes', 'Architecture',
            'Placement',
            'NetworkInterfaces', 'PrivateDnsName', 'PublicDnsName', 'SubnetId', 'VpcId',
            'SecurityGroups', 'SourceDestCheck',
            'Architecture', 'Hypervisor', 'VirtualizationType',
            'ClientToken',
            'EbsOptimized', 'RootDeviceName',
            'StateTransitionReason', 'StateReason',
            'ImageId', 'KeyName',
            'BlockDeviceMappings']
    else:
        remove_fields = []
    
    for instance in instances:
        for k in remove_fields:
            instance.pop(k, None)
    return instances


def run_instance(instance_ip):
    count = 1
    with open('user_data.sh', 'r') as f:
        user_data=f.read()

    try:
        reservation = ec2.run_instances(
            DryRun=False,
            ImageId='ami-80861296',
            MinCount=count, MaxCount=count,
            KeyName='nickd-wp',
            SecurityGroupIds=['sg-baa2dade', 'sg-4fa7df2b'],
            UserData=user_data,
            InstanceType='t2.large',
            Placement={'AvailabilityZone': 'us-east-1e',
                       'Tenancy': 'default'},
            SubnetId='subnet-3a27b007',
            PrivateIpAddress=instance_ip,
            BlockDeviceMappings=[
                {
                    'VirtualName': 'string',
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'SnapshotId': 'snap-066a4d67938024381',
                        'VolumeSize': 53,
                        'DeleteOnTermination': True,
                        'VolumeType': 'standard'
                    },
                }],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': 'mshared-demo-ubuntu'},
                             {'Key': 'vpc', 'Value': 'mshared'}]
                }],
        )
        return reservation
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            return get_authorization_error(e.response['Error'])
        return e.__dict__
    

def stop_instance(): pass
def start_instance(): pass


def list_volumes(**kwargs):
    volumes = {}
    for volume in ec2.describe_volumes(**kwargs)['Volumes']:
        volumes[volume['VolumeId']] = dict(
            Size=volume['Size'], VolumeType=volume['VolumeType'],
            #Tags=tag_list(volume.get('Tags', []))
        )
    return volumes

def tag_list(tags):
    return [t['Key'] + ': ' + t['Value'] for t in tags]

def duration_as_hours(time):
    delta = datetime.now() - time.replace(tzinfo=None)
    return round(delta.days * 24 + delta.seconds/3600, 2)

def get_authorization_error(err):
    index = err['Message'].index('message: ')
    sts_code =err['Message'][index+9:]
    return json.loads(sts.decode_authorization_message(EncodedMessage=sts_code)['DecodedMessage'])


def machine_list():
    print("machine_list:")
    response = list_instances(
        show_detail='full',
        #InstanceIds=['i-091ecaf4462ec65d8'],
        Filters=[
            {'Name': 'instance-state-name', 'Values':['running']},
            {'Name': 'tag:Name', 'Values': ['mshared-demo-ubuntu']}
        ])
    pprint(response, width=120)

def machine_run():
    print("machine_run:")
    for ip in [
            #'10.0.21.113', '10.0.21.112',
            '10.0.21.111'
            ]:
        reservation = run_instance(ip)
        pprint(reservation, width=120)


if __name__ == "__main__":
    print("no action")
