# Author: Callum Bond
# Description:

"""
Lambda 1: SSM parameter poller
- Lambda is triggered by a frequent Eventbridge schedule (eg. every 5 mins)
- Checks if the SSM parameters in the shared account contain new AMI IDs.
- If they do,
    - Create an EB schedule that fires after N days with Lambda 2 (below) as the target
        - 0 = non-prod
        - 8 = prod
"""

import boto3
import datetime
import json

from python.shared.config import load_ami_poller_config
config = load_ami_poller_config()

ssm_client = boto3.client('ssm', endpoint_url=config['endpoint_url'])
scheduler_client = boto3.client('scheduler', endpoint_url=config['endpoint_url'])


def handler(event, context):
    print("Received event:", json.dumps(event, indent=2))
    current_ami_id = get_current_ami_id()
    shared_ami_id = get_shared_ami_id()

    if shared_ami_id == current_ami_id:
        print("The current AMI ID is already the latest version.")
        return
    else:
        print("New AMI found.")
        schedule_name = f"{config['env']}-ami-update-schedule-event-rule"
        ami_id = lookup_ami_id_from_deployment_schedule(schedule_name)

        if not ami_id:
            print("Schedule does not exist. Will create.")
            create_deployment_schedule(schedule_name, current_ami_id)
        elif ami_id == current_ami_id:
            print("Schedule already exists for this AMI ID. Skipping.")
        elif ami_id != current_ami_id:
            print("Schedule exists but has a different AMI. Will replace with the newer AMI ID.")
            delete_deployment_schedule(schedule_name)
            create_deployment_schedule(schedule_name, current_ami_id)


def get_current_ami_id():
    """
    Fetch the current AMI ID from the SSM parameter.

    :return: an AMI ID
    """
    print(f"Fetching AMI ID from SSM parameter: {config['ami_ssm_parameter_name']}")
    resp = ssm_client.get_parameter(Name=config['ami_ssm_parameter_name'])
    ami_id = resp['Parameter']['Value']
    print(f"Found value: {ami_id}")
    return ami_id


def get_shared_ami_id():
    """
    Fetch the SSM parameter from the source AWS account for a particular OS platform name.
    """
    os_platform = config['os_platform']
    platform_list = config['platforms']

    # Localstack returns errors if we query secrets by ARN
    if config['is_local']:
        source_ssm_parameter = platform_list[os_platform]['ssm_parameter']
    else:
        source_ssm_parameter = 'arn:aws:ssm:ap-southeast-2:%s:parameter%s' % (config['source_aws_account_id'], platform_list[os_platform]['ssm_parameter'])

    print(f"Fetching shared SSM parameter: {source_ssm_parameter}")
    resp = ssm_client.get_parameter(Name=source_ssm_parameter)
    current_ami_id = resp['Parameter']['Value']
    print(f"Found value: {current_ami_id}")
    return current_ami_id


def lookup_ami_id_from_deployment_schedule(schedule_name):
    print(f"Checking if schedule '{schedule_name}' already exists.")
    try:
        schedule = scheduler_client.get_schedule(Name=schedule_name)
    except scheduler_client.exceptions.ResourceNotFoundException:
        return None

    target_input = json.loads(schedule['Target']['Input'])
    return target_input['ImageId']


def create_deployment_schedule(schedule_name, ami_id):
    """
    Schedule the `ami_updater.py` Lambda to run in N days from now.

    :param schedule_name:
    :param ami_id:
    :return:
    """
    print("Will schedule Lambda to update SSM and to trigger deployment.")
    days_from_now = config['deployment_schedule_in_days']
    schedule_date = datetime.datetime.now() + datetime.timedelta(days=int(days_from_now))
    print(f"Creating schedule. Name={schedule_name}, Days={config['deployment_schedule_in_days']}, Date={schedule_date} UTC")

    scheduler_client.create_schedule(
        Name=schedule_name,
        ScheduleExpression='at(%s)' % (schedule_date.strftime('%Y-%m-%dT%H:%M:%S')),
        ScheduleExpressionTimezone='UTC',
        FlexibleTimeWindow={
            'Mode': 'OFF'
        },
        Target={
            'Arn': config['lambda_ami_updater_function_arn'],
            'RoleArn': config['lambda_ami_updater_role_arn'],
            # Pass the AMI ID to the rule so that the two are associated.
            # This is in case a new AMI is released while the rule is active,
            # and we know to recreate it.
            'Input': '{\"ImageId\":\"%s\"}' % ami_id,
        }
    )


def delete_deployment_schedule(schedule_name):
    print(f"Deleting schedule: {schedule_name}")
    scheduler_client.delete_schedule(Name=schedule_name)
